# -*- coding: utf-8 -*-
"""
五目ならべのGUIインターフェース
"""

import tkinter as tk
from tkinter import messagebox, font as tkfont
from gomoku_game import GomokuGame
import os

# Xftフォントレンダリングを有効化
os.environ.setdefault('TK_AALIAS', '1')


class GomokuGUI:
    """五目ならべのGUIを管理するクラス"""

    def __init__(self, master, board_size=15):
        """
        初期化

        Args:
            master: Tkinterのルートウィンドウ
            board_size (int): ボードのサイズ
        """
        self.master = master

        # Tclのエンコーディングを明示的にUTF-8に設定
        self.master.tk.call('encoding', 'system', 'utf-8')

        self.master.title("Gomoku - Five in a Row")

        # UTF-8エンコーディングを設定
        self.master.option_add('*font', 'TkDefaultFont')

        self.board_size = board_size
        self.cell_size = 40  # セルのサイズ（ピクセル）
        self.game = GomokuGame(board_size)

        # 日本語対応フォントを選択
        self.jp_font = self._get_japanese_font()

        # デフォルトフォントを設定
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(size=10)
        text_font = tkfont.nametofont("TkTextFont")
        text_font.configure(size=10)

        # キャンバスの作成
        canvas_size = self.cell_size * (self.board_size + 1)
        self.canvas = tk.Canvas(
            master,
            width=canvas_size,
            height=canvas_size,
            bg="burlywood"
        )
        self.canvas.pack()

        # ボタンフレームの作成
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        # リセットボタン
        reset_button = tk.Button(
            button_frame,
            text="新しいゲーム",
            command=self.reset_game,
            font=(self.jp_font, 12)
        )
        reset_button.pack(side=tk.LEFT, padx=5)

        # 終了ボタン
        quit_button = tk.Button(
            button_frame,
            text="終了",
            command=master.quit,
            font=(self.jp_font, 12)
        )
        quit_button.pack(side=tk.LEFT, padx=5)

        # ステータスラベル
        self.status_label = tk.Label(
            master,
            text="黒の番です",
            font=(self.jp_font, 14, "bold")
        )
        self.status_label.pack(pady=5)

        # イベントバインディング
        self.canvas.bind("<Button-1>", self.on_click)

        # ボードを描画
        self.draw_board()

    def _get_japanese_font(self):
        """日本語をサポートするフォントを選択"""
        # まずfontconfigから日本語フォントを取得
        try:
            import subprocess
            result = subprocess.run(['fc-match', '-f', '%{family}', ':lang=ja'],
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout:
                fc_font = result.stdout.strip().split(',')[0]
                # Tkinterが認識していなくても、Xftが使えるはずなので返す
                return fc_font
        except Exception:
            pass

        # fontconfigが失敗した場合、優先順位でフォントを選択
        available_fonts = list(tkfont.families())
        preferred_fonts = [
            'Noto Sans CJK JP',
            'Noto Serif CJK JP',
            'Noto Sans CJK',
            'Noto Sans',
            'DejaVu Sans',
            'TkDefaultFont',
            'fixed'  # X11のデフォルトフォント
        ]

        for font_name in preferred_fonts:
            if font_name in available_fonts:
                return font_name

        # どれも見つからない場合は空文字列（システムデフォルト）
        return ''

    def draw_board(self):
        """ボードを描画"""
        self.canvas.delete("all")

        # グリッド線を描画
        for i in range(self.board_size):
            # 横線
            self.canvas.create_line(
                self.cell_size,
                self.cell_size * (i + 1),
                self.cell_size * self.board_size,
                self.cell_size * (i + 1)
            )
            # 縦線
            self.canvas.create_line(
                self.cell_size * (i + 1),
                self.cell_size,
                self.cell_size * (i + 1),
                self.cell_size * self.board_size
            )

        # 星（天元など）を描画
        star_positions = []
        if self.board_size == 15:
            star_positions = [
                (3, 3), (3, 11), (11, 3), (11, 11),
                (7, 7), (3, 7), (11, 7), (7, 3), (7, 11)
            ]
        elif self.board_size == 19:
            star_positions = [
                (3, 3), (3, 9), (3, 15),
                (9, 3), (9, 9), (9, 15),
                (15, 3), (15, 9), (15, 15)
            ]

        for row, col in star_positions:
            x = self.cell_size * (col + 1)
            y = self.cell_size * (row + 1)
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

        # 石を描画
        board = self.game.get_board()
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] != 0:
                    self.draw_stone(row, col, board[row][col])

    def draw_stone(self, row, col, player):
        """
        石を描画

        Args:
            row (int): 行番号
            col (int): 列番号
            player (int): プレイヤー番号（1: 黒, 2: 白）
        """
        x = self.cell_size * (col + 1)
        y = self.cell_size * (row + 1)
        radius = self.cell_size // 2 - 2

        color = "black" if player == 1 else "white"
        outline = "black"

        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color,
            outline=outline,
            width=2
        )

    def on_click(self, event):
        """
        クリックイベント処理

        Args:
            event: クリックイベント
        """
        if self.game.is_game_over():
            return

        # クリック位置から行列を計算
        col = round((event.x - self.cell_size) / self.cell_size)
        row = round((event.y - self.cell_size) / self.cell_size)

        # 石を置く
        if self.game.place_stone(row, col):
            self.draw_board()

            if self.game.is_game_over():
                winner = self.game.get_winner()
                winner_name = "黒" if winner == 1 else "白"
                self.status_label.config(text=f"{winner_name}の勝利!")
                messagebox.showinfo("ゲーム終了", f"{winner_name}の勝利です！")
            else:
                current_player = self.game.get_current_player()
                player_name = "黒" if current_player == 1 else "白"
                self.status_label.config(text=f"{player_name}の番です")

    def reset_game(self):
        """ゲームをリセット"""
        self.game.reset()
        self.draw_board()
        self.status_label.config(text="黒の番です")


def main():
    """メイン関数"""
    root = tk.Tk()
    app = GomokuGUI(root, board_size=15)
    root.mainloop()


if __name__ == "__main__":
    main()
