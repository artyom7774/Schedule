from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit, QHeaderView
from PyQt5.QtCore import Qt


class MultiTableWidget(QTableWidget):
    def __init__(self, rows, cols, parent=None):
        super().__init__(rows, cols, parent)

        self.blockSignals(True)

        for c in range(cols):
            for r in range(rows):
                self.setItem(r, c, QTableWidgetItem("0"))

        self.blockSignals(False)

        self.setStyleSheet("""QHeaderView::section { padding-right: 8px; }""")

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setFixedWidth(self.columnWidth(0))

        def sync(index, old, new):
            if index == 0:
                self.verticalHeader().setFixedWidth(new)

        self.horizontalHeader().sectionResized.connect(sync)

        self.itemChanged.connect(self.changed)

        self.updating = False
        self.editor = False

    def setHeaderLabelsWithTooltip(self, labels):
        self.setHorizontalHeaderLabels(labels)

        for col, text in enumerate(labels):
            header = self.horizontalHeaderItem(col)

            if header is not None:
                header.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                header.setToolTip(text)

    def closeEditor(self, editor, hint):
        item = self.currentItem()
        value = editor.text() if isinstance(editor, QLineEdit) else None

        self.editor = True

        super().closeEditor(editor, hint)

        self.editor = False

        if value is not None and item is not None and item in self.selectedItems() and len(self.selectedItems()) > 1:
            self.apply(value, item)

    def changed(self, item):
        if self.updating or self.editor:
            return

        if item not in self.selectedItems() or len(self.selectedItems()) <= 1:
            return

        self.apply(item.text(), item)

    def apply(self, value, source):
        if self.updating:
            return

        self.updating = True
        self.blockSignals(True)

        for it in self.selectedItems():
            it.setText(value)

        self.blockSignals(False)
        self.updating = False

        self.cellChanged.emit(source.row(), source.column())
