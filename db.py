import sqlite3
import requests


def create_database():
    """
    Создает базу данных и таблицу 'posts', если она не существует.
    Таблица содержит столбцы для идентификатора поста, идентификатора пользователя, заголовка и текста поста.
    """
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()

    cursor.execute(
        '''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT,
        body TEXT
    )
    '''
    )

    connection.commit()
    connection.close()
    print("База данных и таблица 'posts' созданы.")


def fetch_and_save_posts():
    """
    Получает данные о постах из внешнего API и сохраняет их в таблицу 'posts'.
    Если запрос успешен (код состояния 200), данные постов будут вставлены в базу данных.
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)

    if response.status_code == 200:
        posts = response.json()
        print("Данные получены с сервера.")

        connection = sqlite3.connect('posts.db')
        cursor = connection.cursor()

        for post in posts:
            cursor.execute(
                '''
            INSERT INTO posts (id, user_id, title, body) VALUES (?, ?, ?, ?)
            ''',
                (post['id'], post['userId'], post['title'], post['body']),
            )

        connection.commit()
        connection.close()
        print(f"Сохранено {len(posts)} постов в БД.")
    else:
        print("Ошибка при получении данных:", response.status_code)


def get_posts_by_user(user_id):
    """
    Извлекает и отображает все посты пользователя по его идентификатору (user_id).
    Если посты найдены, они выводятся на экран; если нет, выводится соответствующее сообщение.
    """
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()

    cursor.execute(
        '''
        SELECT * FROM posts WHERE user_id = ?
        ''',
        (user_id,),
    )

    rows = cursor.fetchall()
    connection.close()

    if rows:
        print(f"\nПосты пользователя с user_id = {user_id}:")
        for post in rows:
            print("-" * 40)
            print(f"Post ID: {post[0]}")
            print(f"User  ID: {post[1]}")
            print(f"Title: {post[2]}")
            print(f"Body: {post[3]}\n")
        print("-" * 40)
        print(f"\nВсе посты пользователя с user_id = {user_id} выведены.")
    else:
        print(f"\nПосты пользователя с user_id = {user_id} не найдены.")