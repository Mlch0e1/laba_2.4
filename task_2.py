import os


def encrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()

    result = bytearray()
    for byte in data:
        shifted = ((byte << 2) | (byte >> 6)) & 0xFF
        encrypted = shifted ^ key
        result.append(encrypted)

    with open(output_file, 'wb') as f:
        f.write(result)

    print(f"Готово: {input_file} -> {output_file}")


def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()

    result = bytearray()
    for byte in data:
        xored = byte ^ key
        decrypted = ((xored >> 2) | (xored << 6)) & 0xFF
        result.append(decrypted)

    with open(output_file, 'wb') as f:
        f.write(result)

    print(f"Готово: {input_file} -> {output_file}")


with open("test.txt", "w", encoding='utf-8') as f:
    f.write("Салам Мир! Тестовый файл для шифрования 123456")

print("Шифрование и дешифрование")

print("\n1. Шифрование:")
encrypt_file("test.txt", "encrypted.bin", 0xAA)

print("\n2. Расшифровка:")
decrypt_file("encrypted.bin", "decrypted.txt", 0xAA)

print("\n3. Проверка:")
with open("test.txt", "r", encoding='utf-8') as f:
    original = f.read()
with open("decrypted.txt", "r", encoding='utf-8') as f:
    decrypted = f.read()

print(f"Оригинал: {original}")
print(f"Расшифровано: {decrypted}")

if original == decrypted:
    print("\nУСПЕХ! Файл успешно зашифрован и расшифрован!")
else:
    print("\n Ой ошибка!")

print("\n4. Информация о файлах:")
print(f"test.txt: {os.path.getsize('test.txt')} байт")
print(f"encrypted.bin: {os.path.getsize('encrypted.bin')} байт")
print(f"decrypted.txt: {os.path.getsize('decrypted.txt')} байт")