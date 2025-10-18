import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.abspath('D:/Personal/programming/python_projects/'))

# Импортируем модуль
from Остальное import show

import random
# from ..Остальное import show
import re


def generate_number():
    return "x" if random.randint(0, 5) == 5 else str(random.randint(1, 10))


def generate_operation(return_type="tuple"):
    operators = ['+', '-', '*']
    number = generate_number()
    operator = random.choice(operators[:-1] if number == "x" else operators)
    if return_type == "str":
        return f"{operator} {number}"
    return operator, number


# Функция для генерации случайного выражения
def generate_expression():
    expr = "x"
    expr += " " + " ".join(generate_operation("str") for _ in range(random.randint(1, 3)))
    return expr


def mutate_expression(expression):
    operators = ['+', '-', '*']
    expression = expression.split()
    for i in range(random.randint(1, 4)):
        choice = random.randint(0, 7)
        if choice == 0 and len(expression) < 55:
            for j in generate_operation():
                expression.append(j)
        elif choice == 1 and len(expression) > 3:
            index = random.randint(2, len(expression)-1)
            expression.pop(index)
            expression.pop(index-1)
        else:
            index = random.randint(1, len(expression)-1)
            if index % 2 != 0:
                expression[index] = random.choice(operators)
            else:
                expression[index] = generate_number()
    return " ".join(expression)


def evaluate_expression(expr1, expr2):
    try:
        score = 0
        if isinstance(expr2, str):
            for x in range(-10, 11):
                score += abs(abs(eval(expr1)) - abs(eval(expr2)))
        else:
            for x, y in expr2:
                score += abs(eval(expr1, {"x": x}) - y)
        return score
    except ZeroDivisionError:
        return 9999999999


def get_best(exprs, target):
    best = exprs[0]
    best_score = evaluate_expression(best, target)
    for val in exprs[1:]:
        curr_score = evaluate_expression(val, target)
        if curr_score < best_score:
            best_score = curr_score
            best = val
    return best



def simplify_expression(expr):
    # Преобразование x*x*x*x*x в x**5, x*x*x*x в x**4, и так далее
    max_power = 10  # Предположим, что максимальная степень не превышает 10
    for power in range(max_power, 1, -1):
        pattern = r'(\bx\b(?:\s*\*\s*\bx\b){' + str(power - 1) + r'})'
        replacement = r'x^' + str(power)
        expr = re.sub(pattern, replacement, expr)

    return expr


# Целевая функция
target_function = "x**4 + 3*x**3 - 2*x**2 + x - 5"
target_function = "x**10"

target_function = [(1, 15), (2, 30), (3, 50)]
func = generate_expression()
print(func)
for _ in range(1000):
    funcs = []
    for _ in range(40):
        funcs.append(mutate_expression(func))
    func = get_best(funcs, target_function)
    print(func)
    if evaluate_expression(func, target_function) == 0:
        print("Найдена идентичная функция")
        break

# 6.803693771362305
# 3.7510223388671875
print("Готовая функция:", simplify_expression(func))
show.function(func, target_function if isinstance(target_function, str) else None)
