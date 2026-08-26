import tkinter as tk
from tkinter import ttk


class ScheduleGUI:
    def __init__(self, root, classes):
        self.root = root
        self.classes = classes
        self.root.title("Расписание классов")

        # Левая панель - список классов
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        tk.Label(left_frame, text="Классы:").pack()
        self.listbox = tk.Listbox(left_frame, width=15, height=20)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        for name in sorted(self.classes.keys()):
            self.listbox.insert(tk.END, name)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        # Правая панель - таблицы расписания
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Заголовок для выбранного класса
        self.title_label = tk.Label(right_frame, text="Выберите класс", font=('Arial', 14))
        self.title_label.pack()

        # Фрейм для таблиц (две недели)
        self.table_frame = tk.Frame(right_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Инициализируем пустые таблицы
        self.tables = []
        for week in range(2):
            subframe = tk.Frame(self.table_frame, borderwidth=2, relief=tk.GROOVE)
            subframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            tk.Label(subframe, text=f"Неделя {week + 1}", font=('Arial', 12)).pack()
            # Таблица будет создаваться при выборе

        self.current_class = None

    def on_select(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        class_name = self.listbox.get(index)
        self.show_schedule(class_name)

    def show_schedule(self, class_name):
        # Очистить старые таблицы
        for child in self.table_frame.winfo_children():
            # удаляем все внутренние виджеты
            for subchild in child.winfo_children():
                subchild.destroy()

        self.title_label.config(text=f"Расписание класса {class_name}")
        cls = self.classes[class_name]
        day_names = ["Пн", "Вт", "Ср", "Чт", "Пт"]

        # Для каждой недели создаем таблицу
        for week in range(2):
            week_frame = self.table_frame.winfo_children()[week]  # по порядку
            # Заголовок уже есть, пересоздадим его
            # Удалим старые виджеты внутри week_frame (кроме Label заголовка)
            for widget in week_frame.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget("text").startswith("Неделя"):
                    continue
                widget.destroy()

            # Создаем таблицу: 5 строк (дни) и 10 колонок (уроки) + 1 для названия дня
            # Используем grid
            # Заголовок колонок (уроки)
            for col in range(10):
                lbl = tk.Label(week_frame, text=f"{col + 1}", font=('Arial', 8), relief=tk.RIDGE, width=8)
                lbl.grid(row=0, column=col + 1, sticky="nsew")
            # Названия дней
            for row, day in enumerate(day_names):
                lbl = tk.Label(week_frame, text=day, relief=tk.RIDGE, width=4)
                lbl.grid(row=row + 1, column=0, sticky="nsew")

            # Заполняем уроки
            days = cls.now[week]
            for row_idx, day_lessons in enumerate(days):
                for col_idx, lesson in enumerate(day_lessons):
                    text = ""
                    if lesson is not None:
                        text = f"{lesson['subject']}\n{lesson['teacher']}"
                    lbl = tk.Label(week_frame, text=text, relief=tk.RIDGE, width=8, height=2)
                    lbl.grid(row=row_idx + 1, column=col_idx + 1, sticky="nsew")

            # Настройка весов столбцов и строк для растяжения
            for col in range(11):
                week_frame.columnconfigure(col, weight=1)
            for row in range(6):
                week_frame.rowconfigure(row, weight=1)
