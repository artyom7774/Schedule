from PyQt5.QtWidgets import QWidget, QListWidget, QPushButton, QMenu, QAction
from PyQt5.QtCore import Qt

from src.modules import dialogs

from src.variables import *


class TabClassrooms(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window

        self.enablePushButton = QPushButton(parent=self)
        code = "enable" if self.window.settings["classrooms"]["enable"] else "disable"
        self.enablePushButton.setText(f"{translate('menu.main.tab.classrooms.classrooms')}: {translate(f'menu.main.tab.classrooms.{code}')}")
        self.enablePushButton.setFont(FONT)
        self.enablePushButton.show()

        if self.window.settings["classrooms"]["enable"]:
            self.enablePushButton.setStyleSheet(f"QPushButton {{ background: #109012; }}")

        else:
            self.enablePushButton.setStyleSheet(f"QPushButton {{ background: #901112; }}")

        self.enablePushButton.clicked.connect(lambda: self.enablePushButtonClickedConnect())

        groups = list(self.window.settings["classrooms"]["rooms"].keys())

        self.roomGroupsListWidget = QListWidget(parent=self)
        self.roomGroupsListWidget.itemClicked.connect(lambda item: self.roomGroupsItemClicked(item))
        self.roomGroupsListWidget.addItems(groups)

        self.roomGroupsListWidget.setFont(FONT)
        self.roomGroupsListWidget.show()

        self.roomGroupsListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.roomGroupsListWidget.customContextMenuRequested.connect(lambda pos: self.showContextMenu(pos))

        group = self.window.objects.get("classrooms_selected")

        if group in groups:
            self.roomGroupsListWidget.setCurrentRow(groups.index(group))

        self.createGroupPushButton = QPushButton(parent=self)
        self.createGroupPushButton.clicked.connect(lambda: self.createGroupPushButtonClicked())
        self.createGroupPushButton.setText(translate("menu.main.tab.classrooms.add_group"))
        self.createGroupPushButton.setFont(FONT)
        self.createGroupPushButton.show()

        self.roomsListWidget = QListWidget(parent=self)
        self.roomsListWidget.setFont(FONT)
        self.roomsListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.roomsListWidget.customContextMenuRequested.connect(lambda pos: self.showRoomsContextMenu(pos))

        if group and group in self.window.settings["classrooms"]["rooms"]:
            self.roomsListWidget.addItems(self.window.settings["classrooms"]["rooms"][group])

        self.roomsListWidget.show()

        scroll = self.window.objects.get("classrooms_scroll", 0)
        self.roomsListWidget.verticalScrollBar().setValue(scroll)

        self.addRoomPushButton = QPushButton(parent=self)
        self.addRoomPushButton.setText(translate("menu.main.tab.classrooms.add_classroom"))
        self.addRoomPushButton.setFont(FONT)
        self.addRoomPushButton.clicked.connect(lambda: self.addRoomPushButtonClicked())
        self.addRoomPushButton.setEnabled(bool(group))
        self.addRoomPushButton.show()

    def enablePushButtonClickedConnect(self):
        self.window.settings["classrooms"]["enable"] = 1 - self.window.settings["classrooms"]["enable"]

        TabClassrooms.init(self.window, ignore=[TAB_CLASSROOMS, TAB_TEACHERS], reverse=True)

    def roomGroupsItemClicked(self, item):
        self.window.objects["classrooms_selected"] = item.text()
        self.window.objects["classrooms_scroll"] = 0

        TabClassrooms.init(self.window, ignore=[TAB_CLASSROOMS, TAB_TEACHERS], reverse=True)

    def createGroupPushButtonClicked(self):
        title = translate("dialog.add_classroom_group.title")
        label = translate("dialog.add_classroom_group.label")
        allow = translate("dialog.add_classroom_group.allow")

        self.window.dialog = dialogs.TextInputDialog(self.window, title, label, allow, lambda: self.createGroup())
        self.window.dialog.exec()

    def createGroup(self):
        name = self.window.dialog.edit.text()

        if name == "":
            self.window.dialog.log.setText(translate("log.text.teacher_name_is_empty"))

            return

        if name in self.window.settings["classrooms"]["rooms"]:
            self.window.dialog.log.setText(translate("log.text.group_name_already_exists"))

            return

        self.window.settings["classrooms"]["rooms"][name] = []

        self.window.dialog.close()

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        TabClassrooms.init(self.window, ignore=[TAB_CLASSROOMS, TAB_TEACHERS], reverse=True)

    def showContextMenu(self, pos):
        item = self.roomGroupsListWidget.itemAt(pos)

        if item is None:
            return

        menu = QMenu(self)

        delete = QAction(translate("menu.main.tab.classrooms.delete"), self)
        delete.triggered.connect(lambda: self.roomGroupDeleteElement(item))

        menu.addAction(delete)

        menu.exec_(self.roomGroupsListWidget.mapToGlobal(pos))

    def roomGroupDeleteElement(self, item):
        remove = item.text()

        self.window.settings["classrooms"]["rooms"].pop(remove)

        if self.window.objects.get("classrooms_selected") == remove:
            self.window.objects.pop("classrooms_selected", None)

        self.window.objects.pop("classrooms_scroll", None)

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        TabClassrooms.init(self.window, ignore=[TAB_CLASSROOMS, TAB_TEACHERS], reverse=True)

    def addRoomPushButtonClicked(self):
        group = self.window.objects.get("classrooms_selected")

        if not group:
            return

        title = translate("dialog.add_classroom.title")
        label = translate("dialog.add_classroom.label")
        allow = translate("dialog.add_classroom.allow")

        self.window.dialog = dialogs.TextInputDialog(self.window, title, label, allow, lambda: self.addRoom())
        self.window.dialog.exec()

    def addRoom(self):
        group = self.window.objects.get("classrooms_selected")

        if not group:
            self.window.dialog.close()

            return

        name = self.window.dialog.edit.text()

        if name == "":
            self.window.dialog.log.setText(translate("log.text.classroom_name_is_empty"))

            return

        if name in self.window.settings["classrooms"]["rooms"][group]:
            self.window.dialog.log.setText(translate("log.text.classroom_name_already_exists"))

            return

        self.window.settings["classrooms"]["rooms"][group].append(name)

        self.window.dialog.close()

        self.window.objects["classrooms_scroll"] = self.roomsListWidget.verticalScrollBar().value()
        self.window.objects["classrooms_selected"] = group

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        TabClassrooms.init(self.window, ignore=[TAB_CLASSROOMS, TAB_TEACHERS], reverse=True)

    def showRoomsContextMenu(self, pos):
        group = self.window.objects.get("classrooms_selected")

        if not group:
            return

        item = self.roomsListWidget.itemAt(pos)

        if item is None:
            return

        menu = QMenu(self)

        delete = QAction(translate("menu.main.tab.classrooms.delete"), self)
        delete.triggered.connect(lambda: self.roomDeleteElement(item))

        menu.addAction(delete)

        menu.exec_(self.roomsListWidget.mapToGlobal(pos))

    def roomDeleteElement(self, item):
        group = self.window.objects.get("classrooms_selected")

        if not group:
            return

        remove = item.text()

        self.window.settings["classrooms"]["rooms"][group].remove(remove)

        self.window.objects["classrooms_scroll"] = self.roomsListWidget.verticalScrollBar().value()
        self.window.objects["classrooms_selected"] = group

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        TabClassrooms.init(self.window, ignore=[TAB_CLASSROOMS, TAB_TEACHERS], reverse=True)
