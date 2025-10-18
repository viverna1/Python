import numpy as np


def compare(check_list, comparator):
    best = check_list[0]
    for val in check_list:
        if abs(val - comparator) < abs(best - comparator):
            best = val
    return best


def mutate(number, target):
    difference = abs(number - target)
    # Убедимся, что числа не становятся отрицательными и не превышают разумные пределы
    lower_bound = max(1, number - difference) - 1
    upper_bound = min(target * 2, number + difference) + 1
    return np.random.randint(lower_bound, upper_bound, 10)


target_number = 2624783
population = np.random.randint(1, target_number * 2, 10)  # Популяция создается с числами до 2*target_number

for i in range(10):  # Увеличено количество итераций
    curr_value = compare(population, target_number)
    if target_number == curr_value:
        print(f"Целевое число найдено на итерации {i}")
        break
    population = mutate(curr_value, target_number)
else:
    print("Целевое число не найдено за заданное количество итераций.")

if target_number in population:
    print(f"Результат: список, в котором есть число {target_number}: {population}")
else:
    print(f"Результат: список, в котором есть число, близкое к {target_number}: {population}")
