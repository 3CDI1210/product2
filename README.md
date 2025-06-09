# product2
このオセロ(リバーシ)において、石を挟んで反転させる処理を行っているのは、check_directionメソッドの部分である。
また、勝敗の個数を数える処理は、update_score_labelメソッドの部分である。

**check_directionメソッド**

処理の流れ

１．1マス先に進む

nx, ny = x + dx, y + dy：指定された方向に1マス進む。

２．whileループで進み続ける

盤面の範囲内でループし、以下の条件をチェック：

相手の石があればリストに追加
self.board[ny][nx] == 3 - player：相手の石なら tiles_to_flip に記録。

自分の石にたどり着いたら：

相手の石を1個以上挟んでいれば、合法手。

flip=True のときはその方向の相手の石を自分の色に変える。

return True でその方向が有効であると伝える。

空白マスまたは盤外に出たらbreak
石を挟めないので無効。

３．有効な方向でなければ False を返す


**update_score_labelメソッド**

処理の流れ

１．黒石の数を数える：

black_count = sum(row.count(BLACK) for row in self.board)

・self.board は 8x8 の2次元リスト。

・各 row に対して row.count(BLACK) を実行し、BLACK（=1）の数をカウント。

・全行にわたって sum(...) を取り、黒石の総数を求める。

２．白石の数を数える：

white_count = sum(row.count(WHITE) for row in self.board)

・WHITE（=2）の石も同様にカウント。

３．スコアラベルを更新：

self.score_label.config(text=f"黒: {black_count}　白: {white_count}")

ラベルのテキストに「黒: ○ 白: ○」の形式でスコアを表示。
