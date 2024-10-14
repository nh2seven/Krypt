import sqlite3 as sql


class AuditLog:
    def __init__(self, db, log_id):
        """
        Initialize the audit log variables

        Args:
            self.db: Implicitly creates a new database if it doesn't exist
            self.cur: Cursor object to interact with the database
            self.log_id: ID for the log
        """
        self.db = sql.connect(db, check_same_thread=True, cached_statements=32)
        self.cur = self.db.cursor()
        self.log_id = log_id

    def create_log(self):
        with self.db:
            query = """
            CREATE TABLE auditlog (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT DEFAULT "Unknown",
            details TEXT DEFAULT "N/A",
            action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            self.cur.execute(query)

    def read_log(self):
        with self.db:
            query = """
            SELECT * FROM auditlog
            WHERE log_id = ?;
            """
            self.cur.execute(query, (self.log_id,))

    def update_log(self, action_type, details, action_time):
        with self.db:
            query = """
            UPDATE auditlog
            SET action_type = ?,
                details = ?,
                action_time = ?
            WHERE log_id = ?;
            """
            self.cur.execute(query, (action_type, details, action_time, self.log_id))

    def delete_log(self):
        with self.db:
            query = """
            DELETE FROM auditlog
            WHERE log_id = ?;
            """
            self.cur.execute(query, (self.log_id,))
        pass


if __name__ == "__main__":
    database = "Audit.db"
    db_path = "db/app/" + database
    n = 1

    audit = AuditLog(db_path, n)
    audit.create_log()
    audit.read_log()
    audit.update_log("Action", "Details", "Time")
    audit.delete_log()
