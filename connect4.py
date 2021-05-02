import random
from typing import List, Dict

ROW_COUNT = 6  # used to represent number of rows in a board
COL_COUNT = 7  # used to represent number of columns in a board
EMPTY = '*'  # used to represent an empty part of the board
board_piece = {EMPTY: ':blue_circle: ', 'R': ':red_circle: ',
               'Y': ':yellow_circle: '}


class Board:
    """The board for the connect 4 game
    """
    # === Private Attributes ===
    # _board:
    # The array representing the game board.
    _board: List[List[str]]

    # Methods
    def __init__(self) -> None:
        """Initialize a Board with empty (blue) circles.
        self._arr is an empty 7x6 board.
        """
        arr = [[EMPTY] * 7 for _ in range(6)]
        self._board = arr

    def print_board(self) -> str:
        """Used to print the board with blue circles as empty areas,
        red circles as player 1 moves, and yellow circles as player 2 moves"""
        msg = ''
        for row in self._board:
            for item in row:
                msg += board_piece[item]
            msg += '\n'
        return msg

    def is_valid_location(self, r: int, c: int):
        """Check if the section of the board is not already filled"""
        if self._board[r][c] == EMPTY:
            return True
        return False

    def drop_piece(self, r: int, c: int, piece: str):
        """Drop piece of one of the players into the board"""
        self._board[r][c] = piece

    # for piece can use i from other function
    def is_win(self, piece: str) -> bool:
        """Checks if there are any connect fours"""
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):

                # Horizontal Wins
                if c < COL_COUNT - 3:
                    if (self._board[r][c] == self._board[r][c + 1] == self.
                            _board[r][c + 2] == self._board[r][c + 3] == piece):
                        return True

                # Vertical Wins
                if r < ROW_COUNT - 3:
                    if self._board[r][c] == self._board[r + 1][c] == \
                            self._board[r + 2][c] == \
                            self._board[r + 3][c] == piece:
                        return True

                # Positive Diagonal Wins
                if c < COL_COUNT - 3 and r < ROW_COUNT - 3:
                    if self._board[r][c] == self._board[r + 1][c + 1] == \
                            self._board[r + 2][c + 2] == \
                            self._board[r + 3][c + 3] == piece:
                        return True

                # Negative Diagonal Wins
                if c < COL_COUNT - 3 and 3 <= r < ROW_COUNT:
                    if self._board[r][c] == self._board[r - 1][c + 1] == \
                            self._board[r - 2][c + 2] == \
                            self._board[r - 3][c + 3] == piece:
                        return True
        return False

    def score_position(self, piece: str):
        """
        Return the Score
        """
        score = 0
        # Score Horizontal
        for r in range(ROW_COUNT):
            row = self._board[r]
            for c in range(COL_COUNT - 3):
                section = row[c:c + 4]

                if section.count(piece) == 4:
                    score += 100
                elif section.count(piece) == 3 and \
                        section.count(EMPTY) == 1:
                    score += 10

        # Score Vertical
        for c in range(COL_COUNT):
            col = [self._board[r][c] for r in range(ROW_COUNT)]
            for r in range(ROW_COUNT - 3):
                section = col[r:r + 4]

                if section.count(piece) == 4:
                    score += 100
                elif section.count(piece) == 3 and \
                        section.count(EMPTY) == 1:
                    score += 10

        # Score Positive Diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COL_COUNT - 3):
                section = [self._board[r+i][c+i] for i in range(4)]

                if section.count(piece) == 4:
                    score += 100
                elif section.count(piece) == 3 and \
                        section.count(EMPTY) == 1:
                    score += 10

        # Score Negative Diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COL_COUNT - 3):
                section = [self._board[r+3-i][c+i] for i in range(4)]

                if section.count(piece) == 4:
                    score += 100
                elif section.count(piece) == 3 and \
                        section.count(EMPTY) == 1:
                    score += 10
        return score

    # def is_terminal_node(self, player_piece, ai_piece):
    #     """
    #     Return if the game is finished or if there are no valid locations left.
    #     """
    #     return self.is_win(player_piece) or \
    #            self.is_win(ai_piece) or (len(self.get_valid_locations) == 0)

    def get_valid_locations(self) -> Dict[int, int]:
        """
        Return a dict with key as column, and value as row, representing places
        the piece can be dropped into.
        """
        valid_locations = {}
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):
                if self.is_valid_location(r, c):
                    valid_locations[c] = r
        return valid_locations

    def pick_best_move(self, piece: str) -> tuple:
        """
        Return a Tuple containing the column and row for the best move.
        """
        best_score = 0
        valid_positions = self.get_valid_locations()
        rnd = random.choice(list(valid_positions.keys()))
        best_col_row = rnd, valid_positions[rnd]
        for col in valid_positions:
            temp_board = Board()
            temp_board._board = [sublist.copy() for sublist in self._board]
            row = valid_positions[col]
            temp_board.drop_piece(row, col, piece)
            score = temp_board.score_position(piece)
            if score > best_score:
                best_score = score
                best_col_row = (col, row)

        return best_col_row


if __name__ == '__main__':
    pass
