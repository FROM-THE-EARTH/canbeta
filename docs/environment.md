# 環境構築

## Python

まずは PC 内で開発を行うための環境構築を行ってください．
開発で使用するのは **Python 3.7** です．
もし，Python 3.7 以外のバージョンしかインストールされていない場合は
pyenv などを利用し Python 3.7 を使用できる環境を整えてください．
別のバージョンが存在したとしても，特に削除する必要はありません．

### pyenv 

以下のサイトを参考に pyenv をインストールし，Python のバージョン管理を出来るようにしてください．

- [Windows](https://obataka.com/create-windows-python-virtualenv/)
- [Mac](https://qiita.com/koooooo/items/b21d87ffe2b56d0c589b)
- [Linux](https://qiita.com/neruoneru/items/1107bcdca7fa43de673d)

### pipenv

pipenv は Python の仮想環境を構築し，外部ライブラリの依存関係をその中に整理するために使用するツールです．
インストールは

```
$ pip install pipenv
```

で出来ます ($ はコマンドを示すための単なる記号で入力しなくていいです)．
pipenv がインストール出来たら，clone してある fte-can09 リポジトリのルート(ディレクトリの最上部) で

```
$ pipenv install
```

をすると仮想環境を構築し，fte-can09/Pipenv に定義してある外部ライブラリをインストール出来ます．
**Pipfile** はそのプロジェクトの環境の全てが記載されているファイルです．
Pipfile さえあれば，pipenv を用いていつでも容易に環境構築が可能です．

その他の pipenv の使用方法は[こちら](https://qiita.com/y-tsutsu/items/54c10e0b2c6b565c887a)を参照してください．

### VS Code の設定

エディタは VS Code を利用することを推奨しています．
拡張機能についての制限は特に行っていません．

VS Code では構文解析を行う Python インタープリタを指定することが出来ます．
今回は pipenv で仮想環境を構築したので，その環境でのインタープリタを使用します．
まず，Python スクリプトを開いている状態で，VS Code の画面下の青いバーの左側にある Python... という項目をクリックします．
その後，画面上部中央に利用可能な Python インタプリタがリストされると思いますが，
そこで fte-can09 の名前を含むものを選択します．
すると，編集している Python スクリプトがその仮想環境内で使用している外部ライブラリなどをもとに解析されるので，
インポートエラーのような表示が出なくなります．

### 環境構築における注意点

- pipenv で勝手に他の外部ライブラリをインストールしないでください
- 外部ライブラリが必要になるようであれば，MTG で相談してください
- わからないことがあったら積極的に聞いてください

## Raspberry Pi

### SD

Raspberry Pi 用の SD カードの作成は [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) を使用すると楽です．
OS は Raspberry Pi OS を選択してください．

### Python

Raspberry Pi における Python の環境構築は PC での環境構築方法と同一です．
pipenv は環境構築のために使うので必ずインストールしておいてください．
VS Code は今のところ公式でサポートされていないのでインストールしなくても大丈夫です．

Raspberry Pi をインストールしたての状態では，ターミナル上で

```
$ python
```

と打つと Python 2系が起動されます．Python 3系を起動するためには

```
$ python3
```

と打つ必要があります．
面倒な場合はエイリアスを作成する方法があります．

### Git

Git はデフォルトでインストールされていないかもしれないのでインストールしておきましょう．
ターミナルで，

```
$ sudo apt install git
```

と打てばインストール出来ます．
ユーザー名と E-mail アドレスの設定なども行っておきましょう．

Git のセットアップが出来たら，このリポジトリをクローンしてください．

```
$ git clone https://github.com/jjj999/fte-can09.git
```

クローンし終わったらそのリポジトリのルートに移動し，Python の環境構築を行うために

```
$ pipenv install
```

をします．
これで PC と Raspberry Pi の Python に関する環境が同期されます．

## まとめ

今回のプロジェクトで環境構築が必要なデバイスは

- PC
- Raspberry Pi

の2つです．
また，それぞれの環境を出来るだけ近いものにするために **pipenv** を用います．
環境構築は面倒ですが，一度理解してしまえば単純作業です．

環境構築のためのツールとして，今回のプロジェクトでは

- pyenv
- pipenv
- Git

を利用します．
重要な点は Pipfile さえあれば pipenv で Python の環境構築がほぼ終わるということです．

[次のドキュメント](./development.md)では開発の流れについて説明します．
