import requests

url = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(url)

if response.status_code == 200:
    posts = response.json()
    even_id_posts = [post for post in posts if post['userId'] % 2 == 0]
    print("Посты с чётными userId:")
    for post in even_id_posts:
        print(post)
else:
    print("Ошибка при получении данных:", response.status_code)
