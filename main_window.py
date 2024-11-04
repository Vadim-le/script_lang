from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QTableView,
    QWidget,
    QMessageBox,
)
from PyQt5.QtSql import QSqlTableModel
from add_record_form import AddRecordDialog


class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        """Инициализация главного окна приложения.

        Args:
            db_manager: Объект для управления базой данных.
        """
        super().__init__()
        self.resize(600, 400) 

        self.db_manager = db_manager 

        # Инициализация пользовательского интерфейса
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        # Поле для поиска записей
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Поиск по заголовку")
        self.search_field.setStyleSheet("padding: 5px; font-size: 14px;")

        # Подключение сигнала изменения текста к методу поиска
        self.search_field.textChanged.connect(self.search)

        # Кнопки управления
        self.refresh_button = self.create_button("Обновить", self.load_data)
        self.add_button = self.create_button("Добавить", self.open_add_form)
        self.delete_button = self.create_button("Удалить", self.delete_post)

        # Таблица для отображения записей
        self.table = QTableView(self)
        self.model = QSqlTableModel(self, self.db_manager.connection)
        self.model.setTable("posts")
        self.load_data()  # Загрузка данных из базы данных
        self.table.setModel(self.model)

        # Создание вертикального макета для размещения виджетов
        layout = QVBoxLayout()
        layout.addWidget(self.search_field)
        layout.addWidget(self.table)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_button(self, text, slot):
        """Создание кнопки с заданным текстом и подключение слота.

        Args:
            text (str): Текст кнопки.
            slot (callable): Метод, который будет вызван при нажатии кнопки.

        Returns:
            QPushButton: Созданная кнопка.
        """
        button = QPushButton(text)
        button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        button.clicked.connect(slot)
        return button

    def load_data(self):
        """Загрузка данных из базы данных в таблицу."""
        if not self.model.select():
            print("Ошибка загрузки данных:", self.model.lastError().text())

    def search(self):
        """Поиск записей по заголовку."""
        search_term = self.search_field.text()
        self.model.setFilter(f"title LIKE '%{search_term}%'" if search_term else "")
        self.model.select()

    def open_add_form(self):
        """Открытие диалогового окна для добавления записи."""
        dialog = AddRecordDialog(self.db_manager)
        if dialog.exec():
            self.load_data()

    def delete_post(self):
        """Удаление выбранной записи."""
        selected_index = self.table.currentIndex()
        if selected_index.row() == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return

        confirm = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Удалить выбранную запись? Это действие нельзя отменить.",
        )
        if confirm == QMessageBox.Yes:
            post_id = self.model.record(selected_index.row()).value("id")
            self.db_manager.delete_post(post_id)
            self.load_data()