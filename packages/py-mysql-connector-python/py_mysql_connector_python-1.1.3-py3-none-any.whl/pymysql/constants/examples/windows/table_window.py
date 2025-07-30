import os
from dataclasses import dataclass
from typing import List, Callable, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QMainWindow, QMessageBox, QTableWidgetItem,
                             QTableWidget, QPushButton, QLabel, QApplication, QWidget)

from db.helpers import get_columns
from db.mysql_connection import select, update
from interface.table_window_ui import Ui_TableWindow
from settings import settings
from windows.add_row_dialog import AddRowDialog

ButtonFunc = Callable[[QWidget, int, str], None]


@dataclass
class JoinClause:
    tablename: str
    pk: str
    join_query: str
    columns: List[str]


class TableWindow(QMainWindow, Ui_TableWindow):
    def __init__(self, main_table: str,
                 parent: QMainWindow = None, user_id: int = None,
                 columns: List[str] = None, button_func: ButtonFunc = None,
                 joins: List[JoinClause] = None, where_expression: Optional[str] = None,
                 can_edit=False, can_delete=False, can_add=False, ):
        """
        Универсальный класс для отображения столбцов из бд и их редактирования

        :param main_table: название основной таблицы
        :param parent: родительское окно
        :param user_id: ID пользователя, открывшего окно
        :param columns: столбцы из основной таблицы(первый столбец - обязательно PK)
        :param button_func: функция, вызываемая при нажатии на кнопку
        :param joins: объекты с информацией о присоединяемых таблицах и их столбцах
        :param where_expression: дополнительное условие для фильтрации в запросе(table.column=value)
        :param can_edit: добавлять ли возможность редактирования данных
        :param can_delete: добавлять ли возможность удаления записей
        :param can_add: добавлять ли возможность добавления записей
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(840, 640)

        self.setWindowTitle("Окно таблицы")

        self.main_table = main_table
        self.user_id = user_id
        self.where_expression = where_expression
        self.joins = joins or []
        self.btn_func = button_func

        self.columns = []
        self.tables = [self.main_table]
        columns = columns or get_columns(self.main_table)
        for column in columns:
            self.columns.append(f"{self.main_table}.{column}")

        for ind, join in enumerate(self.joins, start=1):
            self.columns.insert(ind, f"{join.tablename}.{join.pk}")
            self.tables.append(join.tablename)
            for column in join.columns:
                self.columns.append(f"{join.tablename}.{column}")

        self.main_pk = self.columns[0]
        self.has_btn = int(bool(self.btn_func))

        self.filter_cb.clear()
        self.filter_cb.addItems(self.columns[len(self.joins) + self.has_btn:])

        self.table.setColumnCount(len(self.columns) + self.has_btn)
        for col in range(self.has_btn, len(self.joins) + 1 + self.has_btn):
            self.table.setColumnHidden(col, True)

        headers = ["Действие"] if self.btn_func else []
        for column in self.columns:
            headers.append(column)
        self.headers = headers
        self.table.setHorizontalHeaderLabels(self.headers)

        self.table.verticalHeader().setVisible(False)
        self.table.itemChanged.connect(self.save_changes)
        update("SET FOREIGN_KEY_CHECKS = 0")
        self.load_data()

        self.search_edit.textChanged.connect(self.load_data)
        self.sort_cb.currentIndexChanged.connect(self.load_data)
        self.filter_cb.currentIndexChanged.connect(self.load_data)

        if can_edit:
            self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        else:
            self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        if can_delete:
            self.delete_btn.clicked.connect(self.delete_row)
        else:
            self.delete_btn.hide()
        if can_add:
            self.add_btn.clicked.connect(self.add_row)
        else:
            self.add_btn.hide()

    def _get_value_by_column(self, data: dict, column: str) -> str:
        return data.get(column, data[column.split('.')[1]])

    def _quote_value(self, value: str) -> str:
        if value.isdigit():
            return value
        return f"'{value}'"

    def load_data(self):
        self.table.itemChanged.disconnect()
        self.table.setRowCount(0)

        query = (f"SELECT {', '.join(self.columns)} "
                 f"\nFROM {self.main_table}")
        for jc in self.joins:
            query += f"\n{jc.join_query}"

        filter_column = self.filter_cb.currentText()
        filter_value = self.search_edit.text()
        if filter_value != "":
            query += f"\nWHERE {filter_column} LIKE '%{self.search_edit.text()}%'"

        if self.where_expression and filter_value:
            query += f" AND {self.where_expression}"
        elif self.where_expression:
            query += f"\nWHERE {self.where_expression}"

        try:
            data = select(query)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при загрузке данных", str(e))
            self.table.itemChanged.connect(self.save_changes)
            return

        if not data:
            self.table.setRowCount(0)
            self.table.itemChanged.connect(self.save_changes)
            return

        data = sorted(data,
                      key=lambda elem: self._get_value_by_column(elem, filter_column),
                      reverse=self.sort_cb.currentIndex())
        self.table.setRowCount(len(data))

        for i, row in enumerate(data):
            self.table.setRowHeight(i, 50)
            if self.btn_func:
                # Добавляем кнопку
                btn = QPushButton(text=self.btn_func.__doc__)
                btn.setStyleSheet("background: Teal; color: white; border: none;")
                btn.clicked.connect(
                    lambda _, parent_window=self, row_num=i,
                           pk_value=self._get_value_by_column(row, self.main_pk): self.btn_func(parent_window,
                                                                                                row_num, pk_value))
                self.table.setCellWidget(i, 0, btn)

            # Остальные данные
            for j, column in enumerate(self.columns, start=self.has_btn):
                value = str(self._get_value_by_column(row, column))
                if value.endswith((".jpg", ".png")):
                    self.table.setCellWidget(i, j, self.create_image_label(value))
                    continue
                self.table.setItem(i, j, QTableWidgetItem(value))

        self.table.resizeColumnsToContents()
        self.table.itemChanged.connect(self.save_changes)

    @staticmethod
    def create_image_label(image_filename: str):
        image_path = os.path.join(settings.project_root, "images", image_filename)
        label = QLabel()
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            label.setText("Нет изображения")

        return label

    def save_changes(self, item: QTableWidgetItem):
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Сохранить изменения?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            self.load_data()
            return
        current_row = item.row()
        current_column = item.column()
        if current_row is None or current_column is None:
            return
        table, column_name = self.headers[current_column].split('.', 1)
        pk_ind = None
        pk_key = ""
        if table == self.main_table:
            pk_ind = 0 + self.has_btn
            pk_key = self.main_pk
        else:
            for ind, join in enumerate(self.joins):
                if join.tablename == table:
                    pk_ind = ind + 1 + self.has_btn
                    pk_key = join.pk
        if pk_ind is None:
            QMessageBox.critical(self, "Ошибка при попытке сохранения",
                                 "Не получилось понять из какой таблицы поле")
            return
        pk_value = self.table.item(current_row, pk_ind).text()
        new_value = self.table.item(current_row, current_column).text()
        query = f"UPDATE {table} SET {column_name}={self._quote_value(new_value)} WHERE {pk_key} = {self._quote_value(pk_value)}"

        try:
            update(query)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при попытке сохранения", str(e))

        self.load_data()

    def delete_row(self):
        current_row = self.table.currentRow()
        if current_row is None:
            return
        pk_value = self.table.item(current_row, self.has_btn).text()
        try:
            update(f"DELETE FROM {self.main_table} WHERE {self.main_pk} = {self._quote_value(pk_value)}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при попытке удаления", str(e))
        self.load_data()

    def add_row(self):
        self.window = AddRowDialog(self.main_table, self)
        self.window.show()


if __name__ == "__main__":
    import sys


    def add_to_cart(self: TableWindow, row_num: int, pk_value: str):
        """В корзину"""
        product_id = pk_value
        try:
            # Проверяем, есть ли уже такой товар в корзине
            query = f"SELECT quantity FROM cart WHERE user_id = {self.user_id} AND product_id = {product_id}"
            result = select(query)

            if result:
                # Если товар уже есть - увеличиваем количество
                new_quantity = result[0]['quantity'] + 1
                update(
                    f"UPDATE cart SET quantity = {new_quantity} WHERE user_id = {self.user_id} AND product_id = {product_id}")
            else:
                # Если нет - добавляем новый
                update(f"INSERT INTO cart (user_id, product_id, quantity) VALUES ({self.user_id}, {product_id}, 1)")

            QMessageBox.information(self, "Успех", "Товар добавлен в корзину")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить товар в корзину: {str(e)}")


    def increase_quantity(self: TableWindow, row_num: int, pk_value: str):
        """+1"""
        cart_id = pk_value
        try:
            # Если товар уже есть - увеличиваем количество
            new_quantity = int(self.table.item(row_num, 3).text()) + 1
            update(f"UPDATE cart SET quantity = {new_quantity} WHERE id = {cart_id}")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить товар в корзину: {str(e)}")


    app = QApplication(sys.argv)
    user_id = 1
    # window = TableWindow(main_table="products", user_id=1,
    #                      can_edit=True, can_add=True, can_delete=True,
    #                      button_func=add_to_cart)
    window = TableWindow(main_table="cart", where_expression=f"cart.user_id={user_id}",
                         columns=["id", "quantity", "added_at"],
                         joins=[
                             JoinClause(
                                 tablename="products",
                                 pk="id",
                                 join_query="LEFT JOIN products ON products.id = cart.product_id",
                                 columns=["name", "description", "price", "photo"]
                             ),
                         ],
                         button_func=increase_quantity,
                         can_edit=True, can_add=True, can_delete=True)
    window.show()
    sys.exit(app.exec())
