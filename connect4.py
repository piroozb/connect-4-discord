"""
This file contains functions related to the connect 4 game and board.
"""
from typing import List

ROW_COUNT = 6
COL_COUNT = 7
board_piece = {'*': ':blue_circle: ', 'R': ':red_circle: ',
               'Y': ':yellow_circle: '}


class Board:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    """
    # === Private Attributes ===
    # The array representing the game board.
    _arr: List[str]

    # === Representation Invariants ===
    # - If arr is None then self._arr is an empty 7x6 board.

    # Methods
    def __init__(self) -> None:
        """Initialize a Board with empty (blue) circles.
        self._arr is an empty 7x6 board.
        >>> b = Board()
        >>> b._arr
        [['*', '*', '*', '*','*', '*', '*'],
        ['*', '*', '*', '*','*', '*', '*'],
        ['*', '*', '*', '*','*', '*', '*'],
        ['*', '*', '*', '*','*', '*', '*'],
        ['*', '*', '*', '*','*', '*', '*'],
        ['*', '*', '*', '*','*', '*', '*'],]
        """
        arr = _create_board()
        self._arr = arr

    def empty_board(self):
        for i in range(len(self._arr)):
            self._arr[i] = "*"

    def print_board(self) -> str:
        msg = ''
        for row in self._arr:
            for item in row:
                msg += board_piece[item]
            msg += '\n'
        return msg

    def drop_piece(self, r: int, c: int, piece):
        self._arr[r][c] = piece

    def is_valid_location(self, col):
        if self._arr[col] == '*':
            return True
        return False

    # for piece can use i from other function
    def winning_move(self, piece) -> bool:
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):
                if c <= COL_COUNT - 3:
                    # Horizontal Wins
                    if (self._arr[r][c] == self._arr[r][c + 1] == self._arr[r][
                        c + 2]
                            == self._arr[r][c + 3] == piece):
                        return True

                if r <= ROW_COUNT - 3:
                    # Vertical Wins
                    if self._arr[r][c] == self._arr[r + 1][c] == \
                            self._arr[r + 2][c] == \
                            self._arr[r + 3][c] == piece:
                        return True

                # Positive Diagonal Wins
                if c <= COL_COUNT - 3 and r <= ROW_COUNT - 3:
                    if self._arr[r][c] == self._arr[r + 1][c + 1] == \
                            self._arr[r + 2][c + 2] == \
                            self._arr[r + 3][c + 3] == piece:
                        return True

                # Negative Diagonal Wins
                if c <= COL_COUNT - 3 and 3 <= r < ROW_COUNT:
                    if self._arr[r][c] == self._arr[r - 1][c + 1] == \
                            self._arr[r - 2][c + 2] == \
                            self._arr[r - 3][c + 3] == piece:
                        return True
        return False

    def current_row(self) -> int:
        """

        :return: Current row the board is at, which is len of list.
        """
        return self._arr.__len__()

# Helpers
def _create_board():
    arr = [['*'] * 7] * 6
    return arr
