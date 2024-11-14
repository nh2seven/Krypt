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


class Admin:
    def __init__(self, db, recovery_key):
        """
        Handle admin operations.
        No creation or deletion of admin, only one-time setup.

        Args:
        db (str): Database path.
        recovery_key (str): Path to key used for recovery.
        """
        self.db = db
        self.key = recovery_key

    # More functionality to be added in the future; placeholder for now


class Audit:
    def __init__(self, db):
        """
        Handle audit log.
        No updating audit log entries to preserve data integrity.
        Intentionally left out the ability to delete individual logs.

        Args:
        db (str): Database path.
        """
        self.db = db

    def create_log(self, log_id, action_type, details):
        query = """
        INSERT INTO auditlog (log_id, action_type, action_time, details)
        VALUES (?, ?, CURRENT_TIMESTAMP, ?);
        """
        with db_connect(self.db) as cur:
            cur.execute(query, (log_id, action_type, details))

    def read_log(self, filter, value):
        query = "SELECT * FROM auditlog"
        if filter in ["log_id", "action_type", "action_time"]:
            query += f" WHERE {filter} = ?"
            params = (value,)
        else:
            params = ()

        query += ";"
        with db_connect(self.db) as cur:
            cur.execute(query, params)

    def clean_logs(self):
        query = """
        DELETE FROM auditlog;
        """
        self.cur.execute(query)
        with db_connect(self.db) as cur:
            cur.execute(query)


if __name__ == "__main__":
    exit("Invalid entry point")