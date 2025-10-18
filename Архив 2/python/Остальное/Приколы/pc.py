

class Stop(Exception):
    """Исключение для остановки выполнения программы."""


def parse_instruction(code_string: str):
    """Разбирает строку кода на имя функции и аргументы.

    Args:
        code_string (str): Строка кода.

    Returns:
        str: Имя функции.
        list: Список аргументов.
    """
    code_list = code_string.split()
    func_name = code_list[0]
    args = list(map(int, code_list[1:]))
    return func_name, args

def execute_instruction(func_name, args):
    """Выполняет инструкцию.

    Args:
        func_name (str): Имя функции.
        args (list): Список аргументов.

    Raises:
        ValueError: Если функция не существует.
        Stop: Если вызвана функция остановки программы.
    """
    if func_name in regular_funcs:
        return regular_funcs[func_name](args)
    elif func_name in special_funcs:
        return special_funcs[func_name](*args)
    else:
        raise ValueError(f"Неизвестная функция: {func_name}")


def process_list(func):
    global data
    def wrapper(indexes: str):
        master_index = int(indexes[0])
        values = [data[i] for i in indexes]
    
        result = func(values)
    
        if result is not None:
            data[master_index] = result
        return result
    return wrapper

@process_list
def add(args):
    return sum(args)

@process_list
def sub(args):
    return args[0] - sum(data[arg] for arg in args[1:])

@process_list
def mul(args):
    result = 1
    for i in args:
        if i == 0:
            return 0
        result *= i
    return result

@process_list
def div(args):
    if args[1] == 0:
        print("Zero Di, Error")
        return
    return args[0] / args[1]

@process_list
def exp(args):
    return args[0] ** args[1]

@process_list
def sqr(args):
    return args[0] ** (1 / args[1])

@process_list
def mod(args):
    if args[1] == 0:
        print("Zero Di, Error")
        return
    return args[0] % args[1]

@process_list
def absl(args):
    return abs(args[0])


@process_list
def prn(args):
    print(args[0])

def halt():
    """Останавливает выполнение программы."""
    raise Stop()

def jmp(index):
    global line_index
    line_index = index - 2

def setv(*values):
    if len(values) != 2:
        print("wrong format, correct: setv <index> <value>")
        return
    data[values[0]] = values[1]

def gr(*indexes):
    global line_index
    if len(indexes) != 2:
        print("wrong format, correct: gr <value> <value>")
        return
    if data[indexes[0]] > data[indexes[1]]:
        line_index += 2
        while check_line(line_index):
            line_index += 1

def eq(*indexes):
    global line_index
    if len(indexes) != 2:
        print("wrong format, correct: eq <value> <value>")
        return
    if data[indexes[0]] == data[indexes[1]]:
        line_index += 2
        while check_line(line_index):
            line_index += 1


def check_line(line_index):
    return not code_lines[line_index].startswith("#") and len(code_lines[line_index].split()) > 0

# Словарь обычных функций
regular_funcs = {
    "prn": prn,
    "add": add,
    "sub": sub,
    "mul": mul,
    "div": div,
    "sqr": sqr,
    "mod": mod,
    "abs": absl
}

# Словарь специальных функций
special_funcs = {
    "halt": halt,
    "jmp": jmp,
    "setv": setv,
    "gr": gr,
    "eq": eq
}


line_index = 0
code_lines = None
data = None

def main(code):
    global line_index, code_lines, data
    # Хранилище данных
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    code_lines = code.split("\n")

    # Запуск выполнения программы
    complete_lines_count = 0
    try:
        while line_index < len(code_lines):
            # input(code_lines[line_index])
            if check_line(line_index):
                func_name, args = parse_instruction(code_lines[line_index])
                execute_instruction(func_name, args)
            
            line_index += 1
            complete_lines_count += 1
            if complete_lines_count >= 996:
                print("Превышен лимит обработанных строк: 996")
                break
    except Stop:
        pass


prog = """
setv 0 10
setv 1 3
add 2 0 1
prn 2
sub 3 0 1
prn 3
mul 4 0 1
prn 4
div 5 0 1
prn 5
mod 6 0 1
prn 6
exp 7 0 1
prn 7
halt
"""


if __name__ == "__main__":
    main(prog)
