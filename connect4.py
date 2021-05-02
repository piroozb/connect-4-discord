"""
This file contains functions related to the connect 4 game and board.
"""
from typing import List

ROW_COUNT = 6
COL_COUNT = 7
board_piece = {'*': ':blue_circle: ', 'R': ':red_circle: ',
               'Y': ':yellow_circle: '}


class Board:
    """The board for the connect 4 game
    """
    # === Private Attributes ===
    # The array representing the game board.
    _arr: List[List[str]]

    # === Representation Invariants ===
    # - If arr is None then self._arr is an empty 7x6 board.

    # Methods
    def __init__(self) -> None:
        """Initialize a Board with empty (blue) circles.
        self._arr is an empty 7x6 board.
        """
        arr = _create_board()
        self._arr = arr

    def print_board(self) -> str:
        msg = ''
        for row in self._arr:
            for item in row:
                msg += board_piece[item]
            msg += '\n'
        return msg

    def is_valid_location(self, r: int, c: int):
        if self._arr[r][c] == '*':
            return True
        return False

    def drop_piece(self, r: int, c: int, piece):
        self._arr[r][c] = piece

    # for piece can use i from other function
    def winning_move(self, piece) -> bool:
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):
                if c < COL_COUNT - 3:
                    # Horizontal Wins
                    if (self._arr[r][c] == self._arr[r][c + 1] == self._arr[r][
                        c + 2]
                            == self._arr[r][c + 3] == piece):
                        return True

                if r < ROW_COUNT - 3:
                    # Vertical Wins
                    if self._arr[r][c] == self._arr[r + 1][c] == \
                            self._arr[r + 2][c] == \
                            self._arr[r + 3][c] == piece:
                        return True

                # Positive Diagonal Wins
                if c < COL_COUNT - 3 and r < ROW_COUNT - 3:
                    if self._arr[r][c] == self._arr[r + 1][c + 1] == \
                            self._arr[r + 2][c + 2] == \
                            self._arr[r + 3][c + 3] == piece:
                        return True

                # Negative Diagonal Wins
                if c < COL_COUNT - 3 and 3 <= r < ROW_COUNT:
                    if self._arr[r][c] == self._arr[r - 1][c + 1] == \
                            self._arr[r - 2][c + 2] == \
                            self._arr[r - 3][c + 3] == piece:
                        return True
        return False

    def current_row(self) -> int:
        """
        Current row the board is at, which is len of list.
        """
        return self._arr.__len__()


# Helpers
def _create_board():
    arr = [['*'] * 7 for _ in range(6)]
    return arr


if __name__ == '__main__':
    pass