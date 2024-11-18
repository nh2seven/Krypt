from src.modules.contextmanager import db_connect


class InitUser:
    def __init__(self, user_db):
        self.user_db = user_db

    def init_user(self, pw):
        with db_connect(self.user_db) as cur:
            init_user = """
            CREATE TABLE user (
            pwd TEXT NOT NULL
            );
            """
            user_pw = """
            INSERT INTO user (pwd) VALUES (?)
            """
            param = (pw,)

            cur.execute(init_user)
            cur.execute(user_pw, param)

    def init_cred(self):
        with db_connect(self.user_db) as cur:
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
            cur.execute(init_cred)

    def init_group(self):
        with db_connect(self.user_db) as cur:
            init_group = """
            CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cur.execute(init_group)

    def init_audit(self):
        """Creates the auditlog table if it does not exist."""
        with db_connect(self.user_db) as cur:
            init_auditlog = """
            CREATE TABLE IF NOT EXISTS auditlog (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT DEFAULT "None",
            action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            details TEXT DEFAULT "None"
            );
            """
            cur.execute(init_auditlog)


if __name__ == "__main__":
    exit("Invalid entry point")
