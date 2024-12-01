from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QTableView,
    QWidget,
    QLabel,
    QMessageBox,
)
from PyQt5.QtCore import QTimer
from PyQt5.QtSql import QSqlTableModel
from add_record_form import AddPostDialog
from data_loader_thread import DataLoaderThread

class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.setWindowTitle("Управление записями")
        self.resize(600, 400)

        self.db_manager = db_manager

        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Поиск по заголовку")
        self.search_field.setStyleSheet("padding: 5px; font-size: 14px;")

        # Подключение сигнала изменения текста к методу поиска
        self.search_field.textChanged.connect(self.search)

        self.load_data_button = self.create_button("Загрузить данные", self.load_data_in_thread)
        self.add_button = self.create_button("Добавить", self.open_add_dialog)
        self.delete_button = self.create_button("Удалить", self.delete_post)

        self.table = QTableView(self)
        
        self.model = QSqlTableModel(self, self.db_manager.connection)
        self.model.setTable("posts")
        self.model.select()

        self.table.setModel(self.model)

        self.status_label = QLabel("Текущий статус: Готово", self)

        layout = QVBoxLayout()
        layout.addWidget(self.search_field)
        layout.addWidget(self.status_label)
        layout.addWidget(self.table)
        layout.addWidget(self.load_data_button) 
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_data()  

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_updates)
        self.timer.start(10000)

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
        self.status_label.setText("Текущий статус: Загрузка...")

        if not self.model.select():
            print("Ошибка загрузки данных:", self.model.lastError().text())
            self.status_label.setText("Текущий статус: Ошибка загрузки данных") 
        else:
            self.status_label.setText("Текущий статус: Готово")

    def search(self):
        """Поиск записей по заголовку."""
        search_term = self.search_field.text()
        self.model.setFilter(f"title LIKE '%{search_term}%'" if search_term else "")
        self.model.select()

    def load_data_in_thread(self):
        """Загрузка данных в отдельном потоке."""
        self.load_data_button.setEnabled(False)
        self.load_data_button.setStyleSheet("background-color: #A9A9A9; color: white; font-weight: bold; padding: 10px;")  # Тусклый цвет кнопки
        self.status_label.setText("Текущий статус: Загрузка...")

        self.thread = DataLoaderThread(self.db_manager)
        self.thread.saving_started.connect(self.on_saving_started)
        self.thread.data_loaded.connect(self.on_data_loaded)
        self.thread.start()

    def on_saving_started(self):
        """Обновление статуса при начале сохранения."""
        self.status_label.setText("Текущий статус: Сохранение...")

    def on_data_loaded(self):
        """Обновление интерфейса после загрузки данных."""
        self.load_data()
        self.load_data_button.setEnabled(True)
        self.load_data_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")  # Восстановление цвета кнопки
        self.status_label.setText("Текущий статус: Готово")

    def open_add_dialog(self):
        """Открытие диалогового окна для добавления записи."""
        dialog = AddPostDialog(self.db_manager)
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
            "Вы уверены, что хотите удалить выбранную запись?",
        )
        if confirm == QMessageBox.Yes:
            post_id = self.model.record(selected_index.row()).value("id")
            self.db_manager.delete_post(post_id)
            self.load_data()

    def check_for_updates(self):
        """Проверка обновлений данных на сервере."""
        print("Проверка обновлений данных на сервере...")
        self.load_data_in_thread()