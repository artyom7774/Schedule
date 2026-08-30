from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QScrollArea, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtCore import pyqtSignal, QEvent, Qt

from src.variables import *


class ButtonGridWidget(QWidget):
    buttonClicked = pyqtSignal(str)
    buttonClickedIndex = pyqtSignal(int)

    def __init__(self, labels=None, min_cols=1, padding=(16, 10), parent=None, onClick=None, on_click_with_index=False):
        super().__init__(parent)

        self.min_cols = min_cols
        self.h_pad, self.v_pad = padding
        self.spacing = 2

        self.buttons = []
        self.labels = []
        self.cols = min_cols
        self.btn_width = 44
        self.btn_height = 26

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        self._grid_container = QWidget()
        self._grid_layout = QGridLayout(self._grid_container)
        self._grid_layout.setSpacing(self.spacing)
        self._grid_layout.setContentsMargins(4, 4, 4, 4)
        self._grid_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setWidget(self._grid_container)
        self._scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        outer_layout.addWidget(self._scroll_area)

        self._scroll_area.viewport().installEventFilter(self)

        self._on_click_callback = None
        self._on_click_with_index = False

        if onClick is not None:
            self.set_on_click(onClick, on_click_with_index)

        if labels:
            self.set_labels(labels)

    def set_labels(self, labels):
        self.labels = list(labels)
        self._calc_button_size()
        self._rebuild_buttons()
        self._relayout(force=True)

    def add_button(self, label):
        self.labels.append(label)
        old_width = self.btn_width
        self._calc_button_size()

        if self.btn_width != old_width:
            self._rebuild_buttons()

        else:
            btn = self._make_button(label, len(self.buttons))
            self.buttons.append(btn)

        self._relayout(force=True)

        return self.buttons[-1]

    def clear(self):
        self._clear_layout()

        self.buttons = []
        self.labels = []

    def get_button(self, index):
        return self.buttons[index]

    def set_enabled_by_index(self, index, enabled=True):
        self.buttons[index].setEnabled(enabled)

    def set_button_style(self, index, stylesheet):
        self.buttons[index].setStyleSheet(stylesheet)

    def count(self):
        return len(self.buttons)

    def set_on_click(self, callback, with_index=False):
        if self._on_click_callback is not None:
            if self._on_click_with_index:
                self.buttonClickedIndex.disconnect(self._on_click_callback)

            else:
                self.buttonClicked.disconnect(self._on_click_callback)

        self._on_click_callback = callback
        self._on_click_with_index = with_index

        if with_index:
            self.buttonClickedIndex.connect(callback)

        else:
            self.buttonClicked.connect(callback)

    def _calc_button_size(self):
        metrics = QFontMetrics(FONT)

        if self.labels:
            max_text_width = max(metrics.horizontalAdvance(text) for text in self.labels)

        else:
            max_text_width = 0

        self.btn_width = max_text_width + self.h_pad
        self.btn_height = metrics.height() + self.v_pad

    def _make_button(self, label, index):
        btn = QPushButton(label)
        btn.setFixedSize(self.btn_width, self.btn_height)
        btn.setFont(FONT)
        btn.clicked.connect(lambda _, l=label, i=index: self._on_click(l, i))

        return btn

    def _clear_layout(self):
        while self._grid_layout.count():
            item = self._grid_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def _rebuild_buttons(self):
        self._clear_layout()

        self.buttons = [self._make_button(label, i) for i, label in enumerate(self.labels)]

    def _calc_cols(self):
        available = self._scroll_area.viewport().width()
        margins = self._grid_layout.contentsMargins()
        available -= margins.left() + margins.right()

        cell = self.btn_width + self.spacing

        if cell <= 0:
            return self.min_cols

        cols = available // cell

        return max(self.min_cols, int(cols))

    def _relayout(self, force=False):
        new_cols = self._calc_cols()

        if not force and new_cols == self.cols:
            return

        self.cols = new_cols

        for i in reversed(range(self._grid_layout.count())):
            self._grid_layout.takeAt(i)

        for index, btn in enumerate(self.buttons):
            row, col = divmod(index, self.cols)
            self._grid_layout.addWidget(btn, row, col)

    def eventFilter(self, obj, event):
        if obj is self._scroll_area.viewport() and event.type() == QEvent.Resize:
            self._relayout()

        return super().eventFilter(obj, event)

    def _on_click(self, label, index):
        self.buttonClicked.emit(label)
        self.buttonClickedIndex.emit(index)
