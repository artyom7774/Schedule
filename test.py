#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой чат с ИИ на PyQt5.

Установка зависимостей:
    pip install PyQt5 requests

Запуск:
    python ai_chat.py

Использует OpenRouter (OpenAI-совместимый эндпоинт chat/completions).
При первом запуске приложение попросит ввести API-ключ.
Ключ можно также задать заранее через переменную окружения
OPENROUTER_API_KEY.
"""

import os
import sys
import json

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QInputDialog,
    QMessageBox,
    QAction,
    QActionGroup,
    QLineEdit as QLE,
)

import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY_ENV_VAR = "OPENROUTER_API_KEY"

# Доступные модели (можно расширить своим списком)
MODELS = [
    "z-ai/glm-5.3-flash",
]


class ChatWorker(QThread):
    """Отдельный поток для запроса к API, чтобы не подвешивать интерфейс."""

    finished_ok = pyqtSignal(str)
    finished_err = pyqtSignal(str)

    def __init__(self, api_key, model, messages, parent=None):
        super().__init__(parent)
        self.api_key = api_key
        self.model = model
        self.messages = messages

    def run(self):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost",
            "X-Title": "PyQt5 AI Chat",
        }
        payload = {
            "model": self.model,
            "messages": self.messages,
            "stream": False,
        }
        try:
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=110)
            data = resp.json()
            if resp.status_code != 200:
                err_msg = data.get("error", {}).get("message", json.dumps(data))
                self.finished_err.emit(f"Ошибка API ({resp.status_code}): {err_msg}")
                return

            # Формат OpenAI-совместимого API: choices[0].message.content
            choices = data.get("choices", [])
            if not choices:
                self.finished_err.emit(f"Неожиданный формат ответа: {json.dumps(data)}")
                return
            answer = choices[0].get("message", {}).get("content", "")
            self.finished_ok.emit(answer or "(пустой ответ)")
        except requests.exceptions.RequestException as e:
            self.finished_err.emit(f"Ошибка сети: {e}")
        except Exception as e:
            self.finished_err.emit(f"Неожиданная ошибка: {e}")


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Чат с ИИ")
        self.resize(700, 600)

        self.api_key = os.environ.get(API_KEY_ENV_VAR, "")
        self.current_model = MODELS[0]
        self.history = []  # список сообщений в формате Anthropic API
        self.worker = None

        self._build_ui()
        self._build_menu()

        if not self.api_key:
            self._ask_api_key()

    # ---------- UI ----------

    def _build_ui(self):
        central = QWidget()
        layout = QVBoxLayout(central)

        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        self.chat_view.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.chat_view)

        self.status_label = QLabel(f"Модель: {self.current_model}")
        self.status_label.setStyleSheet("color: gray;")
        layout.addWidget(self.status_label)

        input_row = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Введите сообщение и нажмите Enter...")
        self.input_line.returnPressed.connect(self.send_message)
        input_row.addWidget(self.input_line)

        self.send_button = QPushButton("Отправить")
        self.send_button.clicked.connect(self.send_message)
        input_row.addWidget(self.send_button)

        layout.addLayout(input_row)
        self.setCentralWidget(central)

    def _build_menu(self):
        menu_bar = self.menuBar()

        # --- Меню "Файл" ---
        file_menu = menu_bar.addMenu("Файл")

        clear_action = QAction("Очистить чат", self)
        clear_action.triggered.connect(self.clear_chat)
        file_menu.addAction(clear_action)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # --- Меню "Настройки" ---
        settings_menu = menu_bar.addMenu("Настройки")

        api_key_action = QAction("Задать API-ключ...", self)
        api_key_action.triggered.connect(self._ask_api_key)
        settings_menu.addAction(api_key_action)

        model_menu = settings_menu.addMenu("Модель")
        model_group = QActionGroup(self)
        model_group.setExclusive(True)
        for model_name in MODELS:
            action = QAction(model_name, self, checkable=True)
            action.setChecked(model_name == self.current_model)
            action.triggered.connect(
                lambda checked, m=model_name: self._set_model(m)
            )
            model_group.addAction(action)
            model_menu.addAction(action)

        custom_model_action = QAction("Своя модель...", self)
        custom_model_action.triggered.connect(self._ask_custom_model)
        settings_menu.addAction(custom_model_action)

    # ---------- Действия ----------

    def _ask_api_key(self):
        key, ok = QInputDialog.getText(
            self,
            "API-ключ",
            f"Введите API-ключ (или задайте переменную окружения {API_KEY_ENV_VAR}):",
            QLE.Password,
            self.api_key,
        )
        if ok and key.strip():
            self.api_key = key.strip()

    def _ask_custom_model(self):
        model, ok = QInputDialog.getText(
            self, "Своя модель", "Введите название модели:", QLE.Normal, self.current_model
        )
        if ok and model.strip():
            self._set_model(model.strip())

    def _set_model(self, model_name):
        self.current_model = model_name
        self.status_label.setText(f"Модель: {self.current_model}")

    def clear_chat(self):
        self.history = []
        self.chat_view.clear()

    def append_message(self, role_label, text, color):
        self.chat_view.moveCursor(QTextCursor.End)
        self.chat_view.append(
            f'<p><b style="color:{color};">{role_label}:</b> {self._escape(text)}</p>'
        )
        self.chat_view.moveCursor(QTextCursor.End)

    @staticmethod
    def _escape(text):
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )

    def send_message(self):
        text = self.input_line.text().strip()
        if not text:
            return

        if not self.api_key:
            QMessageBox.warning(self, "Нет API-ключа", "Сначала задайте API-ключ в меню «Настройки».")
            return

        self.append_message("Вы", text, "#1a73e8")
        self.history.append({"role": "user", "content": text})
        self.input_line.clear()
        self._set_inputs_enabled(False)
        self.status_label.setText(f"Модель: {self.current_model} — ожидание ответа...")

        self.worker = ChatWorker(self.api_key, self.current_model, self.history)
        self.worker.finished_ok.connect(self._on_answer)
        self.worker.finished_err.connect(self._on_error)
        self.worker.start()

    def _on_answer(self, answer):
        self.append_message("ИИ", answer, "#188038")
        self.history.append({"role": "assistant", "content": answer})
        self.status_label.setText(f"Модель: {self.current_model}")
        self._set_inputs_enabled(True)

    def _on_error(self, error_text):
        self.append_message("Ошибка", error_text, "#d93025")
        # убираем последнее сообщение пользователя, чтобы не портить историю
        if self.history and self.history[-1]["role"] == "user":
            self.history.pop()
        self.status_label.setText(f"Модель: {self.current_model}")
        self._set_inputs_enabled(True)

    def _set_inputs_enabled(self, enabled):
        self.input_line.setEnabled(enabled)
        self.send_button.setEnabled(enabled)
        if enabled:
            self.input_line.setFocus()


def main():
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()