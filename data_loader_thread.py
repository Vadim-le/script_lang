import time
from PyQt5.QtCore import QThread, pyqtSignal

class DataLoaderThread(QThread):
    """Поток для загрузки данных из базы данных.

    Args:
        db_manager: Объект для управления базой данных.
    """
    data_loaded = pyqtSignal()  # Сигнал, который отправляется после загрузки данных
    saving_started = pyqtSignal()  # Сигнал, который отправляется при начале сохранения данных

    def __init__(self, db_manager):
        """Инициализация потока.

        Args:
            db_manager: Объект для управления базой данных.
        """
        super().__init__()
        self.db_manager = db_manager
        self.posts = []  # Список для хранения загруженных записей

    def run(self):
        """Основной метод потока, выполняющий загрузку данных."""
        time.sleep(10)
        self.posts = self.db_manager.fetch_posts()

        if self.posts:
            self.saving_started.emit()  # Эмитирование сигнала о начале сохранения
            time.sleep(3)
            self.db_manager.save_posts(self.posts)  
            self.data_loaded.emit()  # Эмитирование сигнала о завершении загрузки данных
        else:
            self.data_loaded.emit()  # Эмитирование сигнала, если нет данных для загрузки