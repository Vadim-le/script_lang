import socket 

'''
Задание 1.
TCP - КЛИЕНТ
'''

HOST = '127.0.0.1'
PORT = 5000

def start_client(message):
    # Создаем сокет для TCP-соединения
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Подключаемся к серверу по указанному адресу и порту
    client.connect((HOST, PORT))
    print(f'Клиент подключен по адресу {HOST}:{PORT}') 
    
    # Отправляем сообщение на сервер, кодируя его в формат UTF-8
    client.sendall(message.encode('utf-8'))
    
    # Получаем ответ от сервера (максимум 1024 байта)
    data = client.recv(1024)
    print(f"Полученное от сервера сообщение: {data.decode('utf-8')}")

    client.close()
        
if __name__ == "__main__":
    message = input('Введите сообщение: ')
    start_client(message)
