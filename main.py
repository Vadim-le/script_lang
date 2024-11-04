from db import create_database, fetch_and_save_posts, get_posts_by_user


def main():
    while True:
        print("\nВыберите действие:")
        print("1. Создать БД")
        print("2. Получить данные с сервера и сохранить в БД")
        print("3. Чтение данных из БД по user_id")
        print("4. Выход")

        case = input("Ваш выбор: ")

        if case == '1':
            create_database()
        elif case == '2':
            fetch_and_save_posts()
        elif case == '3':
            user_id = input("Введите user_id для получения постов: ")
            get_posts_by_user(user_id)
        elif case == '4':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()