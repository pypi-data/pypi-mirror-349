import os

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit

from db.mysql_connection import select
from interface.auth_window_ui import Ui_AuthWindow
from settings import settings
from windows.user_window import UserWindow


class AuthWindow(QMainWindow, Ui_AuthWindow):
    """
    Окно авторизации пользователя.
    """

    def __init__(self, parent: QMainWindow = None):
        super().__init__(parent)
        self.setupUi(self)
        self.username = ""
        self.set_icon()

        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.log_but.clicked.connect(self.authenticate_user)

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

    def authenticate_user(self):
        login = self.log_edit.text().strip()
        password = self.pass_edit.text().strip()

        try:
            row = select("SELECT id, role FROM users WHERE login = %s AND password = %s", (login, password))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при поиске пользователя", str(e))
            return
        if row:
            self.log_edit.clear()
            self.pass_edit.clear()
            row = row[0]
            role = row["role"]
            self.user_id = row["id"]
            if role == "user":
                self.open_user_window()
            else:
                QMessageBox.critical(self, "Ошибка", "Такой роли не существует")
                return
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль.")

    def open_user_window(self):
        self.window = UserWindow(self.user_id, self)
        self.window.show()
        self.hide()
