import socket
'''
Задание 2.
UDP - СЕРВЕР
'''

HOST = "127.0.0.1"
PORT = 5000
def start_udp_server():
    # Создаем сокет для UDP-соединения
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Привязываем сокет к указанному адресу и порту
    server.bind((HOST, PORT))
    print(f"Сервер ожидает подключения на {HOST}:{PORT}")

    while True:
        # Получаем данные и адрес клиента, отправившего сообщение (максимум 1024 байта)
        data, adr = server.recvfrom(1024)
        print(f"Получено сообщение от клиента: {data.decode('utf-8')}")
        
        # Отправляем обратно те же данные клиенту
        server.sendto(data, adr)
        print('Сообщение отправлено')
        
        server.close()
        break

if __name__ == "__main__":
    start_udp_server()
