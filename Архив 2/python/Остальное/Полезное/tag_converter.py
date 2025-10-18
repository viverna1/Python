result = []
print("Введите HTML (дважды Enter для завершения):")

while True:
    try:
        line = input()
    except EOFError:  # Если ввод завершён (например, через файл)
        break

    if line.strip() == "":  # Проверяем пустую строку
        if result and result[-1].strip() == "":  # Если уже была пустая строка
            break
    result.append(line.replace("<", "&lt;"))

print("\n".join(result))
input()