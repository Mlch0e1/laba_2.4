import os


def serialize_to_xml(obj, root_name="root"):
    if isinstance(obj, dict):
        result = f"<{root_name}>"
        for key, value in obj.items():
            result += serialize_to_xml(value, key)
        result += f"</{root_name}>"
        return result
    elif isinstance(obj, list):
        result = ""
        for item in obj:
            result += serialize_to_xml(item, root_name)
        return result
    else:
        return f"<{root_name}>{obj}</{root_name}>"


def deserialize_from_xml(xml_str):
    xml_str = xml_str.strip()
    content = _get_tag_content(xml_str)
    return _parse_content(content)


def _get_tag_name(xml_str):
    start = xml_str.find('<') + 1
    end = xml_str.find('>')
    return xml_str[start:end]


def _get_tag_content(xml_str):
    tag_name = _get_tag_name(xml_str)
    start = xml_str.find('>') + 1
    end = xml_str.find(f'</{tag_name}>')
    return xml_str[start:end]


def _parse_content(content):
    content = content.strip()
    if '<' not in content:
        return content

    result = {}
    i = 0
    while i < len(content):
        if content[i] == '<':
            tag_end = content.find('>', i)
            tag_name = content[i + 1:tag_end]
            close_tag = f'</{tag_name}>'
            close_pos = content.find(close_tag, tag_end)
            inner = content[tag_end + 1:close_pos]

            if tag_name in result:
                if not isinstance(result[tag_name], list):
                    result[tag_name] = [result[tag_name]]
                result[tag_name].append(_parse_content(inner))
            else:
                result[tag_name] = _parse_content(inner)

            i = close_pos + len(close_tag)
        else:
            i += 1
    return result


def validate_xml(xml_str):
    lines = xml_str.split('\n')
    stack = []

    for line_num, line in enumerate(lines, 1):
        j = 0
        length = len(line)

        while j < length:
            if line[j] == '<':
                if j + 1 < length and line[j + 1] == '/':
                    j += 2
                    tag_name = ""
                    while j < length and line[j] != '>':
                        tag_name += line[j]
                        j += 1
                    if not stack or stack[-1] != tag_name:
                        print(
                            f"Ошибка в строке {line_num}: Несоответствие тегов. Ожидался </{stack[-1] if stack else '?'}>, найден </{tag_name}>")
                        return False
                    stack.pop()
                else:
                    j += 1
                    tag_name = ""
                    while j < length and line[j] != '>' and not line[j].isspace():
                        tag_name += line[j]
                        j += 1
                    while j < length and line[j] != '>':
                        j += 1
                    if tag_name and not (j > 0 and line[j - 1] == '/'):
                        stack.append(tag_name)
            j += 1

    if stack:
        print(f"Ошибка: Не закрыты теги: {', '.join(stack)}")
        return False

    print("XML валиден")
    return True


def test_xml_files():
    print("ПРОВЕРКА XML ФАЙЛОВ ИЗ ПАПКИ resource")

    resource_path = "resource"

    if not os.path.exists(resource_path):
        print(f"Папка {resource_path} не найдена!")
        return

    xml_files = [f for f in os.listdir(resource_path) if f.endswith('.xml')]

    if not xml_files:
        print(f"XML файлы не найдены в папке {resource_path}")
        return

    print(f"Найдено {len(xml_files)} XML файлов:\n")

    for filename in sorted(xml_files):
        filepath = os.path.join(resource_path, filename)
        print(f"{filename}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            preview = content[:150].replace('\n', ' ')
            print(f"Начало: {preview}...")
            validate_xml(content)

        except Exception as e:
            print(f"Ошибка при чтении: {e}")

        print()


if __name__ == "__main__":
    print("XML сериализация, десериализация и валидация")

    print("\nТЕСТ СЕРИАЛИЗАЦИИ И ДЕСЕРИАЛИЗАЦИИ:")

    original_data = {"student": {"name": "Петр", "age": "19", "group": "2КС-9"}}
    print("Исходные данные:", original_data)

    xml_output = serialize_to_xml(original_data)
    print("\nСериализованный XML:\n", xml_output)

    parsed_data = deserialize_from_xml(xml_output)
    print("\nДесериализованные данные:", parsed_data)

    if original_data == parsed_data:
        print("\nДанные совпадают!")
    else:
        print("\nДанные не совпадают")

    print("\nТЕСТ ВАЛИДАЦИИ:")

    print("\nПравильный XML")
    validate_xml("<root><name>John</name></root>")

    print("\nОшибка: не закрыт тег")
    validate_xml("<root><name>John</root>")

    print("\nОшибка: несоответствие тегов")
    validate_xml("<root><name>John</name></root1>")

    test_xml_files()