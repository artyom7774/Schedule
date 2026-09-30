from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from src.variables import *


class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle(translate("dialog.about.title"))
        self.setFixedSize(600, 400)

        layout = QVBoxLayout(self)

        label = QLabel('Супер<span style="color: #4a7dff";">Завуч</span>')
        label.setAlignment(Qt.AlignCenter)
        label.setFont(BIG_FONT)

        layout.addWidget(label)

        links = [
            (f"{translate('dialog.about.site')}:", "https://superzavych.pythonanywhere.com/", "https://superzavych.pythonanywhere.com/"),
            (f"{translate('dialog.about.github')}:", "https://github.com/artyom7774/Schedule", "https://github.com/artyom7774/Schedule"),
            (f"{translate('dialog.about.telegram')}:", "https://t.me/superzavych", "https://t.me/superzavych"),
        ]

        for prefix, url, text in links:
            label = QLabel(f'{prefix} <a href="{url}">{text}</a>', self)

            label.setFont(FONT)
            label.setOpenExternalLinks(True)
            label.setTextInteractionFlags(Qt.TextBrowserInteraction)

            layout.addWidget(label)

        layout.addStretch()
