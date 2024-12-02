import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QComboBox, QLineEdit, QFileDialog, QMessageBox)

class DataVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() 
        self.data = None  # Переменная для хранения загруженных данных

    def initUI(self):
        # Настройка заголовка и размеров окна
        self.setWindowTitle('Лабораторная работа №6')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()  

        # Кнопка для загрузки CSV файла
        self.loadButton = QPushButton('Загрузить CSV')
        self.loadButton.clicked.connect(self.load_data)  # Подключение метода загрузки данных
        layout.addWidget(self.loadButton)

        # Label для отображения статистики
        self.statsLabel = QLabel('Статистика будет отображаться здесь.')
        layout.addWidget(self.statsLabel)

        # ComboBox для выбора типа графика
        self.plotTypeCombo = QComboBox()
        self.plotTypeCombo.addItems(['Выберите тип графика', 'Линейный график', 'Гистограмма', 'Круговая диаграмма'])
        self.plotTypeCombo.currentIndexChanged.connect(self.update_plot)  # Подключение метода обновления графика
        layout.addWidget(self.plotTypeCombo)

        # Поле ввода для нового значения
        self.newValueInput = QLineEdit()
        self.newValueInput.setPlaceholderText('Введите новое значение')  
        layout.addWidget(self.newValueInput)

        # Кнопка добавления нового значения
        self.addValueButton = QPushButton('Добавить значение')
        self.addValueButton.clicked.connect(self.add_value)  # Подключение метода добавления значения
        layout.addWidget(self.addValueButton)

        # Область для отображения графиков
        self.figure = plt.figure()  # Создание фигуры для графиков
        self.canvas = FigureCanvas(self.figure)  # Создание холста для отображения графиков
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def load_data(self):
        # Метод для загрузки данных из CSV файла
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv)')
        if file_path:
            self.data = pd.read_csv(file_path)  # Загрузка данных в DataFrame
            self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')  # Преобразование столбца 'Date' в формат datetime
            self.display_statistics()  # Отображение статистики
            self.update_plot()  # Обновление графика

    def display_statistics(self):
        # Метод для отображения статистики по загруженным данным
        if self.data is not None:
            num_rows = self.data.shape[0] 
            stats_value1 = {
                'Min': self.data['Value1'].min(),
                'Max': self.data['Value1'].max(),
                'Mean': self.data['Value1'].mean(),
                'Median': self.data['Value1'].median(),
                'Count': self.data['Value1'].count()
            }
            stats_value2 = {
                'Min': self.data['Value2'].min(),
                'Max': self.data['Value2'].max(),
                'Mean': self.data['Value2'].mean(),
                'Median': self.data['Value2'].median(),
                'Count': self.data['Value2'].count()
            }

            category_counts = self.data['Category'].value_counts()
            count_a = category_counts.get('A', 0)
            count_b = category_counts.get('B', 0)
            count_c = category_counts.get('C', 0)
            count_d = category_counts.get('D', 0)

            stats_text = (
                f'Статистика \n'
                f'Value1 - Min: {stats_value1["Min"]}, Max: {stats_value1["Max"]}, Mean: {stats_value1["Mean"]:.2f}, Median: {stats_value1 ["Median"]:.2f}, Count: {stats_value1["Count"]}\n'
                f'Value2 - Min: {stats_value2["Min"]}, Max: {stats_value2["Max"]}, Mean: {stats_value2["Mean"]:.2f}, Median: {stats_value2["Median"]:.2f}, Count: {stats_value2["Count"]}\n'
                f'Количество A: {count_a}\n'
                f'Количество B: {count_b}\n'
                f'Количество C: {count_c}\n'
                f'Количество D: {count_d}'
            )
            self.statsLabel.setText(stats_text)  # Обновление метки с текстом статистики

    def update_plot(self):
        # Метод для обновления графика в зависимости от выбранного типа
        if self.data is not None:
            plot_type = self.plotTypeCombo.currentText()  # Получение выбранного типа графика
            self.figure.clear()  # Очистка предыдущего графика

            if plot_type == 'Линейный график':
                plt.plot(self.data['Date'], self.data['Value1'], marker='o')  # Построение линейного графика
                plt.title('Линейный график')
                plt.xlabel('Date')
                plt.ylabel('Value1')
                plt.gcf().autofmt_xdate()

            elif plot_type == 'Гистограмма':
                plt.hist(self.data['Value2'])  # Построение гистограммы
                plt.title('Гистограмма')
                plt.xlabel('Value2')
                plt.ylabel('Частота')

            elif plot_type == 'Круговая диаграмма':
                category_counts = self.data['Category'].value_counts()  # Подсчет категорий для круговой диаграммы
                plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%')  # Построение круговой диаграммы
                plt.title('Круговая диаграмма')

            self.canvas.draw()

    def show_warning(self, message):
        # Метод для отображения предупреждающего сообщения
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle('Warning')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def add_value(self):
        # Метод для добавления нового значения в данные
        new_value = self.newValueInput.text()  # Получение нового значения из поля ввода
        if new_value and self.data is not None:
            plot_type = self.plotTypeCombo.currentText()  # Получение выбранного типа графика
            
            # Создаем новый DataFrame для нового значения
            new_row = pd.DataFrame({'Date': [pd.Timestamp.now()], 'Value1': [None], 'Value2': [None], 'Category': [None]})

            if plot_type == 'Линейный график':
                try:
                    new_value = float(new_value)
                    new_row['Value1'] = new_value
                except ValueError:
                    self.show_warning('Неверный ввод для Value1! Введите число.')
                    self.newValueInput.clear()  
                    return

            elif plot_type == 'Гистограмма':
                try:
                    new_value = float(new_value)
                    new_row['Value2'] = new_value
                except ValueError:
                    self.show_warning('Неверный ввод для Value2! Введите число.')
                    self.newValueInput.clear()  
                    return

            elif plot_type == 'Круговая диаграмма':
                if new_value in ['A', 'B', 'C', 'D']:
                    new_row['Category'] = new_value
                else:
                    self.show_warning('Неверный ввод для круговой диаграммы! Введите одну из букв: A, B, C или D')
                    self.newValueInput.clear()  
                    return
            # Конкатенируем новую строку к существующему DataFrame
            self.data = pd.concat([self.data, new_row], ignore_index=True)

            self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')

            self.update_plot()  # Обновление графика после добавления нового значения
            self.display_statistics()  # Обновление статистики после добавления нового значения
            self.newValueInput.clear()  # Очистка поля ввода после добавления значения

if __name__ == '__main__':
    app = QApplication(sys.argv)  
    ex = DataVisualizer()
    ex.show()
    sys.exit(app.exec_())