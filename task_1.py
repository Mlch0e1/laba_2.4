import struct


def parse_binary_file(filename):
    with open(filename, 'rb') as f:
        signature = f.read(4)
        if signature != b'DATA':
            print("Ошибка: неверная сигнатура файла")
            return

        version = struct.unpack('<H', f.read(2))[0]
        num_records = struct.unpack('<I', f.read(4))[0]

        print(f"Версия файла: {version}")
        print(f"Количество записей: {num_records}")
        print("-" * 40)

        total_temp = 0
        active_flags = 0

        for i in range(num_records):
            timestamp = struct.unpack('<Q', f.read(8))[0]
            record_id = struct.unpack('<I', f.read(4))[0]
            temp_raw = struct.unpack('<h', f.read(2))[0]
            flag = struct.unpack('<B', f.read(1))[0]

            temperature = temp_raw / 100.0
            total_temp += temperature

            if flag & 1:
                active_flags += 1

            print(f"Запись {i + 1}: ID={record_id}, t={temperature}°C, флаг={flag}")

        avg_temp = total_temp / num_records
        print("-" * 40)
        print(f"Средняя температура: {avg_temp:.2f}°C")
        print(f"Активных флагов: {active_flags}")


def create_test_file():
    with open("data.bin", "wb") as f:
        f.write(b'DATA')
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<I', 3))

        f.write(struct.pack('<Q', 1000000))
        f.write(struct.pack('<I', 1))
        f.write(struct.pack('<h', 2345))
        f.write(struct.pack('<B', 1))

        f.write(struct.pack('<Q', 1000001))
        f.write(struct.pack('<I', 2))
        f.write(struct.pack('<h', 1850))
        f.write(struct.pack('<B', 0))

        f.write(struct.pack('<Q', 1000002))
        f.write(struct.pack('<I', 3))
        f.write(struct.pack('<h', -520))
        f.write(struct.pack('<B', 1))


create_test_file()
parse_binary_file("data.bin")