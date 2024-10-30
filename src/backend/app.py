import sqlite3 as sql


class Admin:
    def __init__(self, db, recovery_key):
        """
        Handle admin operations.
        No creation or deletion of admin, only one-time setup.

        Args:
        """
        self.db = sql.connect(db, check_same_thread=True, cached_statements=32)
        self.cur = self.db.cursor()
        self.key = recovery_key


class Audit:
    def __init__(self, db):
        """
        Handle audit log.
        No updating audit log entries to preserve data integrity.
        Intentionally left out the ability to delete individual logs.

        Args:
        """
        self.db = sql.connect(db, check_same_thread=True, cached_statements=32)
        self.cur = self.db.cursor()

    def create_log(self, log_id, action_type, details, action_time):
        with self.db:
            query = """
            INSERT INTO auditlog (log_id, action_type, action_time, details)
            VALUES (?, ?, ?, ?);
            """
            self.cur.execute(query, (log_id, action_type, action_time, details))

    def read_log(self, filter, value):
        query = "SELECT * FROM auditlog"  # Base query
        if filter in ["log_id", "action_type", "action_time"]:
            query += f" WHERE {filter} = ?"
            params = (value,)
        else:
            params = ()

        query += ";"  # Terminate query
        with self.db:
            self.cur.execute(query, params)

    def clean_logs(self):
        with self.db:
            query = """
            DELETE FROM auditlog;
            """
            self.cur.execute(query)


if __name__ == "__main__": # Dummy code, to be replaced
    database = "App.db"
    admin = Admin(database, "admin_key_path")
    audit = Audit(database)
