# テストと依存関係の解決

## テストの概要

### テストスクリプト

テストスクリプト (テスト用の Python ファイル) は fte-can09/test/ ディレクトリ内に置いてください．
そして必ず **test_xxxxxxx.py** という命名規則でファイル名を作成してください．
xxxxxx の部分はテストするクラス名やファイル名にするとわかりやすいです．

テストスクリプトはテストしたい内容を自由に記述してください．
本来は [unittest](https://docs.python.org/ja/3.6/library/unittest.html) というテストフレームワークを
使用するべきですが，習得コストがかかるので現在は検討中です．

### 環境

PC 環境で出来るテストのほとんどが**論理テスト**です．
つまり，論理的に上手くいくかどうかのテストしか行うことが出来ません．
それもセンサやモータなどの外部機器を一切使わずにです．
ただし，PC に接続可能な機器については実機テストを一部行うことが出来ます．

基板は現在発注手続きを進めていますが，早ければ10月の中旬，遅ければ10月末あたりに完成する予定です．
つまり，11月に実機テストラッシュを行うことになるため，10月中は論理テストのみの実行で開発を進めてください．

実機がないことへの対応として，Precursor の実機を使用してみようと考えています．

## 依存関係の解決

テストスクリプトを書く際に，import エラーにハマる可能性があります．
import エラーが発生する原因は，can09 パッケージが仮想環境における Python インタプリタの参照先ディレクトリ内
に含まれていないからです．
Python インタプリタの参照先リストは

```python
import sys

print(sys.path)
```

とすると参照出来ます．
ちなみに sys.path は参照先ディレクトリのリストです．

この問題を解決するには2つの方法があります．

1. 参照ディレクトリ内に can09 のコピーを人為的に加える
2. sys.path に can09 の親ディレクトリを append する

### 参照ディレクトリ内に can09 のコピーを人為的に加える

この方法をとるためには fte-can09/local.py というファイルを使います．
Windows の場合と Mac，Linux の場合で方法が異なります．

この方法は仮想環境内に can09 を取り込ませるので，VS Code の構文解析もでき非常に便利です．
ただし，can09 が更新される度にコピーを実行する必要があります．
なぜなら，コピーした内容はその当時の内容のままだからです．

#### Windows の場合

リポジトリのルート (fte-can09 上) で **local.py** ファイルを実行します．

```
$ python local.py
```

すると，仮想環境内の参照先ディレクトリにそのときの can09 パッケージのコピーが追加されます．


#### Mac, Linux の場合

この場合，ひと手間加える必要があります．
まず，**local.py をコピー**します．
名前は **_local.py** にしておいてください (.gitignore に登録済みなので)．

```
$ cp local.py _local.py
```

そして，_local.py の印がある場所に変更を加えます．
変更する変数は **name_env** です．
これは仮想環境の名前で **fte-can09-xxxxxxxxxxxx** という名前です．
仮想環境の名前は

```
$ ls ~/.local/share/virtualenvs/
```

とすると見つけることが出来ます．
仮想環境の名前を見つけたらコピーし，*name_env* 変数に設定します．

```python
...

if __name__ == "__main__":
    name_pkg = "can09"
    name_env = "fte-can09-xxxxxxx"             # TODO add env name if in Mac or Linux
    version_python = "3.7"

    main(name_pkg, name_env)
```

そして _local.py を保存し実行します．

```
$ python _local.py
```

すると，仮想環境内の参照先ディレクトリにそのときの can09 パッケージのコピーが追加されます．


### sys.path に can09 の親ディレクトリを append する

この方法は Python 実行時に can09 をインポート出来るように設定する方法です．
can09 の親ディレクトリである fte-can09 を sys.path に append すればOKです．

```python
import sys
import os

# can09 をインポートする前に append
sys.append(os.path.abspath(".."))     # fte-can09/test にいる場合
import can09
```

この方法を利用すると特別になにかしなくても最新の can09 をインポート出来ます．
したがって上のようなコードを覚えれば便利だと思われるかもしれませんが，
次のようないくつかの欠点もあります．

- fte-can09 の場所がメンバー全員一緒とは限らない
- ファイルを書く度に必要
- VS Code による can09 パッケージの構文解析が行われない

特に1番目と3番目が開発において致命的です．
したがって，can09 のインポートエラーを解決するためには，基本的に **local.py を実行する方法** を利用してください．


## Node.judge のシミュレート

csv ファイルを用いた Node.judge のシミュレートは pisat.test.core.util 内の **simulate_judge_from** 関数を使うと便利です．
ただし制限があり，**別途 Node.judge に相当する関数を定義** する必要があります．
例えば，

```python
import pisat.config.dname as dname
from pisat.core.nav import Node

class TestNode(Node):

    def judge(self, data):
        altitude = data[dname.ALTITUDE_SEALEVEL]

        if altitude < 10:
            return True
        else:
            return False
```

という Node があった場合，

```python

def judge_testnode(data):
    altitude = data[dname.ALTITUDE_SEALEVEL]

    if altitude < 10:
        return True
    else:
        return False
```

のような関数を定義する必要があるということです．
この関数を用いると以下のように過去のデータから関数をシミュレート出来ます．

```python
from pisat.test.core.util import simulate_judge_from

def judge_testnode(data):
    altitude = data[dname.ALTITUDE_SEALEVEL]

    if altitude < 10:
        return True
    else:
        return False

if __name__ == "__main__":
    csv_file = "xxxxxxxx.csv"

    # フラグが検知されたデータのインデックス (行数) を返す
    # 第1引数 --> Node.judge に相当する関数
    # 第2引数 --> 自身を指すフラグ値
    # 第3引数 --> csv ファイルのパス
    # 第4引数 --> csv ファイルのデータ名 (オプション)
    index_flag_detected = simulate_judge_from(judge_testnode, False, csv_file)
```

*simulate_judge_from* 関数の第4引数はオプションですが，CSV ファイルの1行目にデータ名の記載がない場合や
Node.judge に相当する関数内で使用するデータ名と CSV ファイル1行目に記載されているデータ名が合わない場合などは
必ず指定する必要があります．


## まとめ

ここでは開発におけるテストとその際に必要となる依存関係の解決などの方法を述べました．
特にテストを行う前に can09 を最新にしておくために，

```
$ python local.py (Windows)
$ python _local.py (Mac or Linux)
```

を実行しておく癖を付けましょう．
