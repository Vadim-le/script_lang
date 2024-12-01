from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

class AddPostDialog(QDialog):
    """Диалоговое окно для добавления новой записи.

    Args:
        db_manager: Объект для управления базой данных.
    """
    def __init__(self, db_manager):
        """Инициализация диалогового окна.

        Args:
            db_manager: Объект для управления базой данных.
        """
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Добавить запись")

        layout = QFormLayout()
        self.user_id_input = QLineEdit()
        self.title_input = QLineEdit()
        self.body_input = QLineEdit() 

        layout.addRow("User  ID:", self.user_id_input)
        layout.addRow("Title:", self.title_input)
        layout.addRow("Body:", self.body_input)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_post) 
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_post(self):
        """Добавление новой записи в базу данных."""
        user_id = self.user_id_input.text()
        title = self.title_input.text()
        body = self.body_input.text()

        if user_id and title and body:
            self.db_manager.add_post(user_id, title, body) 
            self.accept() 
        else:
            QMessageBox.warning(
                self, "Ошибка", "Все поля должны быть заполнены"  
            )