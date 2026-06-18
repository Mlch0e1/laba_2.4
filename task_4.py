import os


def to_json(obj, indent=0):
    if obj is None:
        return "null"
    if obj is True:
        return "true"
    if obj is False:
        return "false"
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return '"' + obj + '"'
    if isinstance(obj, list):
        items = [to_json(item, indent) for item in obj]
        return "[" + ", ".join(items) + "]"
    if isinstance(obj, dict):
        items = []
        for key, value in obj.items():
            items.append(f'"{key}": {to_json(value, indent)}')
        return "{" + ", ".join(items) + "}"
    return "null"


def from_json(json_str):
    json_str = json_str.strip()
    if not json_str:
        return None
    if json_str[0] == '{':
        return parse_object(json_str)[0]
    if json_str[0] == '[':
        return parse_array(json_str)[0]
    if json_str[0] == '"':
        return parse_string(json_str)[0]
    if json_str == 'true':
        return True
    if json_str == 'false':
        return False
    if json_str == 'null':
        return None
    try:
        if '.' in json_str:
            return float(json_str)
        return int(json_str)
    except:
        raise ValueError("Не число")


def parse_object(s):
    result = {}
    s = s[1:]
    while s and s[0] != '}':
        key, s = parse_string(s)
        s = s.strip()
        if s[0] != ':':
            raise ValueError("Ожидалось :")
        s = s[1:].strip()
        value, s = parse_value(s)
        result[key] = value
        s = s.strip()
        if s and s[0] == ',':
            s = s[1:].strip()
    return result, s[1:]


def parse_array(s):
    result = []
    s = s[1:]
    while s and s[0] != ']':
        value, s = parse_value(s)
        result.append(value)
        s = s.strip()
        if s and s[0] == ',':
            s = s[1:].strip()
    return result, s[1:]


def parse_string(s):
    if s[0] != '"':
        raise ValueError("Ожидалась кавычка")
    end = s.find('"', 1)
    if end == -1:
        raise ValueError("Нет закрывающей кавычки")
    return s[1:end], s[end + 1:]


def parse_value(s):
    s = s.strip()
    if not s:
        raise ValueError("Пустое значение")
    if s[0] == '"':
        return parse_string(s)
    if s[0] == '{':
        return parse_object(s)
    if s[0] == '[':
        return parse_array(s)
    if s.startswith('true'):
        return True, s[4:]
    if s.startswith('false'):
        return False, s[5:]
    if s.startswith('null'):
        return None, s[4:]
    i = 0
    if s[0] == '-':
        i = 1
    while i < len(s) and (s[i].isdigit() or s[i] == '.'):
        i += 1
    num_str = s[:i]
    try:
        if '.' in num_str:
            return float(num_str), s[i:]
        return int(num_str), s[i:]
    except:
        raise ValueError(f"Не число: {num_str}")


def validate_json(json_str):
    lines = json_str.split('\n')
    try:
        from_json(json_str)
        print("JSON валиден")
        return True
    except Exception as e:
        error = str(e)
        for i, line in enumerate(lines, 1):
            if '{' in line or '}' in line or '"' in line:
                print(f"Ошибка в строке {i}: {error}")
                print(f"{line}")
                return False
        print(f"Ошибка: {error}")
        return False


def test_json_files():
    print("ПРОВЕРКА JSON ФАЙЛОВ ИЗ ПАПКИ resource")

    resource_path = "resource"

    if not os.path.exists(resource_path):
        print(f"Папка {resource_path} не найдена!")
        return

    json_files = [f for f in os.listdir(resource_path) if f.endswith('.json')]

    if not json_files:
        print(f"JSON файлы не найдены в папке {resource_path}")
        return

    print(f"Найдено {len(json_files)} JSON файлов:\n")

    for filename in sorted(json_files):
        filepath = os.path.join(resource_path, filename)
        print(f"{filename}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            preview = content[:100].replace('\n', ' ')
            print(f"Содержимое: {preview}...")
            validate_json(content)

        except Exception as e:
            print(f"Ошибка при чтении: {e}")

        print()


if __name__ == "__main__":
    print("РАБОТА С JSON")

    print("\n1. Исходные данные (Python объект):")
    data = {
        "name": "Иван",
        "age": 20,
        "grades": [5, 4, 5],
        "is_student": True,
        "group": None
    }
    print(data)

    print("\nСериализация (Python → JSON):")
    json_text = to_json(data)
    print(json_text)

    print("\nДесериализация (JSON → Python):")
    parsed_data = from_json(json_text)
    print(parsed_data)

    print("\nПроверка:")
    if data == parsed_data:
        print("Данные совпадают, сериализация и десериализация работают")
    else:
        print("Данные не совпадают")

    print("\n5. Валидация правильного JSON:")
    validate_json('{"name": "John", "age": 25}')

    print("\n6. Валидация НЕправильного JSON:")
    print("   Пример: пропущена закрывающая скобка")
    validate_json('{"name": "John", "age": 25')

    print("\n7. Валидация с пропущенной кавычкой:")
    validate_json('{"name": "John, "age": 25}')

    print("\n8. Сохранение в файл:")
    with open("data.json", "w", encoding='utf-8') as f:
        f.write(json_text)
    print("Сохранено в data.json")

    print("\n9. Загрузка из файла:")
    with open("data.json", "r", encoding='utf-8') as f:
        loaded = f.read()
    print(f"Загружено: {loaded}")

    test_json_files()