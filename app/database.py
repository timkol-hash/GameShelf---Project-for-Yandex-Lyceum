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
                cover_path TEXT
            )""")
            columns = [
                row[1] for row in db.execute("PRAGMA table_info(games)")
            ]

            if "cover_path" not in columns:
                db.execute("ALTER TABLE games ADD COLUMN cover_path TEXT")
            db.commit()

    @staticmethod
    def add_game(title, genre, cover_path=None):
        with sqlite3.connect("data/games.db") as db:
            c = db.cursor()
            db.execute(
                "INSERT INTO games (title, genre, cover_path) VALUES (?, ?, ?)",
                (title, genre, cover_path)
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
    def update_game(game_id, title, genre, cover_path=None):
        with sqlite3.connect("data/games.db") as db:
            db.execute(
                "UPDATE games SET title = ?, genre = ?, cover_path = ? WHERE id = ?",
                (title, genre, cover_path, game_id)
            )

    @staticmethod
    def delete_game(game_id):
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
