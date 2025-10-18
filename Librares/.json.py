import json

data = '{"name": "Виви", "age": 20, "is_admin": false}'

# превращает текст в словарь
# load для чтения с файла
json_dict = json.loads(data)


# превращает словарь в текст
# load для чтения с файла
json_str = json.dumps(json_dict)

# Пример
# with open("data.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)


format_json_str = json.dumps(json_dict, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ':'))
# indent - табуляция
# ensure_ascii=False - позволяет сохранять русский текст без \uXXXX
# sort_keys=True - сортирует ключи по алфавиту
# separators - меняет разделители. Например, separators=(',', ':') убирает пробелы

print(format_json_str)
