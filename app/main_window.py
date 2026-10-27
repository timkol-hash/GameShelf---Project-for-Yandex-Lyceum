from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QLabel
)

from app.game_card import GameCard
from app.database import DataBase
from app.game_form import GameForm

BASE_DIR = Path(__file__).resolve().parent.parent
UI_PATH = BASE_DIR / "ui" / "main_window.ui"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI_PATH), self)
        self.games = DataBase.get_games()
        self.show_favorites_only = False
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(12)
        self.gamesContentLayout.insertLayout(0, self.cards_layout)
        self.fill_genres()
        self.searchEdit.textChanged.connect(self.update_games)
        self.genreComboBox.currentTextChanged.connect(
            self.update_games
        )
        self.update_games()
        self.pageTitleLabel.setText(
            f"Твоя игровая коллекция ({DataBase.get_game_count()})"
        )
        self.addGameButton.clicked.connect(self.open_game_form)
        self.favoritesButton.clicked.connect(self.show_favorites)
        self.collectionButton.clicked.connect(self.show_collection)

    def fill_genres(self):
        genres = sorted({game["genre"] for game in self.games})

        self.genreComboBox.blockSignals(True)
        self.genreComboBox.clear()
        self.genreComboBox.addItem("Все жанры")
        self.genreComboBox.addItems(genres)
        self.genreComboBox.blockSignals(False)

    def update_games(self):
        search_text = self.searchEdit.text().strip().lower()
        selected_genre = self.genreComboBox.currentText()
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()
        found = 0
        for game in self.games:
            title_matches = search_text in game["title"].lower()
            genre_matches = (
                    selected_genre == "Все жанры"
                    or game["genre"] == selected_genre
            )

            is_favorite = bool(game.get("is_favorite", 0))

            favorite_matches = (
                    not self.show_favorites_only or is_favorite
            )

            if title_matches and genre_matches and favorite_matches:
                found += 1
                card = GameCard(
                    game,
                    on_open=self.show_game,
                    on_delete=self.delete_game,
                    on_favorite=self.toggle_favorite
                )
                card.edit_callback = self.edit_game
                self.cards_layout.addWidget(card)
        if found == 0:
            self.cards_layout.addWidget(
                QLabel("Игры не найдены")
            )
        self.pageTitleLabel.setText(
            f"Твоя игровая коллекция ({DataBase.get_game_count()})"
        )
        self.cards_layout.addStretch()

    def toggle_favorite(self, game):
        DataBase.toggle_favorite(game["id"])
        self.games = DataBase.get_games()
        self.update_games()

    def show_favorites(self):
        self.show_favorites_only = not self.show_favorites_only
        self.update_games()

    def show_game(self, game):
        QMessageBox.information(
            self,
            game["title"],
            f'Название: {game["title"]}\n'
            f'Жанр: {game["genre"]}\n'
            f'Описание: {game["about"]}',
        )

    def delete_game(self, game):
        answer = QMessageBox.question(
            self,
            "Удаление игры",
            f'Удалить игру «{game["title"]}»?',
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if answer == QMessageBox.StandardButton.Yes:
            DataBase.delete_game(game["id"])
            self.games = DataBase.get_games()
            self.pageTitleLabel.setText(
                f"Твоя игровая коллекция ({DataBase.get_game_count()})"
            )
            self.fill_genres()
            self.update_games()
            self.fill_genres()
            self.update_games()

    def add_new_game(self, title, genre, cover_path=None):
        DataBase.add_game(title, genre, cover_path)
        self.pageTitleLabel.setText(
            f"Твоя игровая коллекция ({DataBase.get_game_count()})"
        )
        self.games = DataBase.get_games()
        self.fill_genres()
        self.update_games()

    def show_collection(self):
        self.show_favorites_only = False
        self.update_games()

    def open_game_form(self):
        form = GameForm(self)

        if form.exec():
            data = form.get_data()
            title = data["title"]
            genre = data["genre"]
            about = data["about"]
            cover_path = data["cover_path"]

            if not title:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Введи название игры!"
                )
                return

            DataBase.add_game(title, genre, cover_path, about)
            self.games = DataBase.get_games()
            self.fill_genres()
            self.update_games()

    def edit_game(self, game):
        form = GameForm(self, game)

        if form.exec():
            data = form.get_data()
            title = data["title"]
            genre = data["genre"]
            about = data["about"]
            cover_path = data["cover_path"]

            if not title:
                QMessageBox.warning(
                    self, "Ошибка", "Введи название игры!"
                )
                return

            DataBase.update_game(
                game["id"], title, genre, cover_path, about
            )
            self.games = DataBase.get_games()
            self.fill_genres()
            self.update_games()
