import json
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont

FILE_PATH = "1.json"


class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Школьное расписание")
        self.root.geometry("1000x700")

        self.data = None
        self.classes = []

        # Верхняя панель выбора класса
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10, fill=tk.X)

        tk.Label(top_frame, text="Класс:").pack(side=tk.LEFT, padx=5)
        self.class_var = tk.StringVar()
        self.class_combo = ttk.Combobox(top_frame, textvariable=self.class_var,
                                        state="readonly", width=15)
        self.class_combo.pack(side=tk.LEFT, padx=5)

        btn_show = tk.Button(top_frame, text="Показать расписание", command=self.show_schedule)
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

        # Автоматическая загрузка при запуске
        self.load_data_from_file(FILE_PATH)

    def load_data_from_file(self, filepath):
        try:
            self.data = {
    "10 \"Б\"": [
        [
            {
                "subject": "Математика",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Ветренникова Александра Сергеевна"
            },
            {
                "subject": "Математика",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "История Беларуси в контексте всемирной истории",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "Русская литература",
                "teacher": "Зайковская Юлия Сергеевна"
            },
            {
                "subject": "Черчение",
                "teacher": "Федотова Галина Михайловна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Бурехина Татьяна Михайловна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Обществоведение",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Биология",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Информатика",
                "teacher": "Малистова Елена Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "История Беларуси в контексте всемирной истории",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "Английский язык",
                "teacher": "Ветренникова Александра Сергеевна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Бурехина Татьяна Михайловна"
            },
            {
                "subject": "Математика",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Бурехина Татьяна Михайловна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Кублицкая Татьяна Леонидовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "10 \"В\"": [
        [
            {
                "subject": "Математика",
                "teacher": "Верлова Инна Генриховна"
            },
            {
                "subject": "Обществоведение",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Биология",
                "teacher": "Солдатова Анна Валерьевна"
            },
            {
                "subject": "Черчение",
                "teacher": "Федотова Галина Михайловна"
            },
            {
                "subject": "История Беларуси в контексте всемирной истории",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Математика",
                "teacher": "Верлова Инна Генриховна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Верлова Инна Генриховна"
            },
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "История Беларуси в контексте всемирной истории",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Информатика",
                "teacher": "Любоза Александр Александрович"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Матвеев Александр Владимирович"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Верлова Инна Генриховна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Матвеев Александр Владимирович"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "11 \"А\"": [
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Концова Наталья Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "История Беларуси в контексте всемирной истории",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Головешко Наталья Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Головешко Наталья Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Концова Наталья Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Биология",
                "teacher": "Малахова Владислава Сергеевна"
            },
            {
                "subject": "История Беларуси в контексте всемирной истории",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "Информатика",
                "teacher": "Испеньков Андрей Николаевич"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Концова Наталья Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "Обществоведение",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Астрономия",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Голубева Ольга Васильевна"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "11 \"Б\"": [
        [
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Палубец Мария Александровна"
            },
            {
                "subject": "Астрономия",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "История",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "Биология",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Кучко Наталья Вячеславовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусская литература",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "История",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "Обществоведение",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "Информатика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "Математика",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Палубец Мария Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "11 \"В\"": [
        [
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "История Беларуси в контексте всемирной истории",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Шиенок Наталья Николаевна"
            },
            {
                "subject": "Математика",
                "teacher": "Мурашко Татьяна Семёновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Ильчук Кристина Александровна"
            },
            {
                "subject": "Обществоведение",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Математика",
                "teacher": "Мурашко Татьяна Семёновна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Испенькова Вера Викторовна"
            },
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Подлужный Никита Сергеевич"
            },
            {
                "subject": "История Беларуси в контексте всемирной истории",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Астрономия",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русская литература",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Подлужный Никита Сергеевич"
            },
            {
                "subject": "Английский язык",
                "teacher": "Ильчук Кристина Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Мурашко Татьяна Семёновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Мурашко Татьяна Семёновна"
            },
            {
                "subject": "Биология",
                "teacher": "Быкова Лариса Григорьевна"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Подлужный Никита Сергеевич"
            },
            {
                "subject": "Информатика",
                "teacher": "Малистова Елена Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "5 \"А\"": [
        [
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Палубец Мария Александровна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Аксёнова Антонина Антоновна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Палубец Мария Александровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Кислая Татьяна Анатольевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Основы безопасности жизнедеятельности",
                "teacher": "Козел Тамара Ивановна"
            },
            {
                "subject": "Математика",
                "teacher": "Кислая Татьяна Анатольевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Палубец Мария Александровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Козлов Сергей Александрович"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Человек и Мир",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Кислая Татьяна Анатольевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Кислая Татьяна Анатольевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Гурченко Варвара Константиновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Всемирная История",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Аксёнова Антонина Антоновна"
            },
            {
                "subject": "Математика",
                "teacher": "Кислая Татьяна Анатольевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Гурченко Варвара Константиновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "5 \"Б\"": [
        [
            {
                "subject": "Русский язык",
                "teacher": "Батура Алеся Александровна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Голубева Ольга Васильевна"
            },
            {
                "subject": "Математика",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Костюкевич Алена Васильевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Ильчук Кристина Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русская литература",
                "teacher": "Величко Жанна Иосифовна"
            },
            {
                "subject": "Математика",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Голубева Ольга Васильевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Батура Алеся Александровна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Ильчук Кристина Александровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусский язык",
                "teacher": "Голубева Ольга Васильевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Величко Жанна Иосифовна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Трудовое обучение",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Математика",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Основы безопасности жизнедеятельности",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Ильчук Кристина Александровна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Костюкевич Алена Васильевна"
            },
            {
                "subject": "Человек и Мир",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Математика",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Батура Алеся Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "5 \"В\"": [
        [
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Стальмаков Сергей Олегович"
            },
            {
                "subject": "Математика",
                "teacher": "Кореневская Татьяна Леонидовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Человек и Мир",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Кореневская Татьяна Леонидовна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Коробач Екатерина Александровна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Коробач Екатерина Александровна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Кореневская Татьяна Леонидовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Кореневская Татьяна Леонидовна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Стальмаков Сергей Олегович"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Основы безопасности жизнедеятельности",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Стальмаков Сергей Олегович"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Коробач Екатерина Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Кореневская Татьяна Леонидовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "5 \"Г\"": [
        [
            {
                "subject": "Основы безопасности жизнедеятельности",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Беднякова Светлана Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Испенькова Вера Викторовна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Скрабневская Мария Васильевна"
            },
            {
                "subject": "Математика",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Скрабневская Мария Васильевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Скрабневская Мария Васильевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Абесадзе Светлана Валерьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русская литература",
                "teacher": "Беднякова Светлана Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Математика",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Абесадзе Светлана Валерьевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Всемирная История",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Абесадзе Светлана Валерьевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Испенькова Вера Викторовна"
            },
            {
                "subject": "Математика",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Человек и Мир",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусский язык",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "5 \"Д\"": [
        [
            {
                "subject": "Человек и Мир",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Шедько Ростислав Васильевич"
            },
            {
                "subject": "Английский язык",
                "teacher": "Горбач Анна Александровна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "История",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Иванов Владислав Олегович"
            },
            {
                "subject": "Математика",
                "teacher": "Шедько Ростислав Васильевич"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Мировая художественная культура",
                "teacher": "Козьякова Татьяна Викторовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Гурченко Варвара Константиновна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Гурченко Варвара Константиновна"
            },
            {
                "subject": "Математика",
                "teacher": "Шедько Ростислав Васильевич"
            },
            {
                "subject": "История",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Иванов Владислав Олегович"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Горбач Анна Александровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русская литература",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Гурченко Варвара Константиновна"
            },
            {
                "subject": "Основы безопасности жизнедеятельности",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Иванов Владислав Олегович"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Горбач Анна Александровна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Математика",
                "teacher": "Шедько Ростислав Васильевич"
            },
            {
                "subject": "Математика",
                "teacher": "Шедько Ростислав Васильевич"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "5 \"Е\"": [
        [
            {
                "subject": "Русская литература",
                "teacher": "Тугаринова Марина Александровна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Человек и Мир",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Цыбульская Ольга Валентиновна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Цыбульская Ольга Валентиновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Зелинская Ксения Евгеньевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Цыбульская Ольга Валентиновна"
            },
            {
                "subject": "Математика",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Ширко Татьяна Михайловна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Ширко Татьяна Михайловна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русская литература",
                "teacher": "Тугаринова Марина Александровна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Зелинская Ксения Евгеньевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Основы безопасности жизнедеятельности",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Жуков Никита Сергеевич"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Зелинская Ксения Евгеньевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Математика",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "5 \"Ж\"": [
        [
            {
                "subject": "История",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Эдуардовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Тарапата Светлана Олеговна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Бурехина Татьяна Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Эдуардовна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Макаренко Наталья Геннадьевна"
            },
            {
                "subject": "История",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Батура Алеся Александровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Шальц Римма Акмуратовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Макаренко Наталья Геннадьевна"
            },
            {
                "subject": "Человек и Мир",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Шиенок Наталья Николаевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Бурехина Татьяна Михайловна"
            },
            {
                "subject": "Мировая художественная культура",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Макаренко Наталья Геннадьевна"
            },
            {
                "subject": "Основы безопасности жизнедеятельности",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Эдуардовна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Шиенок Наталья Николаевна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Эдуардовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Тарапата Светлана Олеговна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Бурехина Татьяна Михайловна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Тарапата Светлана Олеговна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Шиенок Наталья Николаевна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Эдуардовна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Батура Алеся Александровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "5 \"З\"": [
        [
            {
                "subject": "Математика",
                "teacher": "Хандопкина Наталья Анатольевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Елисеенко Светлана Николаевна"
            },
            {
                "subject": "Основы безопасности жизнедеятельности",
                "teacher": "Мурашко Татьяна Семёновна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Хандопкина Наталья Анатольевна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Елисеенко Светлана Николаевна"
            },
            {
                "subject": "Математика",
                "teacher": "Хандопкина Наталья Анатольевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Салманова Алеся Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "История",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ледник Ирина Леонидовна"
            },
            {
                "subject": "Человек и Мир",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ледник Ирина Леонидовна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Елисеенко Светлана Николаевна"
            },
            {
                "subject": "История",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Математика",
                "teacher": "Хандопкина Наталья Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Математика",
                "teacher": "Хандопкина Наталья Анатольевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ледник Ирина Леонидовна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "5 \"И\"": [
        [
            {
                "subject": "Английский язык",
                "teacher": "Нехуженко Татьяна Юрьевна"
            },
            {
                "subject": "Основы безопасности жизнедеятельности",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Концова Наталья Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Базыко Яна Игоревна"
            },
            {
                "subject": "Математика",
                "teacher": "Базыко Яна Игоревна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусский язык",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Нехуженко Татьяна Юрьевна"
            },
            {
                "subject": "История",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Костючкова Инна Станиславовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусский язык",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Нехуженко Татьяна Юрьевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Математика",
                "teacher": "Базыко Яна Игоревна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Концова Наталья Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Базыко Яна Игоревна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Концова Наталья Владимировна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Базыко Яна Игоревна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "История",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Человек и Мир",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "6 \"А\"": [
        [
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Тугаринова Марина Александровна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Дубовик Лариса Юрьевна"
            },
            {
                "subject": "Информатика",
                "teacher": "Испеньков Андрей Николаевич"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русская литература",
                "teacher": "Кучко Наталья Вячеславовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Дятковская Юлия Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Тугаринова Марина Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русская литература",
                "teacher": "Кучко Наталья Вячеславовна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Тугаринова Марина Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Трудовое обучение",
                "teacher": "Дубовик Лариса Юрьевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Дятковская Юлия Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Дятковская Юлия Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "6 \"Б\"": [
        [
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Костюкевич Алена Васильевна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Котловская Анастасия Юрьевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Подлужный Никита Сергеевич"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Биология",
                "teacher": "Солдатова Анна Валерьевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Костюкевич Алена Васильевна"
            },
            {
                "subject": "Математика",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Информатика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Котловская Анастасия Юрьевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Подлужный Никита Сергеевич"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Подлужный Никита Сергеевич"
            },
            {
                "subject": "Английский язык",
                "teacher": "Котловская Анастасия Юрьевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Математика",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Математика",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусский язык",
                "teacher": "Костюкевич Алена Васильевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Козьякова Татьяна Викторовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "6 \"В\"": [
        [
            {
                "subject": "Русская литература",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Кублицкая Татьяна Леонидовна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русская литература",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Денисенко Сергей Викторович"
            },
            {
                "subject": "Математика",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусская литература",
                "teacher": "Кублицкая Татьяна Леонидовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Математика",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Биология",
                "teacher": "Малахова Владислава Сергеевна"
            },
            {
                "subject": "Математика",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Информатика",
                "teacher": "Малистова Елена Анатольевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Математика",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Денисенко Сергей Викторович"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "6 \"Г\"": [
        [
            {
                "subject": "Трудовое обучение",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Шенделова Инна Викторовна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Математика",
                "teacher": "Шенделова Инна Викторовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Беднякова Светлана Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Информатика",
                "teacher": "Любоза Александр Александрович"
            },
            {
                "subject": "Русский язык",
                "teacher": "Беднякова Светлана Владимировна"
            },
            {
                "subject": "Биология",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Остапчук Ольга Тимофеевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Трудовое обучение",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Савченко Светлана Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Шенделова Инна Викторовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Шенделова Инна Викторовна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Остапчук Ольга Тимофеевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Савченко Светлана Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Шенделова Инна Викторовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Беднякова Светлана Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Остапчук Ольга Тимофеевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "6 \"Д\"": [
        [
            {
                "subject": "Русская литература",
                "teacher": "Макаренко Наталья Геннадьевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Аксёнова Антонина Антоновна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Стальмаков Сергей Олегович"
            },
            {
                "subject": "Математика",
                "teacher": "Конофальская Елена Николаевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Конофальская Елена Николаевна"
            },
            {
                "subject": "Математика",
                "teacher": "Конофальская Елена Николаевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Свирская Екатерина Александровна"
            },
            {
                "subject": "Информатика",
                "teacher": "Испеньков Андрей Николаевич"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Аксёнова Антонина Антоновна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Конофальская Елена Николаевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Осипук Леонид Аркадьевич"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Стальмаков Сергей Олегович"
            },
            {
                "subject": "Русская литература",
                "teacher": "Макаренко Наталья Геннадьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Конофальская Елена Николаевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Свирская Екатерина Александровна"
            },
            {
                "subject": "Биология",
                "teacher": "Быкова Лариса Григорьевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Свирская Екатерина Александровна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Аксёнова Антонина Антоновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Стальмаков Сергей Олегович"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Осипук Леонид Аркадьевич"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "6 \"Е\"": [
        [
            {
                "subject": "Белорусский язык",
                "teacher": "Чикун Галина Валерьевна"
            },
            {
                "subject": "Информатика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Жаголкина Александра Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Скрабневская Мария Васильевна"
            },
            {
                "subject": "Математика",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Биология",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Чикун Галина Валерьевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Скрабневская Мария Васильевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Чикун Галина Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Жаголкина Александра Анатольевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Жаголкина Александра Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Трудовое обучение",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Жуков Никита Сергеевич"
            },
            {
                "subject": "Математика",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Скрабневская Мария Васильевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "6 \"Ж\"": [
        [
            {
                "subject": "Информатика",
                "teacher": "Малистова Елена Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Мороз Светлана Сергеевна"
            },
            {
                "subject": "Математика",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Иванов Владислав Олегович"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусский язык",
                "teacher": "Савченко Светлана Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Савченко Светлана Владимировна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Мороз Светлана Сергеевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Иванов Владислав Олегович"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Мороз Светлана Сергеевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Савченко Светлана Владимировна"
            },
            {
                "subject": "Биология",
                "teacher": "Солдатова Анна Валерьевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Шальц Римма Акмуратовна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Зайковская Юлия Сергеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Математика",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Зайковская Юлия Сергеевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Иванов Владислав Олегович"
            },
            {
                "subject": "Мировая художественная культура",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Математика",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "6 \"З\"": [
        [
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "Информатика",
                "teacher": "Любоза Александр Александрович"
            },
            {
                "subject": "Математика",
                "teacher": "Верлова Инна Генриховна"
            },
            {
                "subject": "Математика",
                "teacher": "Верлова Инна Генриховна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Верлова Инна Генриховна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Биология",
                "teacher": "Малахова Владислава Сергеевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Пашкевич Ирина Сергеевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Зелинская Ксения Евгеньевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусская литература",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Пашкевич Ирина Сергеевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Зелинская Ксения Евгеньевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Зелинская Ксения Евгеньевна"
            },
            {
                "subject": "Математика",
                "teacher": "Верлова Инна Генриховна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Пашкевич Ирина Сергеевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Всемирная История",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "История",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "Русская литература",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Верлова Инна Генриховна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "7 \"А\"": [
        [
            {
                "subject": "Биология",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Костючкова Инна Станиславовна"
            },
            {
                "subject": "Математика",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Бурехина Татьяна Михайловна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Кублицкая Татьяна Леонидовна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Голубева Ольга Васильевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Лобачева Любовь Валентиновна"
            },
            {
                "subject": "Математика",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Бурехина Татьяна Михайловна"
            },
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Кублицкая Татьяна Леонидовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Трудовое обучение",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Бурехина Татьяна Михайловна"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "Математика",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Лобачева Любовь Валентиновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Трудовое обучение",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Биология",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Лобачева Любовь Валентиновна"
            },
            {
                "subject": "Мировая художественная культура",
                "teacher": "Шальц Римма Акмуратовна"
            },
            {
                "subject": "Информатика",
                "teacher": "Испеньков Андрей Николаевич"
            },
            {
                "subject": "Русский язык",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "7 \"Б\"": [
        [
            {
                "subject": "Белорусский язык",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Козьякова Татьяна Викторовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Ветренникова Александра Сергеевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Ветренникова Александра Сергеевна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Математика",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Биология",
                "teacher": "Быкова Лариса Григорьевна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Математика",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "Биология",
                "teacher": "Быкова Лариса Григорьевна"
            },
            {
                "subject": "Информатика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Козел Тамара Ивановна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русская литература",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Кучко Наталья Вячеславовна"
            },
            {
                "subject": "Математика",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Кучко Наталья Вячеславовна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Козел Тамара Ивановна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Ветренникова Александра Сергеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "7 \"В\"": [
        [
            {
                "subject": "Математика",
                "teacher": "Мурашко Татьяна Семёновна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Матвеев Александр Владимирович"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Мурашко Татьяна Семёновна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Информатика",
                "teacher": "Малистова Елена Анатольевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Копцева Татьяна Павловна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Концова Наталья Владимировна"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Биология",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Концова Наталья Владимировна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Копцева Татьяна Павловна"
            },
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Мурашко Татьяна Семёновна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Биология",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Математика",
                "teacher": "Мурашко Татьяна Семёновна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Шиенок Наталья Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Матвеев Александр Владимирович"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Матвеев Александр Владимирович"
            },
            {
                "subject": "Математика",
                "teacher": "Мурашко Татьяна Семёновна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Концова Наталья Владимировна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "7 \"Г\"": [
        [
            {
                "subject": "Английский язык",
                "teacher": "Головешко Наталья Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Величко Жанна Иосифовна"
            },
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "Биология",
                "teacher": "Солдатова Анна Валерьевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Математика",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Математика",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Головешко Наталья Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "Информатика",
                "teacher": "Любоза Александр Александрович"
            },
            {
                "subject": "Математика",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "История Беларуси",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Биология",
                "teacher": "Солдатова Анна Валерьевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Головешко Наталья Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Величко Жанна Иосифовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "7 \"Д\"": [
        [
            {
                "subject": "Белорусский язык",
                "teacher": "Испенькова Вера Викторовна"
            },
            {
                "subject": "Математика",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Подлужный Никита Сергеевич"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Биология",
                "teacher": "Малахова Владислава Сергеевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "История",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Козьякова Татьяна Викторовна"
            },
            {
                "subject": "Математика",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Информатика",
                "teacher": "Испеньков Андрей Николаевич"
            },
            {
                "subject": "Русский язык",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Подлужный Никита Сергеевич"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Палубец Мария Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Трудовое обучение",
                "teacher": "Козьякова Татьяна Викторовна"
            },
            {
                "subject": "Математика",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Палубец Мария Александровна"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусская литература",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Испенькова Вера Викторовна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Подлужный Никита Сергеевич"
            },
            {
                "subject": "Биология",
                "teacher": "Малахова Владислава Сергеевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Палубец Мария Александровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "7 \"Е\"": [
        [
            {
                "subject": "Информатика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Биология",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Жуков Никита Сергеевич"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Всемирная История",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "История",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Математика",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Биология",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Ильчук Кристина Александровна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Ильчук Кристина Александровна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Чикун Галина Валерьевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Трудовое обучение",
                "teacher": "Дубовик Людмила Георгиевна"
            },
            {
                "subject": "Математика",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Математика",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Математика",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Дубовик Людмила Георгиевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Ильчук Кристина Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "7 \"Ж\"": [
        [
            {
                "subject": "Русский язык",
                "teacher": "Зайковская Юлия Сергеевна"
            },
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Голубева Ольга Васильевна"
            },
            {
                "subject": "Информатика",
                "teacher": "Малистова Елена Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Коробач Екатерина Александровна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Шальц Римма Акмуратовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "История Беларуси",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Голубева Ольга Васильевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Математика",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Биология",
                "teacher": "Быкова Лариса Григорьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Ледник Ирина Леонидовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Зайковская Юлия Сергеевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Биология",
                "teacher": "Быкова Лариса Григорьевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Коробач Екатерина Александровна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Коробач Екатерина Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "8 \"А\"": [
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Стальмаков Сергей Олегович"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Математика",
                "teacher": "Кислая Татьяна Анатольевна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Биология",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Математика",
                "teacher": "Кислая Татьяна Анатольевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "Математика",
                "teacher": "Кислая Татьяна Анатольевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Абесадзе Светлана Валерьевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "История Беларуси",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "Информатика",
                "teacher": "Любоза Александр Александрович"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Аксёнова Антонина Антоновна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Математика",
                "teacher": "Кислая Татьяна Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусская литература",
                "teacher": "Аксёнова Антонина Антоновна"
            },
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Абесадзе Светлана Валерьевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Козлов Сергей Александрович"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русская литература",
                "teacher": "Гурченко Варвара Константиновна"
            },
            {
                "subject": "Математика",
                "teacher": "Кислая Татьяна Анатольевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Стальмаков Сергей Олегович"
            },
            {
                "subject": "Английский язык",
                "teacher": "Абесадзе Светлана Валерьевна"
            },
            {
                "subject": "Биология",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Стальмаков Сергей Олегович"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "8 \"Б\"": [
        [
            {
                "subject": "Белорусская литература",
                "teacher": "Костюкевич Алена Васильевна"
            },
            {
                "subject": "Математика",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Скрабневская Мария Васильевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Горбач Анна Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Батура Алеся Александровна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Горбач Анна Александровна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "Биология",
                "teacher": "Солдатова Анна Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Костючкова Инна Станиславовна"
            },
            {
                "subject": "Математика",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Костюкевич Алена Васильевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Математика",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Скрабневская Мария Васильевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Горбач Анна Александровна"
            },
            {
                "subject": "Информатика",
                "teacher": "Испеньков Андрей Николаевич"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Скрабневская Мария Васильевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Биология",
                "teacher": "Солдатова Анна Валерьевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Величко Жанна Иосифовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Батура Алеся Александровна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "8 \"В\"": [
        [
            {
                "subject": "Английский язык",
                "teacher": "Цыбульская Ольга Валентиновна"
            },
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Информатика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Математика",
                "teacher": "Кореневская Татьяна Леонидовна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Биология",
                "teacher": "Малахова Владислава Сергеевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусский язык",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Кореневская Татьяна Леонидовна"
            },
            {
                "subject": "Биология",
                "teacher": "Малахова Владислава Сергеевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Иванов Владислав Олегович"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Кореневская Татьяна Леонидовна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Иванов Владислав Олегович"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Цыбульская Ольга Валентиновна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Иванов Владислав Олегович"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Козьякова Татьяна Викторовна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Кореневская Татьяна Леонидовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Цыбульская Ольга Валентиновна"
            },
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Математика",
                "teacher": "Кореневская Татьяна Леонидовна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "8 \"Г\"": [
        [
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Зелинская Ксения Евгеньевна"
            },
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусский язык",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Информатика",
                "teacher": "Малистова Елена Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Тарапата Светлана Олеговна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Биология",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Математика",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Тарапата Светлана Олеговна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Испенькова Вера Викторовна"
            },
            {
                "subject": "Биология",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Зелинская Ксения Евгеньевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Испенькова Вера Викторовна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Математика",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Тарапата Светлана Олеговна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Зелинская Ксения Евгеньевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Беднякова Светлана Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "8 \"Д\"": [
        [
            {
                "subject": "Белорусская литература",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Шиенок Наталья Николаевна"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Математика",
                "teacher": "Шедько Ростислав Васильевич"
            },
            {
                "subject": "Информатика",
                "teacher": "Любоза Александр Александрович"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Бурехина Татьяна Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Биология",
                "teacher": "Быкова Лариса Григорьевна"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Математика",
                "teacher": "Шедько Ростислав Васильевич"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Бурехина Татьяна Михайловна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Трудовое обучение",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Бурехина Татьяна Михайловна"
            },
            {
                "subject": "Математика",
                "teacher": "Шедько Ростислав Васильевич"
            },
            {
                "subject": "Русский язык",
                "teacher": "Гурченко Варвара Константиновна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Шиенок Наталья Николаевна"
            },
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Гурченко Варвара Константиновна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Биология",
                "teacher": "Быкова Лариса Григорьевна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Елисеенко Светлана Николаевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Математика",
                "teacher": "Шедько Ростислав Васильевич"
            },
            {
                "subject": "Английский язык",
                "teacher": "Елисеенко Светлана Николаевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Елисеенко Светлана Николаевна"
            },
            {
                "subject": "Математика",
                "teacher": "Шедько Ростислав Васильевич"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "8 \"Ж\"": [
        [
            {
                "subject": "Белорусская литература",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Дятковская Юлия Владимировна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Жуков Никита Сергеевич"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Дятковская Юлия Владимировна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Эдуардовна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русский язык",
                "teacher": "Макаренко Наталья Геннадьевна"
            },
            {
                "subject": "Биология",
                "teacher": "Солдатова Анна Валерьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Эдуардовна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Эдуардовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Эдуардовна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Концова Наталья Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Концова Наталья Владимировна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Батура Алеся Александровна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Макаренко Наталья Геннадьевна"
            },
            {
                "subject": "Биология",
                "teacher": "Солдатова Анна Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Дятковская Юлия Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Эдуардовна"
            },
            {
                "subject": "Информатика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Концова Наталья Владимировна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Чибикова Татьяна Николаевна"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "8 \"З\"": [
        [
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Шальц Римма Акмуратовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Котловская Анастасия Юрьевна"
            },
            {
                "subject": "Биология",
                "teacher": "Малахова Владислава Сергеевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Хандопкина Наталья Анатольевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Котловская Анастасия Юрьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Хандопкина Наталья Анатольевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Салманова Алеся Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Махлова Ирина Владимировна"
            },
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Математика",
                "teacher": "Хандопкина Наталья Анатольевна"
            },
            {
                "subject": "Математика",
                "teacher": "Хандопкина Наталья Анатольевна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "Информатика",
                "teacher": "Малистова Елена Анатольевна"
            },
            {
                "subject": "История",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Сушкова Елизавета Андреевна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Всемирная История",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "Биология",
                "teacher": "Малахова Владислава Сергеевна"
            },
            {
                "subject": "Математика",
                "teacher": "Хандопкина Наталья Анатольевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Котловская Анастасия Юрьевна"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "9 \"А\"": [
        [
            {
                "subject": "История Беларуси",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Информатика",
                "teacher": "Любоза Александр Александрович"
            },
            {
                "subject": "Английский язык",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Базыко Яна Игоревна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Базыко Яна Игоревна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Подлужный Никита Сергеевич"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Костюкевич Алена Васильевна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Костюкевич Алена Васильевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Базыко Яна Игоревна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Подлужный Никита Сергеевич"
            },
            {
                "subject": "Обществоведение",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Биология",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Базыко Яна Игоревна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Подлужный Никита Сергеевич"
            },
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "9 \"Б\"": [
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "Информатика",
                "teacher": "Испеньков Андрей Николаевич"
            },
            {
                "subject": "Биология",
                "teacher": "Быкова Лариса Григорьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Тугаринова Марина Александровна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Дубовик Лариса Юрьевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Тугаринова Марина Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Всемирная История",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Остапчук Ольга Тимофеевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Кучко Наталья Вячеславовна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Новодворская Юлия Николаевна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Русская литература",
                "teacher": "Кучко Наталья Вячеславовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Остапчук Ольга Тимофеевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Костючкова Инна Станиславовна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Остапчук Ольга Тимофеевна"
            },
            {
                "subject": "Математика",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Обществоведение",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "9 \"В\"": [
        [
            {
                "subject": "Английский язык",
                "teacher": "Свирская Екатерина Александровна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Козьякова Татьяна Викторовна"
            },
            {
                "subject": "Информатика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Математика",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Свирская Екатерина Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "История Беларуси",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Андреева Елена Матвеевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Свирская Екатерина Александровна"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Математика",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Математика",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Биология",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Кудря Наталья Валерьяновна"
            },
            {
                "subject": "Обществоведение",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Всемирная История",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "9 \"Г\"": [
        [
            {
                "subject": "Математика",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Жаголкина Александра Анатольевна"
            },
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Жаголкина Александра Анатольевна"
            },
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "Математика",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Стальмаков Сергей Олегович"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Биология",
                "teacher": "Солдатова Анна Валерьевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Вакарева Марина Витальевна"
            },
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Жаголкина Александра Анатольевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Стальмаков Сергей Олегович"
            },
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "Обществоведение",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Аксёнова Антонина Антоновна"
            },
            {
                "subject": "Информатика",
                "teacher": "Малистова Елена Анатольевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Денисенко Сергей Викторович"
            },
            {
                "subject": "Физика",
                "teacher": "Старовойтова Татьяна Геннадьевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Быстрова Татьяна Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Семёнова Ирина Ивановна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Аксёнова Антонина Антоновна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Стальмаков Сергей Олегович"
            },
            {
                "subject": "Белорусская литература",
                "teacher": "Кублицкая Татьяна Леонидовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "9 \"Д\"": [
        [
            {
                "subject": "Информатика",
                "teacher": "Любоза Александр Александрович"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Чикун Галина Валерьевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Шенделова Инна Викторовна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Скрабневская Мария Васильевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Пыльская Наталья Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Математика",
                "teacher": "Шенделова Инна Викторовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Беднякова Светлана Владимировна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Мороз Светлана Сергеевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусский язык",
                "teacher": "Чикун Галина Валерьевна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Скрабневская Мария Васильевна"
            },
            {
                "subject": "География",
                "teacher": "Саникович Жанна Петровна"
            },
            {
                "subject": "Обществоведение",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Скрабневская Мария Васильевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Мороз Светлана Сергеевна"
            },
            {
                "subject": "Химия",
                "teacher": "Карполенко Ксения Олеговна"
            },
            {
                "subject": "Физика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Математика",
                "teacher": "Шенделова Инна Викторовна"
            },
            {
                "subject": "Биология",
                "teacher": "Малахова Владислава Сергеевна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Барановская Валерия Сергеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусская литература",
                "teacher": "Савченко Светлана Владимировна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Мороз Светлана Сергеевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Беднякова Светлана Владимировна"
            },
            {
                "subject": "Мировая художественная культура",
                "teacher": "Козьякова Татьяна Викторовна"
            },
            {
                "subject": "Математика",
                "teacher": "Шенделова Инна Викторовна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "9 \"Е\"": [
        [
            {
                "subject": "Русский язык",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Иванов Владислав Олегович"
            },
            {
                "subject": "История",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Макаренко Наталья Геннадьевна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Пашкевич Ирина Сергеевна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Савченко Светлана Владимировна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Пашкевич Ирина Сергеевна"
            },
            {
                "subject": "Химия",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусская литература",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Рябова Наталья Леонидовна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Макаренко Наталья Геннадьевна"
            },
            {
                "subject": "Математика",
                "teacher": "Конофальская Елена Николаевна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Иванов Владислав Олегович"
            },
            {
                "subject": "Математика",
                "teacher": "Конофальская Елена Николаевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Всемирная История",
                "teacher": "Ганзиенко Елена Владимировна"
            },
            {
                "subject": "Обществоведение",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Математика",
                "teacher": "Конофальская Елена Николаевна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Мурадова Анастасия Руслановна"
            },
            {
                "subject": "Биология",
                "teacher": "Стефановская Арина Игоревна"
            },
            {
                "subject": "Физика",
                "teacher": "Киравницина Инна Иосифовна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Пашкевич Ирина Сергеевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Информатика",
                "teacher": "Испеньков Андрей Николаевич"
            },
            {
                "subject": "Математика",
                "teacher": "Конофальская Елена Николаевна"
            },
            {
                "subject": "География",
                "teacher": "Петрова Оксана Геннадьевна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Осипук Леонид Аркадьевич"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Савченко Светлана Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Иванов Владислав Олегович"
            },
            {
                "subject": "Русский язык",
                "teacher": "Крученкова-Зиновьева Светлана Фёдоровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ],
    "9 \"Ж\"": [
        [
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "Искусство. Отечественная и мировая художественная культура",
                "teacher": "Жуков Никита Сергеевич"
            },
            {
                "subject": "Математика",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Математика",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Зелинская Ксения Евгеньевна"
            },
            {
                "subject": "Обществоведение",
                "teacher": "Морозова Елена Александровна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Математика",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Зелинская Ксения Евгеньевна"
            },
            {
                "subject": "Химия",
                "teacher": "Журомская Ольга Леонидовна"
            },
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Белорусская литература",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "История Беларуси",
                "teacher": "Черняева Алеся Михайловна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Математика",
                "teacher": "Давыдько Инна Владимировна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Лобачева Любовь Валентиновна"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "Русский язык",
                "teacher": "Смолова Ирина Владимировна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Биология",
                "teacher": "Быкова Лариса Григорьевна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "География",
                "teacher": "Самарина Марина Владимировна"
            },
            {
                "subject": "Физическая культура и здоровье",
                "teacher": "Зелинская Ксения Евгеньевна"
            },
            {
                "subject": "Всемирная История",
                "teacher": "Майоров Дмитрий Анатольевич"
            },
            {
                "subject": "Белорусский язык",
                "teacher": "Ефимчик Елена Валерьевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ],
        [
            {
                "subject": "Английский язык",
                "teacher": "Лобачева Любовь Валентиновна"
            },
            {
                "subject": "Английский язык",
                "teacher": "Лобачева Любовь Валентиновна"
            },
            {
                "subject": "Физика",
                "teacher": "Ткачева Анна Леонидовна"
            },
            {
                "subject": "Трудовое обучение",
                "teacher": "Ревяко Елена Аркадьевна"
            },
            {
                "subject": "Информатика",
                "teacher": "Спиридонова Наталья Викторовна"
            },
            {
                "subject": "Русская литература",
                "teacher": "Ермакович Жанна Анатольевна"
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            },
            {
                "subject": "#",
                "teacher": ""
            }
        ]
    ]
}

            self.classes = sorted(self.data.keys())
            self.class_combo['values'] = self.classes
            if self.classes:
                self.class_var.set(self.classes[0])
                self.show_schedule()  # сразу показываем расписание для первого класса
        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл '{filepath}' не найден.\nПроверьте путь в переменной FILE_PATH.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
            self.data = None

    def show_schedule(self):
        # Очищаем предыдущую таблицу
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.data:
            messagebox.showwarning("Нет данных", "Сначала загрузите файл с расписанием.")
            return

        selected_class = self.class_var.get()
        if not selected_class:
            messagebox.showwarning("Нет выбора", "Выберите класс.")
            return

        if selected_class not in self.data:
            messagebox.showerror("Ошибка", f"Класс '{selected_class}' не найден в данных.")
            return

        schedule = self.data[selected_class]   # список дней, каждый день – список уроков
        if not schedule:
            messagebox.showinfo("Информация", f"Для класса {selected_class} расписание пустое.")
            return

        num_days = len(schedule)
        max_lessons = max((len(day) for day in schedule), default=0)

        # ======= ПЕРЕВЁРНУТАЯ ТАБЛИЦА =======
        # Заголовки: "День" + номера уроков (1, 2, ...)
        headers = ["День"] + [f"Урок {i+1}" for i in range(max_lessons)]

        header_font = tkfont.Font(weight="bold", size=10)
        cell_font = tkfont.Font(size=9)

        # Заголовки (первая строка)
        for col, header in enumerate(headers):
            label = tk.Label(self.scrollable_frame, text=header, font=header_font,
                             relief="ridge", padx=5, pady=5, bg="#d9d9d9",
                             width=12, wraplength=100)
            label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        # Данные по дням (строки)
        for day_idx in range(num_days):
            day_data = schedule[day_idx]
            # Название дня
            day_label = tk.Label(self.scrollable_frame, text=f"День {day_idx+1}", font=header_font,
                                 relief="ridge", padx=5, pady=5, bg="#f0f0f0")
            day_label.grid(row=day_idx+1, column=0, sticky="nsew", padx=1, pady=1)

            # Уроки этого дня
            for lesson_idx in range(max_lessons):
                if lesson_idx < len(day_data):
                    lesson = day_data[lesson_idx]
                    subject = lesson.get("subject", "")
                    teacher = lesson.get("teacher", "")
                    if subject == "#":
                        text = ""
                    else:
                        text = f"{subject}\n{teacher}" if teacher else subject
                else:
                    text = ""

                label = tk.Label(self.scrollable_frame, text=text, font=cell_font,
                                 relief="ridge", padx=5, pady=5, bg="white",
                                 justify="center", wraplength=100)
                label.grid(row=day_idx+1, column=lesson_idx+1, sticky="nsew", padx=1, pady=1)

        # Растяжение
        for col in range(len(headers)):
            self.scrollable_frame.grid_columnconfigure(col, weight=1)
        for row in range(num_days + 1):
            self.scrollable_frame.grid_rowconfigure(row, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()
