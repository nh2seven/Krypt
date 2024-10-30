import sqlite3 as sql


class InitApp:
    def __init__(self, app_db):
        self.db = sql.connect(app_db, check_same_thread=True, cached_statements=32)
        self.cur = self.db.cursor()

    def init_tables(self):
        with self.db:
            init_auditlog = """
            CREATE TABLE IF NOT EXISTS auditlog (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT DEFAULT "None",
            action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            details TEXT DEFAULT "None"
            );
            """
            self.cur.execute(init_auditlog)

            init_admin = """
            CREATE TABLE IF NOT EXISTS admin (
            admin_id INTEGER PRIMARY KEY UNIQUE,
            admin_pw TEXT NOT NULL UNIQUE
            );
            """
            self.cur.execute(init_admin)

            init_user = """
            CREATE TABLE IF NOT EXISTS users (
            user_db TEXT NOT NULL UNIQUE,
            created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            self.cur.execute(init_user)


class InitUser:
    def __init__(self, user_db):
        self.db = sql.connect(user_db, check_same_thread=True, cached_statements=32)
        self.cur = self.db.cursor()

    def init_tables(self):
        with self.db:
            init_cred = """
            CREATE TABLE IF NOT EXISTS credentials (
            cred_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            url TEXT DEFAULT "None",
            notes TEXT DEFAULT "None",
            tags TEXT DEFAULT "None",
            expiration DATETIME,
            group_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups(group_id)
            );
            """
            self.cur.execute(init_cred)

            init_group = """
            CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            self.cur.execute(init_group)


# Standalone execution
if __name__ == "__main__":
    db_root = "db/"
    app_db = db_root + "App.db"
    user_db = db_root + "users/user.db"

    app = InitApp(app_db)
    app.init_tables()

    user = InitUser(user_db)
    user.init_tables()
