import random
from time import sleep


def print_matrix(mat):
    for line in mat:
        print(" ".join(line))


def generate_line(line):
    return [
        str(random.randint(0, 1)) if (
            (random.randint(0, 100) < 5 and char == " ") or
            (random.randint(0, 100) < 95 and char != " ")
        ) else " "
        for char in line
    ]


def shift_matrix(mat):
    mat.pop()
    mat.insert(0, generate_line(mat[0]))


matrix = [" " * 30 for _ in range(20 )]

for _ in range(100):
    print_matrix(matrix)
    shift_matrix(matrix)
    sleep(0.05)
    print("\n" * 10)
