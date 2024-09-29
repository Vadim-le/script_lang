import socket
'''
Задание 2.
UDP - КЛИЕНТ
'''

HOST = "127.0.0.1"
PORT = 5000

def start_udp_client(message):
    # Создаем сокет для UDP-соединения
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Отправляем сообщение на сервер, кодируя его в формате UTF-8
    client.sendto(message.encode('utf-8'), (HOST, PORT))
    print(f'Сообщение отправлено на {HOST}:{PORT}')

    # Получаем ответ от сервера (максимум 1024 байта)
    data, _ = client.recvfrom(1024) # возвращает данные и адрес отправителя (нижнее подчеркивание испаользуется для гнорирования данных об адресе отправителя)
    print(f"Получено сообщение от сервера: {data.decode('utf-8')}")
    client.close()
    
if __name__ == "__main__":
    message = input('Введите сообщение: ')
    start_udp_client(message)