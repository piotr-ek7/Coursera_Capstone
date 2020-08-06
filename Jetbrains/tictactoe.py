import random
import math

"""
Tic-Tac_Toe game
Menu: start user user                                      or 
      start level_ai level_ai (level_ai: easy medium hard) or 
      start user level_ai  (eg. start user medium)         or 
      start level_ai user                                  or 
      exit
     
Matrix input:
(1,3) (2,3) (3,3)
(1,2) (2,2) (2,3)
(1,1) (2,1) (3,1)
"""


def draw_game(array_to_draw):
    print("---------")
    for cell in range(len(array_to_draw)):
        print("|", " ".join(array_to_draw[cell]), "|")
    print("---------")


def matrix_all_combinations(basic_matrix):
    diagonal_main = [basic_matrix[cell][cell] for cell in range(len(basic_matrix[0]))]
    diagnonal_anti = [basic_matrix[cell][2-cell] for cell in range(len(basic_matrix[0]))]
    matrix_vertical = [[row[cell] for row in basic_matrix] for cell in range(len(basic_matrix[0]))]
    return basic_matrix + matrix_vertical + [diagonal_main] + [diagnonal_anti]


def convert_cells(outer_list, inner_list_id):
    if outer_list <= 3:
        col_pos = inner_list_id
        row_pos = 4 - outer_list
    else:
        row_pos = 4 - inner_list_id
        if 3 < outer_list < 7:
            col_pos = outer_list - 3
        else:
            col_pos = inner_list_id if outer_list == 7 else row_pos
    return col_pos, row_pos


def winning_combinations(matrix_to_check, number_xo=3):
    totalo = 0
    totalx = 0
    sublist_num = 0
    row_id = None
    col_id = None
    for sublist in matrix_to_check:
        subx = sublist.count("X")
        subo = sublist.count("O")
        if number_xo == 2:  # medium level
            sublist_num += 1
            id_null = sublist.index(" ") + 1 if sublist.count(" ") > 0 else 0
            col_id = convert_cells(sublist_num, id_null)[0]
            row_id = convert_cells(sublist_num, id_null)[1]
        if subx == number_xo and (subx + subo == number_xo):
            totalx = 25
            break
        elif subo == number_xo and (subx + subo == number_xo):
            totalo = 25
            break
        else:
            totalx += subx
            totalo += subo
    return totalx, totalo, row_id, col_id


def find_best_move(matrix, mark):  # hard level
    marks = ['X', 'O']
    marks.remove(mark)
    opponent_mark = marks[0]
    best_move = -math.inf
    move_i = 0
    move_j = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == " ":
                matrix[i][j] = mark
                score = mini_max(matrix, 0, False, mark, opponent_mark)
                matrix[i][j] = " "
                if score > best_move:
                    best_move = score
                    move_i = i
                    move_j = j
    return convert_cells(move_i + 1, move_j + 1)


def mini_max(matrix, depth, is_max, mark, opponent_mark):  # hard level
    if mark == "X":
        score = winning_combinations(matrix_all_combinations(matrix))[0]
        score_opponent = -winning_combinations(matrix_all_combinations(matrix))[1]
    else:
        score = winning_combinations(matrix_all_combinations(matrix))[1]
        score_opponent = -winning_combinations(matrix_all_combinations(matrix))[0]

    if score == 25:
        return score
    if score_opponent == -25:
        return score_opponent
    if score + score_opponent == 24:
        return 0

    if is_max:
        best_score = -math.inf
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == " ":
                    matrix[i][j] = mark
                    best_score = max(best_score, mini_max(matrix, depth + 1, False, mark, opponent_mark))
                    matrix[i][j] = " "
        return best_score
    else:
        best_score = math.inf
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == " ":
                    matrix[i][j] = opponent_mark
                    best_score = min(best_score, mini_max(matrix, depth + 1, True, mark, opponent_mark))
                    matrix[i][j] = " "
        return best_score


def game_implementation(matrix, col, row, who_play):
    matrix_transposed = [[row[cell] for row in reversed(matrix)] for cell in range(len(matrix[0]))]
    count_x = [cell for row in matrix_transposed for cell in row].count("X")
    count_o = [cell for row in matrix_transposed for cell in row].count("O")
    if count_x <= count_o:
        x_or_o = "X"
    else:
        x_or_o = "O"
    if who_play in ["easy", "medium", "hard"]:
        print('Making move level "{}"'.format(who_play))
        if who_play == "medium" and (winning_combinations(matrix_all_combinations(matrix), 2)[0] == 25 or
                                     winning_combinations(matrix_all_combinations(matrix), 2)[1] == 25):
            col = winning_combinations(matrix_all_combinations(matrix), 2)[3]
            row = winning_combinations(matrix_all_combinations(matrix), 2)[2]
        elif who_play == "hard":
            if count_x != 0:
                col = find_best_move(matrix, x_or_o)[0]
                row = find_best_move(matrix, x_or_o)[1]
        else:
            while matrix_transposed[col - 1][row - 1] != " ":
                col = random.randint(1, 3)
                row = random.randint(1, 3)
    if matrix_transposed[int(col) - 1][int(row) - 1] == " ":
        matrix_transposed[int(col) - 1][int(row) - 1] = x_or_o
        matrix_reverted = [[row[cell] for row in matrix_transposed] for cell in range(len(matrix_transposed[0]))]
        matrix_to_draw = [matrix_reverted[2], matrix_reverted[1], matrix_reverted[0]]
        draw_game(matrix_to_draw)
        matrix_final = matrix_all_combinations(matrix_to_draw)
        if winning_combinations(matrix_final)[0] == 25:
            print("X wins")
        elif winning_combinations(matrix_final)[1] == 25:
            print("O wins")
        elif winning_combinations(matrix_final)[0] + winning_combinations(matrix_final)[1] < 24:  # 9 horizontal cells + 9 vertical cells+ 6 cells on digonals
            return matrix_to_draw
        else:
            print("Draw")
        return False
    else:
        print("This cell is occupied! Choose another one!")
        return matrix


while True:
    input_command = input("Input command: ").split()
    if (input_command[0] == "start" and
        input_command[1] in ["user", "easy", "medium", "hard"] and
        input_command[2] in ["user", "easy", "medium", "hard"]
            and len(input_command) == 3):

        initial_cells = list("_________".replace("_", " "))
        cells_matrix = [initial_cells[i: i + 3] for i in range(0, len(initial_cells), 3)]

        if input_command[0] == "start":
            draw_game(cells_matrix)
            start_game = True
        else:
            start_game = False

        while start_game:
            for player in input_command[1:]:
                try:
                    if player == "user" and cells_matrix is not False:
                        cor1, cor2 = tuple(map(int, input("Enter the coordinates: ").split(" ")))
                    else:
                        cor1 = random.randint(1, 3)
                        cor2 = random.randint(1, 3)
                    if cor1 not in [1, 2, 3] or cor2 not in [1, 2, 3]:
                        print("Coordinates should be from 1 to 3!")
                    else:
                        try:
                            cells_matrix = game_implementation(cells_matrix, cor1, cor2, player)
                            if cells_matrix is False:
                                start_game = False
                        except:
                            continue
                except:
                    print("You should enter numbers!")
    elif input_command[0].lower() == "exit":
        break
    else:
        print("Bad parameters!")
