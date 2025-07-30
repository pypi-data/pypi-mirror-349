import logging
import sys
from PyQt6.QtWidgets import QApplication
from windows.auth_window import AuthWindow

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    print("Запуск приложения")
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())
