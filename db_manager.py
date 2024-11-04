import requests
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class DatabaseManager:
    def __init__(self, db_name):
        """Инициализация менеджера базы данных.

        Args:
            db_name (str): Имя базы данных для подключения.
        """
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_name)
        
        self.db.open()

    def close_connection(self):
        """Закрывает подключение к базе данных."""
        self.db.close()

    @property
    def connection(self):
        """Возвращает текущее соединение с базой данных."""
        return self.db

    def create_table(self):
        """Создает таблицу 'posts' в базе данных, если она еще не существует."""
        query = QSqlQuery(self.db)
        query.exec_(
            '''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,  
                user_id INTEGER,         
                title TEXT,              
                body TEXT 
            )
            '''
        )

    def add_record(self, user_id, title, body):
        """Добавляет новую запись в таблицу 'posts'.

        Args:
            user_id (int): Идентификатор пользователя.
            title (str): Заголовок поста.
            body (str): Содержимое поста.
        """
        query = QSqlQuery(self.db)
        query.prepare(
            "INSERT INTO posts (user_id, title, body) VALUES (?, ?, ?)"
        )
        query.addBindValue(user_id)
        query.addBindValue(title)    
        query.addBindValue(body)      
        query.exec_()  

    def delete_post(self, post_id):
        """Удаляет запись с указанным ID из таблицы 'posts'.

        Args:
            post_id (int): ID поста для удаления.
        """
        query = QSqlQuery(self.db)
        query.prepare("DELETE FROM posts WHERE id = ?")
        query.addBindValue(post_id)  
        query.exec_() 
    
        
    def fetch_and_save_posts(self):
        """Получает данные с API и сохраняет их в базу данных."""
        url = "https://jsonplaceholder.typicode.com/posts"
        response = requests.get(url)  # Выполняем GET-запрос к API

        if response.status_code == 200:
            posts = response.json()  
            print("Данные успешно получены с сервера.")

            query = QSqlQuery(self.db)

            for post in posts:
                query.prepare(
                    '''
                    INSERT INTO posts (id, user_id, title, body) VALUES (?, ?, ?, ?)
                    '''
                )
                query.addBindValue(post['id'])      
                query.addBindValue(post['userId'])
                query.addBindValue(post['title'])
                query.addBindValue(post['body'])
                query.exec_()  
        else:
            print("Ошибка при получении данных:", response.status_code)

   
