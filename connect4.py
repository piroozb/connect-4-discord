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

    # Methods
    def __init__(self) -> None:
        """Initialize a Board with empty (blue) circles.
        self._arr is an empty 7x6 board.
        """
        arr = _create_board()
        self._arr = arr

    def print_board(self) -> str:
        """Used to print the board with blue circles as empty areas,
        red circles as player 1 moves, and yellow circles as player 2 moves"""
        msg = ''
        for row in self._arr:
            for item in row:
                msg += board_piece[item]
            msg += '\n'
        return msg

    def is_valid_location(self, r: int, c: int):
        """Check if the section of the board is not already filled"""
        if self._arr[r][c] == '*':
            return True
        return False

    def drop_piece(self, r: int, c: int, piece):
        """Drop piece of one of the players into the board"""
        self._arr[r][c] = piece

    # for piece can use i from other function
    def winning_move(self, piece) -> bool:
        """Checks if there are any connect fours"""
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):

                # Horizontal Wins
                if c < COL_COUNT - 3:
                    if (self._arr[r][c] == self._arr[r][c + 1] == self._arr[r][
                        c + 2]
                            == self._arr[r][c + 3] == piece):
                        return True

                # Vertical Wins
                if r < ROW_COUNT - 3:
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


# Helpers
def _create_board():
    arr = [['*'] * 7 for _ in range(6)]
    return arr


if __name__ == '__main__':
    pass
