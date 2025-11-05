import random
def new_tile(matrix):
    candidates = []
    odds = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
    for element in matrix.keys():
        if matrix[element] == 0:
            candidates.append(element)
    if len(candidates) != 0:
        new2 = random.choice(candidates)
        matrix[new2] = random.choice(odds)
    return matrix

def move_right(matrix):
    for checks in range(3):
        sel = 14
        for checks in range(4):
            for checks in range(3):
                if matrix[sel] == 0 and matrix[sel - 1] != 0:
                    matrix[sel] = matrix[sel - 1]
                    matrix[sel - 1] = 0
                sel -= 1
            sel += 13
    sel = 14
    for checks in range(4):
        for checks in range(3):
            if matrix[sel] == matrix[sel - 1]:
                matrix[sel] *= 2
                matrix[sel - 1] = 0
            sel -= 1
        sel += 13
    for checks in range(3):
        sel = 14
        for checks in range(4):
            for checks in range(3):
                if matrix[sel] == 0 and matrix[sel - 1] != 0:
                    matrix[sel] = matrix[sel - 1]
                    matrix[sel - 1] = 0
                sel -= 1
            sel += 13
    return matrix

def move_left(matrix):
    for checks in range(3):
        sel = 11
        for checks in range(4):
            for checks in range(3):
                if matrix[sel] == 0 and matrix[sel + 1] != 0:
                    matrix[sel] = matrix[sel+1]
                    matrix[sel + 1] = 0
                sel += 1
            sel += 7
    sel = 11
    for checks in range(4):
        for checks in range(3):
            if matrix[sel] == matrix[sel + 1]:
                matrix[sel] *= 2
                matrix[sel + 1] = 0
            sel += 1
        sel += 7
    for checks in range(3):
        sel = 11
        for checks in range(4):
            for checks in range(3):
                if matrix[sel] == 0 and matrix[sel + 1] != 0:
                    matrix[sel] = matrix[sel+1]
                    matrix[sel + 1] = 0
                sel += 1
            sel += 7
    return matrix

def move_up(matrix):
    for checks in range(3):
        sel = 11
        for checks in range(4):
            for checks in range(3):
                if matrix[sel] == 0 and matrix[sel + 10] != 0:
                    matrix[sel] = matrix[sel+10]
                    matrix[sel + 10] = 0
                sel += 10
            sel -= 29
    sel = 11
    for checks in range(4):
        for checks in range(3):
            if matrix[sel] == matrix[sel + 10]:
                matrix[sel] *= 2
                matrix[sel + 10] = 0
            sel += 10
        sel -= 29
    for checks in range(3):
        sel = 11
        for checks in range(4):
            for checks in range(3):
                if matrix[sel] == 0 and matrix[sel + 10] != 0:
                    matrix[sel] = matrix[sel+10]
                    matrix[sel + 10] = 0
                sel += 10
            sel -= 29
    return matrix

def move_down(matrix):
    for checks in range(3):
        sel = 41
        for checks in range(4):
            for checks in range(3):
                if matrix[sel] == 0 and matrix[sel - 10] != 0:
                    matrix[sel] = matrix[sel - 10]
                    matrix[sel - 10] = 0
                sel -= 10
            sel += 31
    sel = 41
    for checks in range(4):
        for checks in range(3):
            if matrix[sel] == matrix[sel - 10]:
                matrix[sel] *= 2
                matrix[sel - 10] = 0
            sel -= 10
        sel += 31
    for checks in range(3):
        sel = 41
        for checks in range(4):
            for checks in range(3):
                if matrix[sel] == 0 and matrix[sel - 10] != 0:
                    matrix[sel] = matrix[sel - 10]
                    matrix[sel - 10] = 0
                sel -= 10
            sel += 31
    return matrix

def game_over(matrix):
    candidates = []
    for element in matrix.keys():
        if matrix[element] == 0:
            candidates.append(element)
    if len(candidates) == 0:
        game_over = True
        testmatrix = matrix.copy()
        Rmatrix = move_right(testmatrix)
        if Rmatrix != matrix:
            game_over = False
        testmatrix = matrix.copy()
        Lmatrix = move_left(testmatrix)
        if Lmatrix != matrix:
            game_over = False
        testmatrix = matrix.copy()
        Umatrix = move_up(testmatrix)
        if Umatrix != matrix:
            game_over = False
        testmatrix = matrix.copy()
        Dmatrix = move_down(testmatrix)
        if Dmatrix != matrix:
            game_over = False
    else:
        game_over = False
    return game_over