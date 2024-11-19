from src.modules.contextmanager import db_connect


class InitUser:
    def __init__(self, user_db):
        self.user_db = user_db

    def init_user(self, pw):
        """Initialize user table with password"""
        with db_connect(self.user_db) as cur:
            init_user = """
            CREATE TABLE IF NOT EXISTS user (
                pwd TEXT NOT NULL
            );
            """
            user_pw = "INSERT INTO user (pwd) VALUES (?)"
            cur.execute(init_user)
            cur.execute(user_pw, (pw,))

    def init_group(self):
        """Initialize groups table"""
        with db_connect(self.user_db) as cur:
            init_group = """
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE
            );
            """
            cur.execute(init_group)

    def init_cred(self):
        """Initialize credentials table"""
        with db_connect(self.user_db) as cur:
            init_cred = """
            CREATE TABLE IF NOT EXISTS credentials (
                cred_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                url TEXT DEFAULT 'None',
                notes TEXT DEFAULT 'None',
                group_id INTEGER,
                FOREIGN KEY (group_id) REFERENCES groups(group_id)
            );
            """
            cur.execute(init_cred)

    def init_audit(self):
        """Initialize audit log table"""
        with db_connect(self.user_db) as cur:
            init_auditlog = """
            CREATE TABLE IF NOT EXISTS auditlog (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_type TEXT DEFAULT 'None',
                action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details TEXT DEFAULT 'None'
            );
            """
            cur.execute(init_auditlog)


class DatabaseTriggers:
    def __init__(self, user_db):
        self.user_db = user_db

    def create_triggers(self):
        triggers = [
            """
            CREATE TRIGGER IF NOT EXISTS after_cred_insert
            AFTER INSERT ON credentials
            BEGIN
                INSERT INTO auditlog (action_type, action_time, details)
                VALUES ('INSERT', DATETIME('now'), 'Inserted credential: ' || NEW.title);
            END;
            """,
            """
            CREATE TRIGGER IF NOT EXISTS after_cred_delete 
            AFTER DELETE ON credentials
            BEGIN
                INSERT INTO auditlog (action_type, action_time, details)
                VALUES ('DELETE', DATETIME('now'), 'Deleted credential: ' || OLD.title);
            END;
            """,
            """
            CREATE TRIGGER IF NOT EXISTS after_cred_update
            AFTER UPDATE ON credentials
            BEGIN
                INSERT INTO auditlog (action_type, action_time, details)
                VALUES ('UPDATE', DATETIME('now'), 'Updated credential: ' || OLD.title);
            END;
            """,
            """
            CREATE TRIGGER IF NOT EXISTS after_group_insert
            AFTER INSERT ON groups
            BEGIN
                INSERT INTO auditlog (action_type, action_time, details)
                VALUES ('INSERT', DATETIME('now'), 'Inserted group: ' || NEW.title);
            END;
            """,
            """
            CREATE TRIGGER IF NOT EXISTS after_group_delete 
            AFTER DELETE ON groups
            BEGIN
                INSERT INTO auditlog (action_type, action_time, details)
                VALUES ('DELETE', DATETIME('now'), 'Deleted group: ' || OLD.title);
            END;
            """,
            """
            CREATE TRIGGER IF NOT EXISTS after_group_update
            AFTER UPDATE ON groups
            BEGIN
                INSERT INTO auditlog (action_type, action_time, details)
                VALUES ('UPDATE', DATETIME('now'), 'Updated group: ' || OLD.title);
            END;
            """,
        ]
        with db_connect(self.user_db) as cursor:
            for trigger_sql in triggers:
                cursor.execute(trigger_sql)


if __name__ == "__main__":
    exit("Invalid entry point")
