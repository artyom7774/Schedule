from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5.QtCore import Qt


class MultiTableWidget(QTableWidget):
    def __init__(self, rows, cols, parent=None):
        super().__init__(rows, cols, parent)

        self.blockSignals(True)

        for r in range(rows):
            for c in range(cols):
                self.setItem(r, c, QTableWidgetItem("0"))

        self.blockSignals(False)

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
