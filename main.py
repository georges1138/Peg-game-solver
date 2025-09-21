from dataclasses import dataclass
from typing import ClassVar, Tuple, Literal
import time

"""
This Python program solves the Peg Board game.  The user will initialing pick the first empty hole on the board,
then the program will transverse the valid moves until only one peg is left.  It uses the Depth-First search algorithm
to track each move and to reverse if an unsuccessful finish is reached.
"""

@dataclass(slots=True)
class Peg:
    number: int
    moves: list[Tuple]


class Board:
    # Class variable that holds the move rules for each position on the peg board.
    rules: ClassVar[list[list[Tuple]]] = [
        [(4, 2), (6, 3)],
        [(7, 4), (9, 5)],
        [(8, 5), (10, 6)],
        [(1, 2), (6, 5), (11, 7), (13, 8)],
        [(12, 8), (14, 9)],
        [(1, 3), (4, 5), (13, 9), (15, 10)],
        [(2, 4), (9, 8)],
        [(3, 5), (10, 9)],
        [(2, 5), (7, 8)],
        [(3, 6), (8, 9)],
        [(4, 7), (13, 12)],
        [(5, 8), (14, 13)],
        [(4, 8), (6, 9), (11, 12), (15, 14)],
        [(5, 9), (12, 13)],
        [(6, 10), (13, 14)]
    ]

    def __init__(self):
        self.markers = ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X']
        self.all_pegs = []

        for i, r in enumerate(Board.rules, start=1):
            self.all_pegs.append(Peg(i, r))


def first_peg_position() -> Literal[1, 4, 5, 6, 13] | None:
    """
    Function that will take a user's input as the first empty peg hole.
    :return:
    """
    while True:
        try:
            first_hole = int(input("Please enter the starting hole: "))
        except ValueError:
            print("Invalid entry.  Please enter a number: 1, 4, 5, 6, or 13:")
            continue

        if first_hole not in (1, 4, 5, 6, 13):
            print("Invalid starting hole.  Please enter a number: 1, 4, 5, 6, or 13:")
            continue
        print(f"Confirmed: Starting at position: {first_hole}")
        return first_hole


def transverse_board(board, pos, moves) -> None:
    """
    This is the recursive function that will do a depth-first search approach to solve the
    Peg board game.

    :param board:
    :param pos:
    :param moves:
    :return:
    """
    # check base case
    if check_finish(board):
        return

    # get the moves from current position
    for i, (m, current_peg) in enumerate(zip(board.markers, board.all_pegs)):
        if m == 'O':
            # If space is open, check every valid move...
            for j in range(len(current_peg.moves)):
                x, y = current_peg.moves[j]

                # Make sure there are pegs
                if board.markers[x - 1] == 'X' and board.markers[y - 1] == 'X':
                    print(f"Move: {x}->{current_peg.number} - remove {y}")
                    board.markers[current_peg.number - 1] = 'X'
                    board.markers[x - 1] = 'O'
                    board.markers[y - 1] = 'O'
                    moves.append((x, y))

                    ### Restart the cycle with new peg positions ***
                    transverse_board(board, current_peg.number, moves)
                    if check_finish(board):
                        return
                elif board.markers[x - 1] == 'O' or board.markers[y - 1] == 'O':
                    # There's a missing peg, Cannot move from here
                    continue

    if not check_finish(board):
        print("Exhausted all moves, but still more than 1 peg: failed!")
        x, y = moves.pop()
        print(f'Undo last move: {x} - {y}')
        # Put the pegs back from last move and move to next moves
        board.markers[x - 1] = 'X'
        board.markers[y - 1] = 'X'
        board.markers[pos - 1] = 'O'
        return


def check_finish(board: Board) -> bool:
    """
    Boolean function to check if the peg board only has one peg left, therefore successfully completed.
    :param board:
    :return:
    """
    count = 0
    for p in board.markers:
        if p == 'X':
            count += 1
        if count > 1:
            return False

    if count == 1:
        return True
    return False


def main() -> None:
    """
    The main routine function.
    :return:
    """
    board = Board()
    moves_stack = []

    print("Welcome to the Peg Board Game Solver!")
    start_time = time.perf_counter()
    peg_pos = first_peg_position()
    board.markers[peg_pos-1] = 'O'
    print(f"{board.markers=}")

    print(f"Starting...")  # And away we go!
    transverse_board(board, peg_pos, moves_stack)
    print(f"{moves_stack=}")
    print(f"{board.markers=}")

    end_time = time.perf_counter()
    print(f"Time to complete: {end_time - start_time}")


if __name__ == "__main__":
    main()