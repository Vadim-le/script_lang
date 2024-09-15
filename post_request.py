import requests
import json

url = "https://jsonplaceholder.typicode.com/posts"

new_post = {
    "title": "Тестовый пост",
    "body": "Cодержимое тестового поста.",
    "userId": 1
}
response = requests.post(url, json=new_post)

if response.status_code == 201:
    created_post = response.json()
    print("Созданный пост:")
    print(json.dumps(created_post, ensure_ascii=False, indent=4))
else:
    print("Ошибка при создании поста:", response.status_code)


