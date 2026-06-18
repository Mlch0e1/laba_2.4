import socket
import threading
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def handle_client(conn, addr):
    print(f"Клиент подключился: {addr}")
    try:
        data = conn.recv(4096).decode('utf-8')
        print(f"Получено: {data[:200]}")

        if data.startswith("UPLOAD:"):
            filename = data[7:].split('\n')[0]
            content = data[data.find('\n') + 1:]

            print(f"Имя файла: {filename}")
            print(f"Содержимое: {content[:100]}")

            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            with open(filepath, 'rb') as f:
                original = f.read()
            encrypted = bytes([b ^ 0xAA for b in original])

            with open(filepath + '.bin', 'wb') as f:
                f.write(encrypted)

            conn.send(b"OK")
            print(f"Файл сохранён: {filename}")

        elif data.startswith("DOWNLOAD:"):
            filename = data[9:].strip()
            filepath = os.path.join(UPLOAD_DIR, filename + '.bin')

            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    conn.sendall(f.read())
                print(f"Файл отправлен: {filename}.bin")
            else:
                conn.send(b"NOT_FOUND")

    except Exception as e:
        print(f"Ошибка: {e}")
        conn.send(b"ERROR")
    finally:
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8888))
    server.listen(5)
    print("=" * 40)
    print("СЕРВЕР ЗАПУЩЕН на порту 8888")
    print("=" * 40)

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    start_server()