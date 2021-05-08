import random
from typing import List, Dict
import math

ROW_COUNT = 6  # used to represent number of rows in a board
COL_COUNT = 7  # used to represent number of columns in a board
EMPTY = '*'  # used to represent an empty part of the board
board_piece = {EMPTY: ':blue_circle: ', 'R': ':red_circle: ',
               'Y': ':yellow_circle: '}
PLAYER_PIECE = 'R'
AI_PIECE = 'Y'


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
        Return the Score of the position.
        """
        score = 0
        # Score center column
        center_list = [self._board[r][COL_COUNT // 2] for r in range(ROW_COUNT)]
        center_count = center_list.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(ROW_COUNT):
            row = self._board[r]
            for c in range(COL_COUNT - 3):
                section = row[c:c + 4]
                score += evaluate_section(section, piece)

        # Score Vertical
        for c in range(COL_COUNT):
            col = [self._board[r][c] for r in range(ROW_COUNT)]
            for r in range(ROW_COUNT - 3):
                section = col[r:r + 4]
                score += evaluate_section(section, piece)

        # Score Positive Diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COL_COUNT - 3):
                section = [self._board[r + i][c + i] for i in range(4)]
                score += evaluate_section(section, piece)

        # Score Negative Diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COL_COUNT - 3):
                section = [self._board[r + 3 - i][c + i] for i in range(4)]
                score += evaluate_section(section, piece)
        return score

    def is_terminal_node(self) -> bool:
        """
        Return if the game is finished or if there are no valid locations left.
        """
        return self.is_win(PLAYER_PIECE) or \
            self.is_win(AI_PIECE) or (len(self.get_valid_locations()) == 0)

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

    def minimax(self, depth, alpha, beta, maximizing_player) -> tuple:
        valid_locations = self.get_valid_locations()
        is_terminal = self.is_terminal_node()
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.is_win(AI_PIECE):
                    return None, 100000000000000
                elif self.is_win(PLAYER_PIECE):
                    return None, -10000000000000
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, self.score_position(AI_PIECE)

        if maximizing_player:  # Maximizing player (for bot turn)
            value = -math.inf
            column = random.choice(list(valid_locations.keys()))
            for col in valid_locations:
                row = valid_locations[col]
                temp_board = Board()
                temp_board._board = [sublist.copy() for sublist in self._board]
                temp_board.drop_piece(row, col, AI_PIECE)
                new_score = temp_board.minimax(depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player (for player turn)
            value = math.inf
            column = random.choice(list(valid_locations.keys()))
            for col in valid_locations:
                row = valid_locations[col]
                temp_board = Board()
                temp_board._board = [sublist.copy() for sublist in self._board]
                temp_board.drop_piece(row, col, PLAYER_PIECE)
                new_score = temp_board.minimax(depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value


# Helper
def evaluate_section(section: list, piece: str) -> int:
    """Evaluates the score of a specific section on the board based on
    how close the section is to giving a connect 4"""
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if section.count(piece) == 4:
        score += 10000
    elif section.count(piece) == 3 and section.count(EMPTY) == 1:
        score += 10
    elif section.count(piece) == 2 and section.count(EMPTY) == 2:
        score += 5

    if section.count(opp_piece) == 3 and section.count(EMPTY) == 1:
        score -= 8
    elif section.count(opp_piece) == 4:
        score -= 8000

    return score


if __name__ == '__main__':
    pass
