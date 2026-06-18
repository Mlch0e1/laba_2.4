import socket
import os


def upload_file(filename):
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    message = f"UPLOAD:{filename}\n{content}"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8888))
    sock.send(message.encode('utf-8'))

    response = sock.recv(1024).decode('utf-8')
    print(f"Ответ: {response}")
    sock.close()


def download_file(filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8888))
    sock.send(f"DOWNLOAD:{filename}".encode('utf-8'))

    data = sock.recv(10240)
    if data == b"NOT_FOUND":
        print("Файл не найден")
    else:
        with open(f"downloaded_{filename}.bin", 'wb') as f:
            f.write(data)
        print(f"Сохранён: downloaded_{filename}.bin ({len(data)} байт)")
    sock.close()


def main():
    print("=" * 40)
    print("КЛИЕНТ ЗАПУЩЕН")
    print("=" * 40)
    print("upload test_1.json - загрузить файл")
    print("download test_1 - скачать файл")
    print("exit - выход")
    print("=" * 40)

    while True:
        cmd = input("\n> ").strip()
        if cmd == 'exit':
            break
        elif cmd.startswith('upload '):
            upload_file(cmd[7:])
        elif cmd.startswith('download '):
            download_file(cmd[9:])
        else:
            print("Неизвестно. Пример: upload test_1.json")


if __name__ == "__main__":
    main()