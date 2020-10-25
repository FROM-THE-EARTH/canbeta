# コマンドについて

## コマンドの定義方法

この通信におけるコマンドは通常の PC のターミナルで行うコマンドとほとんど同じ構造をしています．
つまり，コマンド名があり引数があり，その情報をもとに処理を実行します．
ただし以下の点が異なります．

- オプション引数はなく位置引数のみを持ちます
- 結果もコマンド (コマンド名はFF) として返ってくる
- コマンドは CommandBase のサブクラスとして定義される

特にコマンドの定義という点で上の3つの項目のうち最後の項目が重要になります．

コマンドの基礎となる CommandBase は非常に軽量なクラスです．
ユーザーが実質的に定義すべき項目は3つだけです:

```python
from enum import Enum, auto
from typing import Any

from pisat.comm.transceiver import CommSocket

from can09.server.request import RequestParams


class CommandParams(Enum):
    ARGS_NOTHING = auto()
    ARGS_ARBITARY = auto()


class CommandBase:
    
    COMMAND = b""
    LEN_ARGS = CommandParams.ARGS_NOTHING
    
    @classmethod
    def exec(cls, socket: CommSocket, params: RequestParams) -> Any:
        pass

class ResponseBase(CommandBase):
    
    COMMAND = b"FF"

```

*COMMAND* はコマンド名で bytes 型です．
[フォーマットの説明](./format.md)でも述べたようにコマンド名はアルファベット2文字です．

*LEN_ARGS* はコマンドの引数の数です．
特別な引数の数として CommandParams の属性を使うことも出来ますが，使わなくても OK です．

*exec* はサーバーが *COMMAND* と同じコマンド名を持つリクエストを受けた場合に呼び出されるメソッドです．
つまり，コマンドの実行は具体的にこのメソッドで行われます．
引数には *CommSocket* と *RequestParams* が渡されます．
*CommSocket* は pisat で定義されているもので，自分のアドレスと相手のアドレスをつなぎ，いかにも 2 つの端末間で通信がなされているかのように見せかけることが出来るオブジェクトです．
コマンドは *CommSocket* を使ってレスポンスを返すことが出来ます．
*RequestParams* は[フォーマットの説明](./format.md)で述べられたフォーマットの各パラメータが格納されたクラスです．
このクラスからリクエストの内容について (例えばコマンドの引数) 知ることが出来ます．

上のコードスニペットからわかるように，CommandBase にはインスタンス変数やインスタンスメソッドは一切ありません．

例として，引数を結合してクライアントにレスポンスを返すコマンドを作ってみます．

```python
from pisat.comm.transceiver import CommSocket

from can09.server import CommandBase, ResponseBase
from can09.server import RequestForm, RequestParam, Request

class CatCommand(CommandBase):
    COMMAND = b"BB"
    LEN_ARGS = CommandParams.ARGS_ARBITARY

    @classmethod
    def exec(cls, socket: CommSocket, params: RequestParams) -> None:
        # 引数を結合する
        data_concatenated = b"".join(params.args)

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

上の例のように，レスポンスを返す手順は

1. RequestForm を使ってフォームを生成
2. フォームに記入 (フォームの内容を埋める)
3. Request.make_request を使ってフォームの内容からフォーマット済みデータを作成
4. フォーマット済みデータを送信

の流れになります．
上記の例では引数を結合するという意味のない処理をしていましたが，これを他の処理に変えることでコマンドをいくらでも多様にすることが出来ます．


## コマンドの登録

定義したコマンドはサーバーに追加してあげなければ動作しません．
サーバークラスとしては CommandServer を用いる必要があり，

```python
command_server.append(CatCommand)
```

のように，append メソッドを用いてコマンドを**クラスのまま追加**しなければなりません．


## コマンドの種類

現時点で用意されているコマンドを以下に列挙します．
アルファベット2文字はコマンド名です．

### レスポンスを返す (FF)

### プログラムを終了させる

