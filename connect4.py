ROW_COUNT = 6
COL_COUNT = 7


def create_board():
    arr = [['*']*7]*6
    return arr


# for piece can use i from other function
def winning_move(board, piece):

    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if c <= COL_COUNT - 3:
                # Horizontal WINS
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


def empty_board(arr):
    for i in range(len(arr)):
        arr[i] = "*"


def print_board(arr):
    pass
    # printed = 0
    # str = ''
    # for i in arr:
    #     str += i + " "
    #     printed += 1
    #     if printed == COL_COUNT:
    #         print(str)
    #         printed = 0
    #         str = ''
    # print("\n")


def drop_piece(arr, r, c, piece):
    arr[r][c] = piece


def is_valid_location(board, col):
    if board[col] == '*':
        return True
    return False
