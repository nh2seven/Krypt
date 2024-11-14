import os
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
    def __init__(self, db, username, password):
        """
        Initializes the variables for an admin.

        Args:
            username (int): Username for the admin.
            password (str): Password for the admin.
        """
        self.db = db
        self.uname = username # 1
        self.pw = password  # Encryption to be applied in an external module

    def login(self):
        """Verify login details for admin."""
        with db_connect(self.db) as cur:
            query = "SELECT admin_pw FROM admin WHERE admin_id = ?"
            cur.execute(query, (self.uname,))
            result = cur.fetchone()
            if result and result[0] == self.pw:
                pass  # Redirect to admin panel

    def logout(self):
        """Handles admin logout. Encrypt data before logging out."""
        print(f"{self.uname} logged out")
        # Redirect to login screen


if __name__ == "__main__":
    exit("Invalid entry point")
