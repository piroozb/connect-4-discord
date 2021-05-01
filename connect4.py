"""
This file contains functions related to the connect 4 game and board.
"""
from typing import List

ROW_COUNT = 6
COL_COUNT = 7
board_piece = {'*': ':blue_circle: ', 'R': ':red_circle: ',
               'Y': ':yellow_circle: '}


def create_board():
    arr = [['*']*7]*6
    return arr


# for piece can use i from other function
def winning_move(board, piece) -> bool:

    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if c <= COL_COUNT - 3:
                # Horizontal Wins
                if (board[r][c] == board[r][c+1] == board[r][c+2]
                        == board[r][c+3] == piece):
                    return True

            if r <= ROW_COUNT - 3:
                # Vertical Wins
                if board[r][c] == board[r+1][c] == board[r+2][c] == \
                        board[r+3][c] == piece:
                    return True

            # Positive Diagonal Wins
            if c <= COL_COUNT - 3 and r <= ROW_COUNT - 3:
                if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == \
                        board[r+3][c+3] == piece:
                    return True

            # Negative Diagonal Wins
            if c <= COL_COUNT - 3 and 3 <= r < ROW_COUNT:
                if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == \
                        board[r-3][c+3] == piece:
                    return True
    return False


def empty_board(arr):
    for i in range(len(arr)):
        arr[i] = "*"


def print_board(board: List[list]) -> str:
    msg = ''
    for row in board:
        for item in row:
            msg += board_piece[item]
        msg += '\n'
    return msg


def drop_piece(arr, r, c, piece):
    arr[r][c] = piece


def is_valid_location(board, col):
    if board[col] == '*':
        return True
    return False
