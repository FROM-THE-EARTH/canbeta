# トラブルシューティング

## BNO055 の出力がずっと0になる

動作モードが config モードのままかもしれません．

```python
bno055.change_operation_mode(Bno055.OperationMode.NDOF)
```

を実行してみてください．

## シリアル通信が出来ない

デバイスファイルを読み書きする権限が付与されていない可能性があります．以下のコマンドを実行してみてください．

```
$ sudo chmod 777 (デバイス名)
```

## SAM-M8Q のデータが取れない

以下のコマンドを打ってみてください．

```
$ stty -F /dev/(デバイス名) -echo
```

デバイス名は基本は serial0 です．

## IM920 が動作しない (1)

ボーレートが合っていない可能性があります．IM920 のボーレートは19200Hzです．handler を19200Hzのボーレートで初期化して使用してください．

```python
from pisat.handler import PyserialSerialHandler
from pisat.comm.transceiver import Im920

handler = PyserialSerialHandler("/dev/ttyUSB0", boadrate=19200)
im920 = Im920(handler)
```

## IM920 が動作しない (2)

ペアリングが行われていない可能性があります．IM920 にはIDがあり，裏側に書いてある6桁の数字がIDです．相手側のIDを登録しておかないと受信を行うことが出来ません．

6桁の数字のIDの登録方法には2通りあります．1つ目の方法は数字を16進数に直して登録する方法です．

```python
# ID: 007378
# -> 16進数: 1CD2
im920.add_rec_id("1CD2")
```

2つ目の方法は6桁の数字を直接渡し，is_hex 引数を True に設定する方法です．この方法が計算しなくても出来るので簡単です．

```python
# ID: 007378
im920.add_rec_id("007378", is_hex=True)
```
