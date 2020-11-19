# トラブルシューティング

## BNO055 の出力がずっと0になる

動作モードが config モードのままかもしれません．

```python
bno055.change_operation_mode(Bno055.OperationMode.NDOF)
```

を実行してみてください．

## SAM-M8Q のデータが取れない

以下のコマンドを打ってみてください．

```
stty -F /dev/(デバイス名) -echo
```

デバイス名は基本は serial0 です．
