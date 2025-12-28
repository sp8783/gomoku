# -*- coding: utf-8 -*-
"""
五目ならべのゲームロジック
"""


class GomokuGame:
    """五目ならべゲームのロジックを管理するクラス"""

    def __init__(self, board_size=15):
        """
        初期化

        Args:
            board_size (int): ボードのサイズ（デフォルト15x15）
        """
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 1  # 1: 黒石, 2: 白石
        self.game_over = False
        self.winner = None

    def reset(self):
        """ゲームをリセット"""
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 1
        self.game_over = False
        self.winner = None

    def place_stone(self, row, col):
        """
        石を置く

        Args:
            row (int): 行番号
            col (int): 列番号

        Returns:
            bool: 石を置けた場合True、置けなかった場合False
        """
        if self.game_over:
            return False

        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            return False

        if self.board[row][col] != 0:
            return False

        self.board[row][col] = self.current_player

        if self.check_winner(row, col):
            self.game_over = True
            self.winner = self.current_player
        else:
            self.current_player = 3 - self.current_player  # 1→2, 2→1

        return True

    def check_winner(self, row, col):
        """
        勝敗判定（最後に置いた石の周りをチェック）

        Args:
            row (int): 最後に置いた石の行番号
            col (int): 最後に置いた石の列番号

        Returns:
            bool: 勝利条件を満たす場合True
        """
        player = self.board[row][col]

        # 8方向をチェック
        directions = [
            (0, 1),   # 横
            (1, 0),   # 縦
            (1, 1),   # 斜め右下
            (1, -1),  # 斜め左下
        ]

        for dx, dy in directions:
            count = 1

            # 正方向にカウント
            for i in range(1, 5):
                new_row = row + dx * i
                new_col = col + dy * i
                if (0 <= new_row < self.board_size and
                    0 <= new_col < self.board_size and
                    self.board[new_row][new_col] == player):
                    count += 1
                else:
                    break

            # 負方向にカウント
            for i in range(1, 5):
                new_row = row - dx * i
                new_col = col - dy * i
                if (0 <= new_row < self.board_size and
                    0 <= new_col < self.board_size and
                    self.board[new_row][new_col] == player):
                    count += 1
                else:
                    break

            if count >= 5:
                return True

        return False

    def get_board(self):
        """ボードの状態を取得"""
        return self.board

    def get_current_player(self):
        """現在のプレイヤーを取得"""
        return self.current_player

    def is_game_over(self):
        """ゲーム終了判定"""
        return self.game_over

    def get_winner(self):
        """勝者を取得"""
        return self.winner
