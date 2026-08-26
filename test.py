import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                             QWidget, QVBoxLayout, QLabel, QPushButton)

# ---------- Классы для каждой вкладки ----------
class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Это вкладка 1"))
        layout.addWidget(QPushButton("Кнопка на вкладке 1"))
        self.setLayout(layout)

class Tab2(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Это вкладка 2"))
        layout.addWidget(QPushButton("Кнопка на вкладке 2"))
        self.setLayout(layout)

class Tab3(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Это вкладка 3"))
        self.setLayout(layout)

class Tab4(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Это вкладка 4"))
        self.setLayout(layout)

class Tab5(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Это вкладка 5"))
        self.setLayout(layout)

# ---------- Главное окно ----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение с 5 вкладками")
        self.setGeometry(100, 100, 600, 400)

        # Создаём виджет вкладок
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)  # Устанавливаем как центральный виджет

        # Добавляем вкладки
        self.tabs.addTab(Tab1(), "Вкладка 1")
        self.tabs.addTab(Tab2(), "Вкладка 2")
        self.tabs.addTab(Tab3(), "Вкладка 3")
        self.tabs.addTab(Tab4(), "Вкладка 4")
        self.tabs.addTab(Tab5(), "Вкладка 5")

        # Можно подключить сигнал на смену вкладки (опционально)
        self.tabs.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        print(f"Переключились на вкладку {index + 1}")

# ---------- Запуск приложения ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
