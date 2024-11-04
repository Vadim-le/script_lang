from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

class AddRecordDialog(QDialog):
    def __init__(self, db_manager):
        """Инициализация диалогового окна для добавления записи.

        Args:
            db_manager: Объект для управления базой данных.
        """
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Добавить запись")  

        # Создание компоновки формы
        layout = QFormLayout()

        # Поля ввода для идентификатора пользователя, заголовка и текста записи
        self.user_id_input = QLineEdit()
        self.title_input = QLineEdit()
        self.body_input = QLineEdit()

        # Добавление полей ввода в форму
        layout.addRow("User  ID:", self.user_id_input)
        layout.addRow("Title:", self.title_input)
        layout.addRow("Body:", self.body_input)

        # Создание кнопки "Добавить" и подключение её к методу add_record
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_record)
        layout.addWidget(self.add_button)  

        # Установка компоновки для диалогового окна
        self.setLayout(layout)

    def add_record(self):
        """Метод для обработки нажатия кнопки "Добавить".

        Проверяет, заполнены ли все поля, и добавляет запись в базу данных.
        Если поля не заполнены, отображает предупреждение.
        """
        # Получение текста из полей ввода
        user_id = self.user_id_input.text()
        title = self.title_input.text()
        body = self.body_input.text()

        if user_id and title and body:
            self.db_manager.add_record(user_id, title, body)  
            self.accept()  
        else:
            QMessageBox.warning(
                self, "Ошибка", "Должны быть заполнены все поля"
            )