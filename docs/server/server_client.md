# サーバーとクライアントの扱いについて

## サーバーの起動

サーバーを起動するためには，[CommandServer](../../can09/server/command_server.py) クラスを利用します．

### サーバーの初期化

*CommandServer* を初期化するためには *SocketTransceiver* オブジェクトと *Request* クラスが必要です．

*SocketTransceiver* オブジェクトは [pisat](https://github.com/jjj999/pisat/) で定義されています．
このオブジェクトは

```python
# TransceiverBase を継承したクラスのオブジェクトを作る
im920_server_handler = PyserialSerialHandler("/dev/tty/USB0")
im920_server = Im920(im920_server_handler)

# TrasnceiverBase を継承したクラスのオブジェクトをラップする
socket_transceiver_server = SocketTransceiver(im920_server)
```

のように作成します．
この SocketTransceiver オブジェクトは通信のハードウェアを定義するために必要です．

次に *Request* クラスを準備する必要があります．
これは，既に用意されているのでインポートするだけで OK です．

```python
from can09.server import Request
```

このオブジェクトはクライアントからのリクエストを処理するために必要です．
*Request* はユーティリティクラスなのでインスタンス化する必要はありません．

これらを踏まえてサーバーの初期化は

```python
from can09.server import CommandServer

server = CommandServer(socket_transceiver_server, Request)
```

で行えることが出来る．

### コマンドの登録

サーバーを初期化したら，起動する前にまずコマンドを登録する必要があります (コマンドの詳細は[こちら](./command.md))．
コマンドの登録は *append* メソッドを使って行います．
*append* は任意個のコマンドを受け付けます．

```python
# TestCommand1, TestCommand2 というコマンドがあるとします
server.append(TestCommand1, TestCommand2)
```

コマンドが比較的多い場合，

```python
commands = (TestCommand1, TestCommand2, TestCommand3, TestCommand4)
server.append(*command)
```

のように登録すると便利です．

### サーバーの起動

コマンドが登録できたらサーバーを起動できます．
サーバーは *start_serve* メソッドを利用して起動できます．
もしコマンドが1つも登録されていない場合には *RequestCommandError* を送出します．

```python
server.start_serve()
```

サーバーを起動する際はタイムアウトを設定できます．
単位は秒です．
タイムアウトは**クライアントからの1回のリクエスト受付の最大の待機時間**です．
決して，タイムアウトに設定した時間が経過すると終了するというわけではありません．

例えばタイムアウトを5秒に設定すると，5秒間リクエストがなければサーバーは終了します．
しかし，クライアントから3秒間隔でリクエストが来るような場合ではサーバーは起動し続けます．

```python
# タイムアウトを5秒に設定する場合
server.start_serve(timeout=5.)
```

## リクエストの送り方

これまでサーバー側の説明をメインに行ってきましたが，もちろんクライアント側にも所定の手順が存在します．

### サーバーへのソケットを作成する

サーバーとの通信において，クライアントを表現する特別なクラスはありません (必要ないからです)．
なので，pisat の TransceiverBase を継承したクラスのような通信機能を持つクラスならなんでも使えることになりますが，*SocketTransceiver* を利用して *CommSocket* オブジェクトを作成し通信するのが便利です．

*SocketTransceiver* のセットアップ方法はサーバーの説明で示した方法と全く同じです．

```python
from pisat.handler import PyserialSerialHandler
from pisat.comm.transceiver import Im920, SocketTransceiver

# TransceiverBase を継承したクラスのオブジェクトを作る
im920_client_handler = PyserialSerialHandler("/dev/tty/USB1")
im920_client = Im920(im920_client_handler)

# TrasnceiverBase を継承したクラスのオブジェクトをラップする
socket_transceiver_client = SocketTransceiver(im920_client)
```

次に，*CommSocket* オブジェクトを *SocketTransceiver.create_socket* メソッドを使って作成します．

```python
# アドレスの表記方法は Transceiver クラスによって異なります
# Im920 の場合はデバイスの ID のみで識別します
server_address = (3B6D,)

# 相手側のアドレスを指定してソケットを作成します
socket = socket_transceiver_client.create_socket(server_address)
```

このようにソケットを作成する利点は以下のとおりです．

- 相手側のアドレスは作成時に一回だけ指定すれば良い
- 相手が複数存在する場合にオブジェクトで区別出来る
- 他の相手とのデータの送受信の影響を受けない
- パケット量 (一度の通信でのバイト数の制限) を気にしなく良くなる

上記の利点はクライアントサーバーモデルを実装する上で重要です．
特にパケット量を気にする必要がないのは非常に強力で，多様なリクエストを可能にします．
例えば，CommSocket を用いず Im920 クラスをそのまま使った場合，リクエストが 64 byte を超過するとエラーが発生してしまいます．
つまり，リクエストは 64 byte 以下でなければならないという制限が課せられることになります．
しかし，この問題は CommSocket を利用することで回避できます．
このような理由から，クライアントが CommSocket を利用することはデファクトスタンダードであると言えます．

### ソケットでリクエストを送る

リクエストの送り方は [コマンドの説明](./command.md) で述べたレスポンスの送り方とほとんど同じです (ここではレスポンスも一種のリクエストとして実装されているからです)．
すなわち，

1. RequestForm を使ってフォームを生成
2. フォームに記入 (フォームの内容を埋める)
3. Request.make_request を使ってフォームの内容からフォーマット済みデータを作成
4. フォーマット済みデータを送信

の手順を踏みます．
最後の送信はもちろん CommSocket を利用します．

例として，以下のようなコマンドが定義されているとします ([コマンドの説明](./command.md)で使用したコマンドクラスです)．

```python
from pisat.comm.transceiver import CommSocket

from can09.server import CommandBase, ResponseBase
from can09.server import RequestForm, RequestParams, Request

class CatCommand(CommandBase):
    COMMAND = b"BB"
    LEN_ARGS = CommandParams.ARGS_ARBITARY

    @classmethod
    def exec(cls, socket: CommSocket, params: RequestParams) -> None:
        # 引数を結合する
        data_concatenated = b"".join(params.args)

        # 以下はレスポンスの作成

        # フォームを作成
        form = RequestForm()
        form.reception_num = params.reception_num
        form.command = ResponseBase
        form.args = (data_concatenated,)

        # フォームからデータを生成
        data_sending = Request.make_request(socket, form)

        # フォーマット済みデータを送信
        socket.send(data_sending)
```

このコマンドをリクエストとしてフォーマットしてサーバーに送るためには以下のようにします．

```python
import codecs

from pisat.comm.transceiver import Im920

from can09.server import CommandBase, ResponseBase
from can09.server import RequestForm, RequestParams, Request

# ソケット作成部分は省略

args = ["Hello", "World", "!!!"]
args = tuple(map(Im920.encode, args))

# RequestForm オブジェクトを作成
form = RequestForm()

# フォームに必要な内容を登録
form.reception_num = 100
form.command = CatCommand
form.args = args

# フォーマット済みデータを生成
data_sending = Request.make_request(socket.addr_yours, form)

# IM920 はASCII文字の16進数表現なので追加で変換
data_sending = codec.encode(data_sending, "hex_codec")

# データ送信
socket.send(data_sending)
```

### レスポンスを確認する

リクエストを送るとコマンドによってはサーバーはレスポンスを返します．
さきほど例として作った CatCommand もレスポンスを返すコマンドです．
レスポンスを見るためには *Request* クラスの *parse_request* メソッドを使います．
このメソッドを使用すると，リクエストが解析され *RequestParam* というクラスが返ってきます．
この *RequestParams* クラスにはレスポンスとして送られきた内容が全て含まれています．

```python
# レスポンスを解析する．CommSocket オブジェクトを渡すことで
# 勝手に必要なだけデータを受信し解析を行うので，このメソッド
# を呼び出す前に socket.recv などでデータを受信する必要はあり
# ません (というかデータが壊れるのでやらないでください)．
params = Request.parse_request(socket)
```

*RequestParams* には以下のような属性があります．

- *reception_num* (リクエストを送る際に設定した数字)
- *command* (レスポンスなので **FF** で固定)
- *address* (サーバーのアドレス)
- *args* (レスポンス内容)

それぞれ[フォーマットの説明](./format.md)で述べたパラメータに対応しています．
最も重要な属性は *RequestParams.args*  という属性です．
この属性にはレスポンスの内容がタプルとして格納されています．
例えば上の例だと，CatCommand というコマンドはクライアントから受け取った引数を結合し，レスポンスとして返すコマンドであったので，

```python
# 内容は bytes で格納されているのでデコードして str にしておく
args = list(map(Im920.decode, params.args))

print(args)
# [HelloWorld!!!]
```

のように返ってくるはずです．
このようにしてサーバーがリクエストに対して返したレスポンスを確認することが出来ます．
