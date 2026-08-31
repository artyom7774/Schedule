import json
import tkinter as tk
from tkinter import ttk

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Школьное расписание")
        self.root.geometry("1200x750")

        self.load_data()

        self.mode_var = tk.StringVar(value="class")
        self.selected_class = tk.StringVar()
        self.selected_teacher = tk.StringVar()

        self.create_widgets()
        self.update_view()

    def load_data(self):
        with open("answer.json", "r", encoding="utf-8") as f:
            self.answer = json.load(f)

        with open("settings.json", "r", encoding="utf-8") as f:
            self.settings = json.load(f)

        self.class_schedule = self.answer

        # Определение смены для классов
        self.class_shift = {}
        shift_array = self.settings["classes"]["shift"]
        for cls in self.class_schedule.keys():
            grade_num = int(cls.split()[0])
            idx = grade_num - 1
            shift_value = shift_array[idx] if idx < len(shift_array) else 0
            self.class_shift[cls] = "1 смена" if shift_value == 0 else "2 смена"

        # Построение расписания по учителям с указанием смены
        self.teacher_schedule = {}
        for class_name, days in self.class_schedule.items():
            shift = self.class_shift[class_name]
            for day_idx, lessons in enumerate(days):
                for lesson_idx, lesson in enumerate(lessons):
                    subject = lesson.get("subject")
                    teachers = lesson.get("teachers", [])
                    if subject != "#" and teachers:
                        display_text = f"{class_name} ({shift}): {subject}"
                        for teacher in teachers:
                            if teacher not in self.teacher_schedule:
                                self.teacher_schedule[teacher] = [[None]*8 for _ in range(5)]
                            self.teacher_schedule[teacher][day_idx][lesson_idx] = display_text

        self.class_list = sorted(self.class_schedule.keys())
        self.teacher_list = sorted(self.teacher_schedule.keys())

    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(side=tk.TOP, fill=tk.X)

        mode_frame = ttk.Frame(top_frame)
        mode_frame.pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(mode_frame, text="Режим:").pack(side=tk.LEFT)
        ttk.Radiobutton(mode_frame, text="По классам", variable=self.mode_var,
                        value="class", command=self.update_view).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="По учителям", variable=self.mode_var,
                        value="teacher", command=self.update_view).pack(side=tk.LEFT, padx=5)

        self.class_combo = ttk.Combobox(top_frame, textvariable=self.selected_class,
                                        values=self.class_list, state="readonly", width=15)
        self.class_combo.pack(side=tk.LEFT, padx=5)
        self.class_combo.bind("<<ComboboxSelected>>", self.update_view)

        self.teacher_combo = ttk.Combobox(top_frame, textvariable=self.selected_teacher,
                                          values=self.teacher_list, state="readonly", width=25)
        self.teacher_combo.pack(side=tk.LEFT, padx=5)
        self.teacher_combo.bind("<<ComboboxSelected>>", self.update_view)

        self.shift_label = ttk.Label(top_frame, text="", font=("Arial", 10, "bold"))
        self.shift_label.pack(side=tk.LEFT, padx=(20, 0))

        # Основной контейнер для таблиц
        self.table_frame = ttk.Frame(self.root, padding="10")
        self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def clear_table_frame(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

    def build_class_table(self):
        cls = self.selected_class.get()
        if not cls:
            return
        schedule = self.class_schedule.get(cls, [])
        if not schedule:
            return

        # Создаем один фрейм для таблицы класса
        frame = ttk.Frame(self.table_frame)
        frame.pack(fill=tk.BOTH, expand=True)

        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
        # Заголовки дней
        for col, day in enumerate(days):
            lbl = ttk.Label(frame, text=day, font=("Arial", 10, "bold"),
                            relief="ridge", anchor="center", padding=5)
            lbl.grid(row=0, column=col+1, sticky="nsew", padx=1, pady=1)

        # Заголовки уроков
        for row in range(1, 9):
            lbl = ttk.Label(frame, text=str(row), font=("Arial", 10, "bold"),
                            relief="ridge", anchor="center", padding=5)
            lbl.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)

        for col in range(6):
            frame.columnconfigure(col, weight=1)
        for row in range(9):
            frame.rowconfigure(row, weight=1)

        # Заполнение ячеек
        for day_idx, lessons in enumerate(schedule):
            for lesson_idx, lesson in enumerate(lessons):
                subject = lesson.get("subject", "")
                teachers = lesson.get("teachers", [])
                text = subject if subject != "#" else ""
                if teachers:
                    text += "\n" + ", ".join(teachers)
                lbl = tk.Label(frame, text=text, relief="ridge",
                               anchor="center", padx=2, pady=2, bg="white")
                lbl.grid(row=lesson_idx+1, column=day_idx+1, sticky="nsew", padx=1, pady=1)

    def build_teacher_tables(self):
        teacher = self.selected_teacher.get()
        if not teacher:
            return
        schedule = self.teacher_schedule.get(teacher, [])
        if not schedule:
            return

        # Разделяем данные по сменам
        shift_data = {"1 смена": [[None]*8 for _ in range(5)],
                      "2 смена": [[None]*8 for _ in range(5)]}

        for day in range(5):
            for lesson in range(8):
                cell = schedule[day][lesson]
                if cell is not None:
                    # Извлекаем смену из строки
                    start = cell.find('(')
                    end = cell.find(')')
                    if start != -1 and end != -1:
                        shift = cell[start+1:end]
                        if shift in shift_data:
                            shift_data[shift][day][lesson] = cell

        # Создаем два фрейма рядом
        left_frame = ttk.Frame(self.table_frame, relief="solid", borderwidth=1)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        right_frame = ttk.Frame(self.table_frame, relief="solid", borderwidth=1)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Заголовки для каждой таблицы
        ttk.Label(left_frame, text="Первая смена", font=("Arial", 12, "bold")).pack()
        ttk.Label(right_frame, text="Вторая смена", font=("Arial", 12, "bold")).pack()

        # Функция для создания таблицы в фрейме
        def build_shift_table(parent, data):
            days = ["Пн", "Вт", "Ср", "Чт", "Пт"]
            # Внутренний фрейм для сетки
            grid_frame = ttk.Frame(parent)
            grid_frame.pack(fill=tk.BOTH, expand=True)

            for col, day in enumerate(days):
                lbl = ttk.Label(grid_frame, text=day, font=("Arial", 9, "bold"),
                                relief="ridge", anchor="center", padding=2)
                lbl.grid(row=0, column=col+1, sticky="nsew", padx=1, pady=1)

            for row in range(1, 9):
                lbl = ttk.Label(grid_frame, text=str(row), font=("Arial", 9, "bold"),
                                relief="ridge", anchor="center", padding=2)
                lbl.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)

            for col in range(6):
                grid_frame.columnconfigure(col, weight=1)
            for row in range(9):
                grid_frame.rowconfigure(row, weight=1)

            for day_idx in range(5):
                for lesson_idx in range(8):
                    text = data[day_idx][lesson_idx] or ""
                    lbl = tk.Label(grid_frame, text=text, relief="ridge",
                                   anchor="center", padx=2, pady=2, bg="white",
                                   font=("Arial", 8))
                    lbl.grid(row=lesson_idx+1, column=day_idx+1, sticky="nsew", padx=1, pady=1)

        build_shift_table(left_frame, shift_data["1 смена"])
        build_shift_table(right_frame, shift_data["2 смена"])

    def update_view(self, *args):
        mode = self.mode_var.get()
        if mode == "class":
            self.class_combo.pack(side=tk.LEFT, padx=5)
            self.teacher_combo.pack_forget()
            cls = self.selected_class.get()
            if cls:
                shift = self.class_shift.get(cls, "")
                self.shift_label.config(text=f"Смена: {shift}")
            else:
                self.shift_label.config(text="")
        else:
            self.teacher_combo.pack(side=tk.LEFT, padx=5)
            self.class_combo.pack_forget()
            self.shift_label.config(text="")

        self.clear_table_frame()
        if mode == "class":
            self.build_class_table()
        else:
            self.build_teacher_tables()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()