import os

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from db.mysql_connection import select, update
from interface.user_window_ui import Ui_UserWindow
from settings import settings
from windows.table_window import TableWindow, JoinClause


class UserWindow(QMainWindow, Ui_UserWindow):
    def __init__(self, user_id: int, parent: QMainWindow = None):
        super().__init__(parent)
        self.setupUi(self)
        self.user_id = user_id
        self.set_icon()
        self.set_avatar()
        self.set_labels()

        self.back_btn.clicked.connect(self.go_back)
        self.table_button_1.clicked.connect(self.open_cart_window)
        self.table_button_1.setText("Корзина")
        self.table_button_2.clicked.connect(self.open_products_window)
        self.table_button_2.setText("Продукты")

    def set_icon(self):
        try:
            pixmap = QPixmap(
                os.path.join(
                    settings.project_root, "images", "logo.png"
                )
            )
            if not pixmap.isNull():
                self.icon_label.setPixmap(pixmap)
                self.icon_label.setScaledContents(True)
        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")

    def set_avatar(self):
        try:
            pixmap = QPixmap(
                os.path.join(
                    settings.project_root, "images", "logo.png"
                )
            )
            if not pixmap.isNull():
                self.avatar_label.setPixmap(pixmap)
                self.avatar_label.setScaledContents(True)
        except Exception as e:
            print(f"Ошибка загрузки аватарки: {e}")

    def set_labels(self):
        username = select(
            f"SELECT login FROM users WHERE id = {self.user_id}"
        )[0].get("login", "Undefined")
        self.name_label.setText(username)
        self.role_label.setText("User")

    def go_back(self):
        self.parent().show()
        self.close()

    def open_cart_window(self):
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

        self.window = TableWindow(main_table="cart", parent=self, user_id=self.user_id,
                                  where_expression=f"cart.user_id={self.user_id}",
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
        self.window.show()

    def open_products_window(self):
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

        self.window = TableWindow(main_table="products", parent=self, user_id=self.user_id,
                                  can_edit=False, can_add=False, can_delete=False,
                                  button_func=add_to_cart)
        self.window.show()
