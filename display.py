import json
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont

# ====== НАСТРОЙКИ ======
FILE_PATH = "answer.json"   # Укажите путь к вашему файлу с расписанием
# =======================

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Школьное расписание")
        self.root.geometry("1100x750")

        self.data = None
        self.classes = []
        self.all_teachers = []
        self.teacher_schedule = {}   # {teacher: {day: {lesson: [(class, subject)]}}}

        # Верхняя панель управления
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10, fill=tk.X)

        # Режим отображения
        self.mode_var = tk.StringVar(value="class")
        mode_class = tk.Radiobutton(top_frame, text="По классам", variable=self.mode_var,
                                    value="class", command=self.on_mode_change)
        mode_class.pack(side=tk.LEFT, padx=5)
        mode_teacher = tk.Radiobutton(top_frame, text="По учителям", variable=self.mode_var,
                                      value="teacher", command=self.on_mode_change)
        mode_teacher.pack(side=tk.LEFT, padx=5)

        # Переключатель транспонирования
        self.transposed = tk.BooleanVar(value=False)
        chk_transpose = tk.Checkbutton(top_frame, text="Транспонировать",
                                       variable=self.transposed,
                                       command=self.show_schedule)
        chk_transpose.pack(side=tk.LEFT, padx=10)

        tk.Label(top_frame, text="Выбор:").pack(side=tk.LEFT, padx=(20,5))
        self.combo_var = tk.StringVar()
        self.combo = ttk.Combobox(top_frame, textvariable=self.combo_var,
                                  state="readonly", width=25)
        self.combo.pack(side=tk.LEFT, padx=5)

        btn_show = tk.Button(top_frame, text="Показать", command=self.show_schedule)
        btn_show.pack(side=tk.LEFT, padx=5)

        # Область для таблицы с прокруткой
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(self.table_frame)
        scrollbar = tk.Scrollbar(self.table_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Загрузка данных
        self.load_data_from_file(FILE_PATH)

    def load_data_from_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.data = json.loads(content)

            self.classes = sorted(self.data.keys())

            # Построить расписание учителей
            self.build_teacher_schedule()

            # Настроить комбобокс в зависимости от режима
            self.on_mode_change()

            # Автоматически показать первое расписание
            if self.classes:
                self.show_schedule()
            # messagebox.showinfo("Успех", f"Загружено {len(self.classes)} классов и {len(self.all_teachers)} учителей.")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл '{filepath}' не найден.\nПроверьте путь в переменной FILE_PATH.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
            self.data = None

    def build_teacher_schedule(self):
        """Строит словарь: учитель -> день -> урок -> [(класс, предмет)]"""
        self.teacher_schedule = {}
        self.all_teachers = set()

        if not self.data:
            return

        for class_name, days in self.data.items():
            for day_idx, lessons in enumerate(days):
                for lesson_idx, lesson in enumerate(lessons):
                    subject = lesson.get("subject", "")
                    teacher = lesson.get("teacher", "")
                    if subject == "#" or not teacher:
                        continue
                    self.all_teachers.add(teacher)
                    # Инициализация структуры
                    self.teacher_schedule.setdefault(teacher, {})
                    self.teacher_schedule[teacher].setdefault(day_idx, {})
                    self.teacher_schedule[teacher][day_idx].setdefault(lesson_idx, [])
                    self.teacher_schedule[teacher][day_idx][lesson_idx].append((class_name, subject))

        self.all_teachers = sorted(self.all_teachers)

    def on_mode_change(self):
        """Обновляет список в комбобоксе при смене режима"""
        mode = self.mode_var.get()
        if mode == "class":
            self.combo['values'] = self.classes
            if self.classes:
                self.combo_var.set(self.classes[0])
        else:  # teacher
            self.combo['values'] = self.all_teachers
            if self.all_teachers:
                self.combo_var.set(self.all_teachers[0])
        self.show_schedule()

    def show_schedule(self):
        # Очистка
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.data:
            messagebox.showwarning("Нет данных", "Сначала загрузите файл с расписанием.")
            return

        mode = self.mode_var.get()
        selection = self.combo_var.get()
        if not selection:
            messagebox.showwarning("Нет выбора", "Выберите элемент из списка.")
            return

        if mode == "class":
            self.show_class_schedule(selection)
        else:
            self.show_teacher_schedule(selection)

    def show_class_schedule(self, class_name):
        if class_name not in self.data:
            messagebox.showerror("Ошибка", f"Класс '{class_name}' не найден.")
            return

        schedule = self.data[class_name]
        if not schedule:
            messagebox.showinfo("Информация", f"Для класса {class_name} расписание пустое.")
            return

        num_days = len(schedule)
        max_lessons = max((len(day) for day in schedule), default=0)

        transposed = self.transposed.get()

        if not transposed:
            # Обычный вид: дни — строки, уроки — столбцы
            headers = ["День"] + [f"Урок {i+1}" for i in range(max_lessons)]
            rows = num_days
            cols = max_lessons + 1
            get_cell = lambda d, l: (schedule[d][l] if l < len(schedule[d]) else None)
        else:
            # Транспонированный: уроки — строки, дни — столбцы
            headers = ["Урок"] + [f"День {i+1}" for i in range(num_days)]
            rows = max_lessons
            cols = num_days + 1
            get_cell = lambda l, d: (schedule[d][l] if d < len(schedule) and l < len(schedule[d]) else None)

        header_font = tkfont.Font(weight="bold", size=10)
        cell_font = tkfont.Font(size=9)

        # Заголовки
        for col, header in enumerate(headers):
            label = tk.Label(self.scrollable_frame, text=header, font=header_font,
                             relief="ridge", padx=5, pady=5, bg="#d9d9d9",
                             width=12, wraplength=100)
            label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        # Данные
        for r in range(rows):
            # Номер/название строки
            row_label = tk.Label(self.scrollable_frame,
                                 text=headers[0] if not transposed else f"Урок {r+1}",
                                 font=header_font,
                                 relief="ridge", padx=5, pady=5, bg="#f0f0f0")
            row_label.grid(row=r+1, column=0, sticky="nsew", padx=1, pady=1)

            for c in range(1, cols):
                if not transposed:
                    lesson_data = get_cell(r, c-1)   # day, lesson_idx
                else:
                    lesson_data = get_cell(r, c-1)   # lesson_idx, day

                if lesson_data:
                    subject = lesson_data.get("subject", "")
                    teacher = lesson_data.get("teacher", "")
                    text = f"{subject}\n{teacher}" if subject != "#" and teacher else (subject if subject != "#" else "")
                else:
                    text = ""

                label = tk.Label(self.scrollable_frame, text=text, font=cell_font,
                                 relief="ridge", padx=5, pady=5, bg="white",
                                 justify="center", wraplength=100)
                label.grid(row=r+1, column=c, sticky="nsew", padx=1, pady=1)

        # Растяжение
        for col in range(cols):
            self.scrollable_frame.grid_columnconfigure(col, weight=1)
        for row in range(rows + 1):
            self.scrollable_frame.grid_rowconfigure(row, weight=1)

    def show_teacher_schedule(self, teacher_name):
        if teacher_name not in self.teacher_schedule:
            messagebox.showerror("Ошибка", f"Учитель '{teacher_name}' не найден.")
            return

        teacher_data = self.teacher_schedule[teacher_name]
        if not teacher_data:
            messagebox.showinfo("Информация", f"У учителя {teacher_name} нет занятий.")
            return

        all_days = set()
        all_lessons = set()
        for day, lessons in teacher_data.items():
            all_days.add(day)
            all_lessons.update(lessons.keys())
        num_days = max(all_days) + 1 if all_days else 0
        max_lessons = max(all_lessons) + 1 if all_lessons else 0

        transposed = self.transposed.get()

        if not transposed:
            # дни — строки, уроки — столбцы
            headers = ["День"] + [f"Урок {i+1}" for i in range(max_lessons)]
            rows = num_days
            cols = max_lessons + 1
            get_cell = lambda d, l: teacher_data.get(d, {}).get(l, [])
        else:
            # уроки — строки, дни — столбцы
            headers = ["Урок"] + [f"День {i+1}" for i in range(num_days)]
            rows = max_lessons
            cols = num_days + 1
            get_cell = lambda l, d: teacher_data.get(d, {}).get(l, [])

        header_font = tkfont.Font(weight="bold", size=10)
        cell_font = tkfont.Font(size=9)

        # Заголовки
        for col, header in enumerate(headers):
            label = tk.Label(self.scrollable_frame, text=header, font=header_font,
                             relief="ridge", padx=5, pady=5, bg="#d9d9d9",
                             width=12, wraplength=100)
            label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        # Данные
        for r in range(rows):
            row_label = tk.Label(self.scrollable_frame,
                                 text=headers[0] if not transposed else f"Урок {r+1}",
                                 font=header_font,
                                 relief="ridge", padx=5, pady=5, bg="#f0f0f0")
            row_label.grid(row=r+1, column=0, sticky="nsew", padx=1, pady=1)

            for c in range(1, cols):
                if not transposed:
                    entries = get_cell(r, c-1)   # day, lesson_idx
                else:
                    entries = get_cell(r, c-1)   # lesson_idx, day

                if entries:
                    text = "\n".join([f"{cls}: {subj}" for cls, subj in entries])
                else:
                    text = ""

                label = tk.Label(self.scrollable_frame, text=text, font=cell_font,
                                 relief="ridge", padx=5, pady=5, bg="white",
                                 justify="center", wraplength=100)
                label.grid(row=r+1, column=c, sticky="nsew", padx=1, pady=1)

        # Растяжение
        for col in range(cols):
            self.scrollable_frame.grid_columnconfigure(col, weight=1)
        for row in range(rows + 1):
            self.scrollable_frame.grid_rowconfigure(row, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()