from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit,
    QComboBox, QPushButton, QLabel,
    QFileDialog
)


class GameForm(QDialog):
    def __init__(self, parent=None, game=None):
        super().__init__(parent)
        self.game = game
        self.setWindowTitle("Добавить игру")
        self.setMinimumWidth(300)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Название игры"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Описание"))
        self.title_about = QLineEdit()
        layout.addWidget(self.title_about)
        layout.addWidget(QLabel("Жанр"))
        self.genre_input = QComboBox()
        self.genre_input.addItems([
            "Экшен", "РПГ", "Приключение",
            "Песочница", "Гонки", "Стратегия",
            "Хоррор", "Шутер",
        ])
        self.cover_path = game.get("cover_path") if game else None
        self.coverButton = QPushButton("Выбрать обложку")
        self.coverButton.clicked.connect(self.choose_cover)
        layout.addWidget(self.genre_input)
        self.save_button = QPushButton("Сохранить")
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.coverButton)
        if game:
            self.title_input.setText(game["title"])
            self.genre_input.setCurrentText(game["genre"])
            self.title_about.setText(game["about"])
            self.setWindowTitle("Редактировать игру")

    def get_data(self):
        return {
            "title": self.title_input.text().strip(),
            "genre": self.genre_input.currentText(),
            "cover_path": self.cover_path,
            "about": self.title_about.text().strip()
        }

    def choose_cover(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выбрать обложку",
            "",
            "Картинки (*.png *.jpg *.jpeg *.webp)"
        )

        if path:
            self.cover_path = path
            self.coverButton.setText("Обложка выбрана")
