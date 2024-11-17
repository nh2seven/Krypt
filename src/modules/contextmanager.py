import sqlite3 as sql
from contextlib import contextmanager

@contextmanager
def db_connect(database):
    """Reusable database connection context manager
    
    Args:
        database (str): Path to SQLite database file
        
    Yields:
        sqlite3.Cursor: Database cursor object
    """
    connection = sql.connect(database, check_same_thread=False, cached_statements=32)
    cursor = connection.cursor() 
    try:
        yield cursor
    finally:
        connection.commit()
        cursor.close()
        connection.close()

if __name__ == "__main__":
    exit("Invalid entry point")