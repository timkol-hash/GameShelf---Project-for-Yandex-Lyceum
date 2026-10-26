import sys

from PyQt6.QtWidgets import QApplication

from app.main_window import MainWindow
from app.database import DataBase


def main():
    DataBase.init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


def except_hook(t, v, b):
    sys.__excepthook__(t, v, b)


if __name__ == "__main__":
    sys.excepthook = except_hook
    main()
