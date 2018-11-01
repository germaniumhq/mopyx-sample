import sys

from PySide2.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from mopyx import model, render, render_call, action

from mopyx_sample.ui.Ui_MainWindow import Ui_MainWindow


@model
class RootModel:
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.items = []

        self.selectedItemIndex = -1


root_model = RootModel()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()

        self.setupUi(self)

        self.update_from_model()
        self.wire_ui_signals()

    def wire_ui_signals(self):
        self.first_name_edit.textEdited.connect(self.set_first_name)
        self.last_name_edit.textEdited.connect(self.set_last_name)

        self.items_table.itemSelectionChanged.connect(self.set_selected_item_index)

        self.item_button_add.clicked.connect(self.add_item)
        self.item_button_move_up.clicked.connect(self.move_up_item)
        self.item_button_move_down.clicked.connect(self.move_down_item)
        self.item_button_delete.clicked.connect(self.delete_item)

    @render
    def update_from_model(self):
        render_call(
            lambda: self.full_name_label.setText(
                f"{root_model.first_name} {root_model.last_name}"))

        self.update_table_items()
        self.update_buttons()

    @render(ignore_updates=True)
    def update_table_items(self):
        self.items_table.setRowCount(len(root_model.items))
        self.items_table.setColumnCount(1)

        for i in range(len(root_model.items)):
            self.items_table.setItem(i, 0, QTableWidgetItem(root_model.items[i]))

        render_call(lambda: self.items_table.setCurrentCell(root_model.selectedItemIndex, 0),
                    ignore_updates=True)

        if root_model.items:
            self.selected_items_label.setText(f"Items are: {', '.join(root_model.items)}")
        else:
            self.selected_items_label.setText("There are no items")

    @render(ignore_updates=True)
    def update_buttons(self):
        self.item_button_move_up.setEnabled(root_model.selectedItemIndex > 0)
        self.item_button_move_down.setEnabled(
            root_model.selectedItemIndex < len(root_model.items) - 1 and root_model.selectedItemIndex >= 0)
        self.item_button_delete.setEnabled(root_model.selectedItemIndex >= 0)

    @action
    def set_selected_item_index(self):
        root_model.selectedItemIndex = self.items_table.currentRow()

    def add_item(self):
        root_model.items.append(self.item_name_edit.text())
        self.item_name_edit.setText("")

    @action
    def move_up_item(self):
        swap = root_model.items[root_model.selectedItemIndex - 1]
        root_model.items[root_model.selectedItemIndex - 1] = root_model.items[root_model.selectedItemIndex]
        root_model.items[root_model.selectedItemIndex] = swap
        root_model.selectedItemIndex -= 1

    @action
    def move_down_item(self):
        swap = root_model.items[root_model.selectedItemIndex + 1]
        root_model.items[root_model.selectedItemIndex + 1] = root_model.items[root_model.selectedItemIndex]
        root_model.items[root_model.selectedItemIndex] = swap
        root_model.selectedItemIndex += 1

    @action
    def delete_item(self):
        del root_model.items[root_model.selectedItemIndex]
        root_model.selectedItemIndex -= 1

    def set_last_name(self, value):
        root_model.last_name = value

    def set_first_name(self, value):
        root_model.first_name = value


def main():
    app = QApplication(sys.argv)
    MainWindow().show()

    ret = app.exec_()
    sys.exit(ret)


if __name__ == '__main__':
    main()
