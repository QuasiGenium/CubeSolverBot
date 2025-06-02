import kociemba

col_to_sgt = {"y": "U", "w": "D", "b": "F", "g": "B", "r": "R", "o": "L"}

def make_instruction(sides):
    cub_not = ''
    for i in sides:
        cub_not += col_to_sgt[i]
    a = kociemba.solve(cub_not)
    return a

