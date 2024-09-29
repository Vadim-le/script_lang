import socket

'''
Задание 1. 
TCP - СЕРВЕР
'''

HOST = '127.0.0.1'
PORT = 5000

def start_server():
    # Создаем сокет для TCP-соединения
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Привязываем сокет к указанному адресу и порту
    server.bind((HOST, PORT))
    
    # Начинаем прослушивание входящих соединений
    server.listen(1) # максимальное количество клиентов в очереди - 1
    print(f'Сервер ждет подключение по адресу {HOST}:{PORT}')
    
    while True:
        # Принимаем входящее соединение от клиента
        client, client_adr = server.accept()
        print(f'Client is connected {client_adr}')  # Выводим адрес подключившегося клиента
        
        # Получаем данные от клиента (максимум 1024 байта)
        data = client.recv(1024)
        if data:
            print(f'Полученное от клиента сообщение: {data.decode("utf-8")}')

            # Отправляем обратно те же данные клиенту
            client.sendall(data)
            print('Сообщение отправлено')
            
            server.close() 
            break 
        
if __name__ == "__main__":
    start_server()
