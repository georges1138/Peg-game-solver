# This is a sample Python script.  It uses recursion to solve the Peg Board Game.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# 'Finished' flag
done = False

# List to track the peg moves
moves = []

# The Peg Board
markers = ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X']
##########  1   2   3   4   5   6   7   8  9   10  11  12  13   14  15
##markers = ['O','O','O','X','X','O','X','X','O','O','O','X','X','O','O']

# The rules of possible moves for each position on the board
rules = [[(4,2),(6,3)],[(7,4),(9,5)],[(8,5),(10,6)],[(1,2),(6,5),(11,7),(13,8)],[(12,8),(14,9)],[(1,3),(4,5),(13,9),(15,10)],
    [(2,4),(9,8)],[(3,5),(10,9)],[(2,5),(7,8)],[(3,6),(8,9)],
    [(4,7),(13,12)],[(5,8),(14,13)],[(4,8),(6,9),(11,12),(15,14)],
    [(5,9),(12,13)],[(6,10),(13,14)]]

class Peg:

    def __init__(self, number, moves):
        self.number = number
        self.moves = moves

    def __str__(self):
        return '{self.number} with moves {self.moves}'.format(self=self)


class Board:

    def __init__(self):
        self.all_pegs = []

        for i in range(len(rules)):
            created_peg = Peg(i + 1, rules[i])
            self.all_pegs.append(created_peg)

def first_peg():
    while True:
        try:
            firsthole = int(input("Please enter the starting hole: "))
        except:
            print("Invalid entry.  Please enter a number.")
            continue
        else:
            if firsthole not in [1, 4, 5, 6, 13]:
                print("Invalid starting hole.  Please enter again.")
                continue
            else:
                print(f'Confirmed: Starting at position {firsthole}')
                return firsthole


def transverse_board(board, markers, xp):
    global done
    global moves
    # pass
    # get the moves from current position
    for i in range(len(markers)):
        if markers[i] == 'O':
            curpeg = board.all_pegs[i]
            # print(curpeg)
            # For every valid move...
            for i in range(len(curpeg.moves)):
                x, y = curpeg.moves[i]
                # print(f'Test move: {x},{y}')
                # Make sure there are pegs
                if markers[x - 1] == 'X' and markers[y - 1] == 'X':
                    print(f"Move: {x}->{curpeg.number} - remove {y}")
                    markers[curpeg.number - 1] = 'X'
                    markers[x - 1] = 'O'
                    markers[y - 1] = 'O'
                    moves.append((x, y))
                    # print("adding move:")
                    # print(moves)
                    # print(markers)
                    done = check_finish(markers)
                    if done:
                        return
                    ### Restart the cycle with new peg positions ***
                    transverse_board(board, markers, curpeg.number)
                    if done:
                        return
                elif markers[x - 1] == 'O' or markers[y - 1] == 'O':
                    # There's a missing peg, Cannot move from here
                    # print('Cannot move, going to the next move:')
                    continue
        else:
            # print(f'{i+1}: Peg hole not empty, skipping:')
            continue

    # print("Got Here!!!----------------------")
    if not done:
        print("Exhausted all moves, but still more than 1 peg: failed!")
        x, y = moves[-1]
        print(f'Undo last move: {x} - {y}')
        # Put the pegs back from last move and move to next moves
        markers[x - 1] = 'X'
        markers[y - 1] = 'X'
        markers[xp - 1] = 'O'
        moves.pop(-1)
        # print("after")
        # print(moves)
        return


def check_finish(markers):
    count = 0
    # check to see if only one peg remains
    for i in range(len(markers)):
        if markers[i] == 'X':
            count += 1

    if count == 1:
        print("done.")
        return True
    else:
        # not done
        return False


print("Welcome to the Peg Board Game!")

start_time = time.time()
#First, Setup
board = Board()
pos = first_peg()
markers[pos-1] = 'O'
print(markers)
print("Starting...")
#And away we go
transverse_board(board, markers, pos)
print(moves)
print("Back in main")
print(markers)
end_time = time.time()
elapsed_time = end_time - start_time

print(elapsed_time)
