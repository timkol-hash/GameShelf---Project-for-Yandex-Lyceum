from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit,
    QComboBox, QPushButton, QLabel,
    QFileDialog
)


class GameForm(QDialog):
    def __init__(self, parent=None, game=None):
        super().__init__(parent)
        self.game = game
        self.titleEdit = QLineEdit()
        self.setWindowTitle("Добавить игру")
        self.setMinimumWidth(300)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Название игры"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Жанр"))
        self.genre_input = QComboBox()
        self.genre_input.addItems([
            "Action", "RPG", "Adventure",
            "Sandbox", "Racing", "Strategy",
            "Horror", "Shooter",
        ])
        self.cover_path = None
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
            self.setWindowTitle("Редактировать игру")

    def get_data(self):
        return {
            "title": self.titleEdit.text().strip(),
            "genre": self.genreComboBox.currentText(),
            "cover_path": self.cover_path
        }

    def choose_cover(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выбрать обложку",
            "",
            "Images (*.png *.jpg *.jpeg *.webp)"
        )

        if path:
            self.cover_path = path
            self.coverButton.setText("Обложка выбрана")
