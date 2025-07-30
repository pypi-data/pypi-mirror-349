import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QLineEdit, QVBoxLayout, QLabel, QWidget, QMainWindow, QMessageBox, QComboBox, \
    QApplication, QDateTimeEdit, QCheckBox, QDateEdit

from db.helpers import get_columns, get_foreign_key_info, get_column_info
from db.mysql_connection import update, select


class AddRowDialog(QMainWindow):
    def __init__(self, tablename: str, parent: QWidget = None):
        super().__init__(parent)
        self.tablename = tablename
        self.columns = get_columns(self.tablename)

        self.setWindowTitle(f"Добавить {tablename}")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        self.fields = self.create_fields_for_columns(self.columns)

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.save)
        self.layout.addWidget(self.add_btn)

        self.setLayout(self.layout)

    def _quote_value(self, value: str) -> str:
        value = str(value)
        if value.isdigit():
            return value
        return f"'{value}'"

    def save(self):
        columns = []
        values = []
        for column, widget in self.fields.items():
            value = ""
            if type(widget) is QLineEdit:
                widget: QLineEdit
                value = self._quote_value(widget.text())
            elif type(widget) is QComboBox:
                widget: QComboBox
                value = self._quote_value(widget.currentData())
            elif type(widget) is QDateEdit:
                widget: QDateEdit
                value = f"STR_TO_DATE('{widget.text()}', '%d.%m.%Y')"
            elif type(widget) is QDateTimeEdit:
                widget: QDateTimeEdit
                value = f"STR_TO_DATE('{widget.text()}', '%d.%m.%Y %H:%i')"

            if value:
                columns.append(column)
                values.append(value)

        query = (f"INSERT INTO {self.tablename} ({', '.join(columns)}) "
                 f"VALUES ({', '.join(values)})")
        try:
            update(query)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при попытке сохранения", str(e))
            return
        self.parent().load_data()
        self.close()

    def create_fields_for_columns(self, columns: list[str]) -> dict[str, QLineEdit]:
        widgets = dict()

        for column in columns:
            if column == "id":
                continue
            self.layout.addWidget(QLabel(f"{column}:"))
            widget = QLineEdit()
            column_info = get_column_info(self.tablename, column)
            if column_info["COLUMN_KEY"]=="MUL":
                widget = QComboBox()
                ref_table, ref_pk = get_foreign_key_info(self.tablename, column)
                ref_name_col = get_columns(ref_table)[1]
                values = select(f"SELECT {ref_pk}, {ref_name_col} FROM {ref_table}")
                for value in values:
                    widget.addItem(value[ref_name_col], value[ref_pk])
            elif column_info["COLUMN_TYPE"] == "date":
                widget = QDateEdit()
                widget.setCalendarPopup(True)
            elif column_info["COLUMN_TYPE"] in ["datetime", "timestamp"]:
                widget = QDateTimeEdit()
                widget.setCalendarPopup(True)

            widgets[column] = widget
            self.layout.addWidget(widgets[column])

        return widgets

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddRowDialog("cart")
    window.show()
    sys.exit(app.exec())