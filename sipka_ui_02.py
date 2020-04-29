import time


# counts number of executed steps
step_counter = 0

# default moves in x y directions
X_MOVE_OPT = [-1, -1, -2, -2,  1, 1,  2, 2]
Y_MOVE_OPT = [-2,  2, -1,  1, -2, 2, -1, 1]



# create chessboard of required size
def create_board(size):
    chessboard = {0: {'neighbours': [], 'visited': '', 'sequence_num': ''}}

    for x in range(size):
        for y in range(size):
            neighbours = []
            square_num = (x * size) + y
            chessboard[square_num] = {}

            chessboard[square_num]['visited'] = False
            chessboard[square_num]['sequence_num'] = 0
            x_moves, y_moves = create_possible_moves(x, y, size)

            for move in range(len(x_moves)):
                neighbours.append((x_moves[move] * size) + y_moves[move])

            chessboard[square_num]['neighbours'] = neighbours

    return chessboard


# sets selected lists of possible moves in x y directions
def choose_move_list():
    global X_MOVE_OPT
    global Y_MOVE_OPT

    print(  "A: (1, 2) (1, -2) (2, 1) (2, -1) (-1, 2) (-1, -2) (-2, 1) (-2, -1)"
          "\nB: (-1, -2) (-1, 2) (-2, -1) (-2, 1) (1, -2) (1, 2) (2, -1) (2, 1)\n")
    choice = input("Vyber si poradie moznych pohybov: ")

    if choice == "A" or choice == "a":
        X_MOVE_OPT = [1,  1, 2,  2, -1, -1, -2, -2]
        Y_MOVE_OPT = [2, -2, 1, -1,  2, -2,  1, -1]

    if choice == "B" or choice == "b":
        X_MOVE_OPT = [-1, -1, -2, -2,  1, 1,  2, 2]
        Y_MOVE_OPT = [-2,  2, -1,  1, -2, 2, -1, 1]


# creates possible moves for selected square
def create_possible_moves(x, y, size):
    x_moves = []
    y_moves = []

    for i in range(8):
        next_x = x + X_MOVE_OPT[i]
        next_y = y + Y_MOVE_OPT[i]

        if in_area(next_x, next_y, size) == True:
            x_moves.append(next_x)
            y_moves.append(next_y)

    return x_moves, y_moves


# sets coordinates of starting point
def set_starting_point(size):
    x = int(input("Pociatocna suradnica x (0 - " + str(size - 1) + "): "))
    y = int(input("Pociatocna suradnica y (0 - " + str(size - 1) + "): "))
    return (x * size) + y


# checks if square is in the area of chessboard
def in_area(x, y, size):
    if x >= 0 and y >= 0 and x < size and y < size:
        return True
    else:
        return False


# checks if square was already visited
def unvisited(board, square_num):
    if board[square_num]['visited'] == False:
        return True
    else:
        return False


# measures time of find_path() function
def time_counter(counter):
    global start_time

    if counter == True:
        start_time = time.time()
    if counter == False:
        end_time = time.time()
        print("Cas najdenia cesty: {0:.2f}".format(end_time - start_time))


# converts square_num to coordinates
def num_to_coordinates(square_num, size, path_final):
    num = square_num
    x = num

    while num >= size:
        x = num - size
        num -= size

    y = (square_num - x) / size

    path_final.append((x, int(y)))
    return path_final


# finds knight's tour
def find_path(board, visited_count, size, square_num, path_final, time_limit):
    global start_time
    global step_counter

    board[square_num]['visited'] = True
    board[square_num]['sequence_num'] = visited_count
    path_final = num_to_coordinates(square_num, size, path_final)

    #if number of visited squares is size^2 then knight's tour was found
    if visited_count == size * size:
        print_path(board, size, path_final)
        time_counter(False)
        return True

    step_counter += 1

    # if execution time is larger than limit then function is terminated
    if time.time() > start_time + time_limit:
        return

    neighbours = board[square_num]['neighbours']
    for i in range(len(neighbours)):
        if unvisited(board, neighbours[i]) == True:
            if find_path(board, visited_count + 1, size, neighbours[i], path_final, time_limit) == True:
                return True

            # if dead end is found, set visited squares as unvisited and go back until there is another possible move
            board[neighbours[i]]['visited'] = False
            board[neighbours[i]]['sequence_num'] = 0
            path_final.pop()

    return False


# prints knight's tour
def print_path(board, size, path_final):
    # prints a sequence of coordinates of knight's tour
    print(path_final)

    # prints a chessboard where we can see in which order were the squares visited
    for x in range(size):
        for y in range(size):
            print(board[(x * size) + y]['sequence_num'], end = " ")
        print()
    print()


# prints number of executed steps
def print_step_counter():
    global step_counter

    print("Pocet krokov:", step_counter)
    step_counter = 0
    print()


# main function
def main():
    size = int(input("Zadaj velkost sachovnice: "))
    time_limit = int(input("Maximalna doba hladania: "))

    for i in range(10):
        path_final = []
        choose_move_list()
        board = create_board(size)
        square_num = set_starting_point(size)
        time_counter(True)

        if find_path(board, 1, size, square_num, path_final, time_limit) == False:
            print("Time limit over :(")

        print_step_counter()


main()