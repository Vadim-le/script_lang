import requests
import json

post_id = 100 # при id=101 будет ошибка 500, тк сервер не хранит созданный нами ранее пост
url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

updated_post = {
    "id": post_id,
    "title": "Обновлённый пост",
    "body": "Обновлённое содержимое поста.",
    "userId": 1
}

response = requests.put(url, json=updated_post)

if response.status_code == 200:
    updated_post_response = response.json()
    print("Обновлённый пост:")
    print(json.dumps(updated_post_response, ensure_ascii=False, indent=4))
else:
    print("Ошибка при обновлении поста:", response.status_code)
