import sqlite3 as sql


class Metadata:
    def __init__(self, db, meta_id):
        """
        """
        self.db = sql.connect(db, check_same_thread=True, cached_statements=32)
        self.cur = self.db.cursor()
        self.meta_id = meta_id

    def create_meta(self):
        with self.db:
            query = """
                    CREATE TABLE metadata (
                    meta_id INTEGER PRIMARY KEY UNIQUE,
                    description TEXT DEFAULT "N/A",
                    tags TEXT DEFAULT "N/A",
                    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expire_in TIMESTAMP NOT NULL
                    );
                    """
            self.cur.execute(query)
        
    def read_meta(self):
        with self.db:
            query = f"""
                    SELECT * FROM metadata
                    WHERE meta_id = ?;
                    """
            self.cur.execute(query, (self.meta_id,))

    def update_meta(self, attr, value):
        with self.db:
            query = f"""
                    UPDATE metadata
                    SET {attr} = ?
                    WHERE meta_id = ?;
                    """
            self.cur.execute(query, (value, self.meta_id,))

    def delete_meta(self):
        with self.db:
            query = f"""
                    DELETE FROM metadata
                    WHERE meta_id = ?;
                    """
            self.cur.execute(query, (self.meta_id,))

if __name__ == "__main__":
    meta_id = int(input("Metadata ID: "))
    username = input("Username: ")
    database = username.lower() + ".db"

    meta = Metadata(database, meta_id)

    # Test functions
    meta.create_meta()
    meta.read_meta()
    meta.update_meta("description", "Test")
    meta.delete_meta()