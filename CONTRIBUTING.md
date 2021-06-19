# Contribution Guide

本プロジェクトのコントリビューションガイドです．

## Git 開発フロー

Git を使った開発フローは [Branching Model](https://nvie.com/posts/a-successful-git-branching-model/) を採用しています．

### The main branches

このモデルでは2つの軸となるブランチが存在します:

- master
- develop

この2つのブランチの共通点はブランチが消滅することがないという点です．一方で相違点はその役割であり，**master は現在プロダクトとしてリリースされているブランチ**を指しており，**develop は次期リリースされるバージョンを開発するブランチ**を指しています．また，master のリリースはバージョン番号によってタグ付けされ，本プロジェクトでは `x.x.x` の3つのバージョンでタグ付けを行います．それぞれ，**メジャー番号**，**マイナー番号**，**パッチ番号**と呼ぶことにし，develop ブランチは次のマイナー番号またはメジャー番号を持つバージョンの開発を行います．

### Supporting branches

また，このモデルには3種類の副次的なブランチが設けられています:

- feature
- release
- hotfix

第一に，feature ブランチは新たな機能を実装する際に作られるブランチです．このブランチは `Feature request` という名前で提出された issue によってのみ発生する可能性があります（必要ないと判断されれば発生しません）．したがって，このブランチは issue 番号によって一意に識別可能であり，それを示すために `feature-issXXX` （`XXX` は issue 番号）という命名規則によって名付けられます．このブランチは開発終了後，リポジトリ管理者への Pull request によって develop ブランチへとマージされます．マージ後，feature ブランチは削除されます．

release ブランチは master ブランチへのマージによってリリースされる前段階を設けるために作成されるブランチです．このブランチでは主にテストを中心に行い，場合によっては発見されたバグの修正などが行われます．そしてデプロイ可能状態であるとみなされた場合，master ブランチへとマージされます．また，同時に develop ブランチへもマージされます（これは release ブランチ上で行われたバグ修正などのコミットの内容を反映させるためです）．この2つのブランチへのマージが終了すると，release ブランチは削除されます．また，release ブランチは次期バージョン番号によって一意に識別することが可能です．したがって，release ブランチは `release-x.x` の命名規則によって名付けられます．ただし，ここではマイナー番号までのバージョン番号を表示するという点に注意してください．これは，master ブランチのバグ修正は develop ブランチでは行わないためであり，release ブランチのマージによるアップグレードは常に何らかの新機能や機能修正を伴っているためです．

最後に，hotfix ブランチは master ブランチで発見されたバグを修正するためだけに作成されるブランチです．このブランチは `Bug report` という名前で提出された issue によってのみ発生する可能性があります．したがって，このブランチは issue 番号によって一意に識別可能であり，それを示すために `hotfix-issXXX`（`XXX` は issue 番号）という命名規則によって名付けられます．このブランチはバグの修正完了後，master ブランチ，develop ブランチの両方へマージされます．マージ後，hotfix ブランチは削除されます．

## Issues

新たな issue はテンプレートを利用して発行してください．issue 発行後，その種類によって feature ブランチまたは hotfix ブランチが作成されます．

- バグについての報告    --> [こちら](https://github.com/FROM-THE-EARTH/canbeta/issues/new?template=bug_report.md)
- 新しい機能などの提案  --> [こちら](https://github.com/FROM-THE-EARTH/canbeta/issues/new?template=feature_request.md)

## Pull Request

本プロジェクトでは **feature, release, hotfix ブランチを master, develop ブランチへ Pull request なしにマージすることを禁じます**．したがって，あるブランチでの開発が終了しマージを希望する場合は Pull request を行ってください．Pull request にはテンプレートが用意されているので，必要事項を記入の上でリクエストを行ってください．リクエストの承認はリポジトリ管理者によって行われます．

## Commits

本プロジェクトではコミットメッセージについてもテンプレートを用意しています（[.gitmessage ファイル](.gitmessage)）．このテンプレートをローカルリポジトリで登録するために，ローカルリポジトリ下で以下のコマンドを実行してください:

```
git config commit.template .gitmessage
```

コミット時には以下のコマンドを実行して，テンプレートに従ってコミットメッセージを記入してください:

```
git commit
```

上記コマンドを実行するとエディタが起動し，コミットメッセージを記入できるようになりますが，起動するエディタは以下のようにして変更することが出来ます:

```
git config [--global] core.editor [vim / emacs]
```