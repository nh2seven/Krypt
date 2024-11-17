from .init import InitUser as iu
import sqlite3 as sql
from contextlib import contextmanager


@contextmanager
def db_connect(database):
    connection = sql.connect(database, check_same_thread=False, cached_statements=32)
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        connection.commit()
        cursor.close()
        connection.close()


class Credentials:
    def __init__(self, db):
        """
        Handle user credentials.

        Args:
        db (str): Database path.
        """
        self.db = db

    def add_cred(self, title, username, password, url, notes, tags, expiration, group_id):
        with db_connect(self.db) as cur:
            query = """INSERT INTO credentials (title, username, password, url, notes, tags, expiration, group_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
            params = (title, username, password, url, notes, tags, expiration, group_id)
            cur.execute(query, params)

    def get_cred(self, title):
        with db_connect(self.db) as cur:
            query = """SELECT * FROM credentials WHERE title = ?;"""
            cur.execute(query, (title,))

    def modify_cred(self, title, username, password, url, notes, tags, expiration, group_id):
        with db_connect(self.db) as cur:
            query = """UPDATE credentials SET username = ?, password = ?, url = ?, notes = ?, tags = ?, expiration = ?, group_id = ? WHERE title = ?;"""
            params = (username, password, url, notes, tags, expiration, group_id, title)
            cur.execute(query, params)

    def remove_cred(self, title):
        with db_connect(self.db) as cur:
            query = """DELETE FROM credentials WHERE title = ?;"""
            cur.execute(query, (title,))


class Groups:
    def __init__(self, db):
        """
        Handle user groups.

        Args:
        db (str): Database path.
        """
        self.db = db

    def create_group(self):
        group = iu(self.db)
        group.init_cred()

    def delete_group(self, group_id):
        with db_connect(self.db) as cur:
            query = """DELETE FROM groups WHERE group_id = ?;"""
            cur.execute(query, (group_id,))


class Audit:
    def __init__(self, db):
        """
        Handle user audit.

        Args:
        db (str): Database path.
        """
        self.db = db

    def create_audit(self):
        audit = iu(self.db)
        audit.init_audit()

    def add_log(self, action_type, details):
        """Inserts an entry into the auditlog table."""
        with db_connect(self.database) as cur:
            insert_auditlog = """
            INSERT INTO auditlog (action_type, details) 
            VALUES (?, ?);
            """
            cur.execute(insert_auditlog, (action_type, details))


if __name__ == "__main__":  # Dummy code, to be replaced
    database = "user.db"
    cred = Credentials(database)
    group = Groups(database)
    audit = Audit(database)