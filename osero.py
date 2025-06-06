import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 8
CELL_SIZE = 60
EMPTY, BLACK, WHITE = 0, 1, 2

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("オセロ")
        self.show_menu()

    def show_menu(self):
        self.clear_widgets()
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=40)

        title = tk.Label(self.menu_frame, text="オセロ - モード選択", font=("Arial", 20))
        title.pack(pady=20)

        btn1 = tk.Button(self.menu_frame, text="プレイヤー vs プレイヤー", font=("Arial", 14), width=25,
                         command=lambda: self.start_game(vs_ai=False))
        btn1.pack(pady=10)

        btn2 = tk.Button(self.menu_frame, text="プレイヤー vs コンピュータ", font=("Arial", 14), width=25,
                         command=lambda: self.start_game(vs_ai=True))
        btn2.pack(pady=10)

    def start_game(self, vs_ai):
        self.clear_widgets()
        self.game = OthelloGame(self.root, vs_ai, back_to_menu=self.show_menu)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class OthelloGame:
    def __init__(self, master, vs_ai, back_to_menu):
        self.master = master
        self.vs_ai = vs_ai
        self.back_to_menu = back_to_menu

        self.turn_label = tk.Label(master, text="", font=("Arial", 16))
        self.turn_label.pack()

        self.score_label = tk.Label(master, text="", font=("Arial", 14))
        self.score_label.pack()

        self.restart_button = tk.Button(master, text="リスタート", font=("Arial", 12), command=self.restart_game)
        self.restart_button.pack(pady=5)

        self.back_button = tk.Button(master, text="メニューに戻る", font=("Arial", 12), command=self.back_to_menu)
        self.back_button.pack(pady=2)

        self.canvas = tk.Canvas(master, width=BOARD_SIZE*CELL_SIZE, height=BOARD_SIZE*CELL_SIZE, bg='green')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = BLACK
        self.init_board()
        self.update_turn_label()
        self.update_score_label()
        self.draw_board()

    def init_board(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                self.board[y][x] = EMPTY
        mid = BOARD_SIZE // 2
        self.board[mid-1][mid-1] = WHITE
        self.board[mid][mid] = WHITE
        self.board[mid-1][mid] = BLACK
        self.board[mid][mid-1] = BLACK

    def draw_board(self):
        self.canvas.delete("all")
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                x1 = x * CELL_SIZE
                y1 = y * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

                if self.board[y][x] == BLACK:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="black")
                elif self.board[y][x] == WHITE:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="white")
                elif self.is_valid_move(x, y, self.current_player):
                    # 合法手のハイライト
                    self.canvas.create_oval(x1+15, y1+15, x2-15, y2-15, fill="yellow", outline="")

    def handle_click(self, event):
        if self.vs_ai and self.current_player == WHITE:
            return
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if self.is_valid_move(x, y, self.current_player):
            self.make_move(x, y, self.current_player)
            self.draw_board()
            self.update_score_label()
            self.switch_turn()
        else:
            messagebox.showinfo("無効な手", "その場所には置けません")

    def switch_turn(self):
        opponent = 3 - self.current_player
        if self.has_valid_moves(opponent):
            self.current_player = opponent
            self.update_turn_label()
            if self.vs_ai and self.current_player == WHITE:
                self.master.after(500, self.make_ai_move)
        elif self.has_valid_moves(self.current_player):
            messagebox.showinfo("パス", "相手は置けないためパスします")
        else:
            self.end_game()
        self.update_score_label()
        self.draw_board()

    def make_ai_move(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.is_valid_move(x, y, WHITE):
                    self.make_move(x, y, WHITE)
                    self.draw_board()
                    self.update_score_label()
                    self.switch_turn()
                    return
        # AIに有効な手がない → パス処理
        messagebox.showinfo("パス", "AIは置けないためパスします")
        self.switch_turn()

    def end_game(self):
        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)
        if black_count > white_count:
            winner = "黒の勝ち！"
        elif white_count > black_count:
            winner = "白の勝ち！"
        else:
            winner = "引き分け！"
        messagebox.showinfo("ゲーム終了", f"黒: {black_count} 白: {white_count}\n{winner}")

    def is_valid_move(self, x, y, player):
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            return False
        if self.board[y][x] != EMPTY:
            return False
        return any(self.check_direction(x, y, dx, dy, player, flip=False) for dx, dy in self.directions())

    def make_move(self, x, y, player):
        self.board[y][x] = player
        for dx, dy in self.directions():
            self.check_direction(x, y, dx, dy, player, flip=True)

    def check_direction(self, x, y, dx, dy, player, flip):
        nx, ny = x + dx, y + dy
        tiles_to_flip = []
        while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            if self.board[ny][nx] == 3 - player:
                tiles_to_flip.append((nx, ny))
            elif self.board[ny][nx] == player:
                if flip:
                    for fx, fy in tiles_to_flip:
                        self.board[fy][fx] = player
                return len(tiles_to_flip) > 0
            else:
                break
            nx += dx
            ny += dy
        return False

    def has_valid_moves(self, player):
        return any(self.is_valid_move(x, y, player)
                   for y in range(BOARD_SIZE) for x in range(BOARD_SIZE))

    def update_turn_label(self):
        if self.vs_ai:
            name = "黒（あなた）" if self.current_player == BLACK else "白（AI）"
        else:
            name = "黒" if self.current_player == BLACK else "白"
        self.turn_label.config(text=f"現在のターン：{name}")

    def update_score_label(self):
        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)
        self.score_label.config(text=f"黒: {black_count}　白: {white_count}")

    def restart_game(self):
        self.current_player = BLACK
        self.init_board()
        self.update_turn_label()
        self.update_score_label()
        self.draw_board()

    def directions(self):
        return [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()




