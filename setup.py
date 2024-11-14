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


def dirs():
    # Create database directories
    db_root = "db/"
    if not os.path.exists(db_root):
        os.makedirs(db_root)

    db_users = os.path.join(db_root, "users/")
    if not os.path.exists(db_users):
        os.makedirs(db_users)


def set_admin(db):
    apwd = input("Enter admin password: ")
    with db_connect(db) as cur:
        cur.execute("SELECT COUNT(*) FROM admin")
        if cur.fetchone()[0] == 0:
            query = """
            INSERT INTO admin (admin_id, admin_pw)
            VALUES (?, ?);
            """
            cur.execute(query, (1, apwd))
            print("Admin credentials set successfully.")
        else:
            print("Admin credentials already set.")


if __name__ == "__main__":
    exit("Invalid entry point")
