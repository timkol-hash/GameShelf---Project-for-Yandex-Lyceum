from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

BASE_DIR = Path(__file__).resolve().parent.parent
ABOUT_UI_PATH = BASE_DIR / "ui" / "about_UI.ui"


class About(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(str(ABOUT_UI_PATH), self)