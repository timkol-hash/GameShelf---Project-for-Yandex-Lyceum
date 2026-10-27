import sqlite3


class DataBase:
    @staticmethod
    def init_db():
        with sqlite3.connect("data/games.db") as db:
            c = db.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL,
                cover_path TEXT,
                is_favorite INTEGER DEFAULT 0,
                about TEXT
            )""")
            columns = [
                row[1] for row in db.execute("PRAGMA table_info(games)")
            ]

            if "about" not in columns:
                db.execute("ALTER TABLE games ADD COLUMN about TEXT")

            if "is_favorite" not in columns:
                db.execute("ALTER TABLE games ADD COLUMN is_favorite INTEGER")

            db.execute(
                "UPDATE games SET is_favorite = 0 WHERE is_favorite IS NULL"
            )

            if "cover_path" not in columns:
                db.execute("ALTER TABLE games ADD COLUMN cover_path TEXT")
            db.commit()

    @staticmethod
    def add_game(title: str, genre: str, cover_path=None, about=None):
        with sqlite3.connect("data/games.db") as db:
            c = db.cursor()
            db.execute(
                "INSERT INTO games (title, genre, cover_path, about) VALUES (?, ?, ?, ?)",
                (title, genre, cover_path, about)
            )
            db.commit()

    @staticmethod
    def get_games():
        with sqlite3.connect("data/games.db") as db:
            db.row_factory = sqlite3.Row
            c = db.cursor()
            r = c.execute(
                "SELECT * FROM games ORDER BY title"
            ).fetchall()

            games = [dict(row) for row in r]

        return games

    @staticmethod
    def update_game(game_id: int, title: str, genre: str, cover_path=None, about=None):
        with sqlite3.connect("data/games.db") as db:
            db.execute(
                "UPDATE games SET title = ?, genre = ?, cover_path = ?, about = ? WHERE id = ?",
                (title, genre, cover_path, about, game_id)
            )

    @staticmethod
    def toggle_favorite(game_id: int):
        with sqlite3.connect("data/games.db") as db:
            cursor = db.execute(
                "SELECT is_favorite FROM games WHERE id = ?",
                (game_id,)
            )
            row = cursor.fetchone()

            if row is not None:
                new_value = 1 - (row[0] or 0)
                db.execute(
                    "UPDATE games SET is_favorite = ? WHERE id = ?",
                    (new_value, game_id)
                )

    @staticmethod
    def delete_game(game_id: int):
        with sqlite3.connect("data/games.db") as db:
            db.execute(
                "DELETE FROM games WHERE id = ?",
                (game_id,),
            )

    @staticmethod
    def get_game_count():
        with sqlite3.connect("data/games.db") as db:
            result = db.execute(
                "SELECT COUNT(*) FROM games"
            ).fetchone()

        return result[0]
