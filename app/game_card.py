from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class GameCard(QFrame):
    def __init__(self, game, on_open=None, on_delete=None):
        super().__init__()
        self.photo = QPixmap(game.get("cover_path"))
        self.game = game
        self.on_open = on_open
        self.on_delete = on_delete


        self.setObjectName("gameCard")
        self.setStyleSheet("""
            QFrame#gameCard {
                background-color: #202020;
                border: 1px solid #383838;
                border-radius: 10px;
            }
            QLabel {
                border: none;
                background: transparent;
            }
            QPushButton {
                background-color: #353535;
                color: white;
                border: 1px solid #454545;
                border-radius: 6px;
                padding: 7px 12px;
            }
            QPushButton:hover {
                background-color: #484848;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 14, 16, 14)
        main_layout.setSpacing(14)

        cover = QLabel()
        cover.setFixedSize(64, 84)
        cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cover.setStyleSheet("""
            background-color: #303030;
            border-radius: 6px;
            font-size: 25px;
        """)
        if self.photo.isNull():
            cover.setText("Х")
        else:
            cover.setPixmap(
                self.photo.scaled(
                    cover.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        main_layout.addWidget(cover)

        info_layout = QVBoxLayout()

        title = QLabel(game["title"])
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")

        genre = QLabel(f'Жанр: {game["genre"]}')
        genre.setStyleSheet("color: #aaaaaa;")

        info_layout.addWidget(title)
        info_layout.addWidget(genre)
        info_layout.addStretch()

        main_layout.addLayout(info_layout, 1)

        open_button = QPushButton("Подробнее")
        open_button.clicked.connect(self.open_game)
        main_layout.addWidget(open_button)

        edit_button = QPushButton("Изменить")
        edit_button.clicked.connect(self.edit_game)
        main_layout.addWidget(edit_button)

        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(self.delete_game)
        main_layout.addWidget(delete_button)

    def open_game(self):
        if self.on_open:
            self.on_open(self.game)

    def delete_game(self):
        if self.on_delete:
            self.on_delete(self.game)

    def edit_game(self):
        if self.on_open:
            self.on_open(self.game)

    def edit_game(self):
        callback = getattr(self, "edit_callback", None)

        if callback:
            callback(self.game)
