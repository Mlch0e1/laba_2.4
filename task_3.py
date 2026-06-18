import os
import re


def process_numbers(filename):

    if not os.path.exists(filename):
        print(f"Файл {filename} не найден!")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    print(f"Размер файла: {os.path.getsize(filename)} байт")

    def replacer(match):
        num = int(match.group())
        if num % 7 == 0:
            new_num = num * 100 // 5358
            print(f"  {num} → {new_num}")
            return str(new_num)
        print(f"  {num} → {num} (не кратно 7)")
        return str(num)

    new_text = re.sub(r'-?\d+', replacer, text)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_text)

    print(f"Новый размер: {os.path.getsize(filename)} байт")
    print("Готово!")


with open("numbers.txt", "w", encoding='utf-8') as f:
    f.write("Числа: 5, 15, 20, 7, 36, 100, -1, -18")

print("Поиск чисел кратных 7")

print("\nИсходный файл:")
with open("numbers.txt", "r", encoding='utf-8') as f:
    print(f.read())

print("\nОбработка:")
process_numbers("numbers.txt")

print("\nРезультат:")
with open("numbers.txt", "r", encoding='utf-8') as f:
    print(f.read())