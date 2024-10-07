import sqlite3 as sql


# Handle a single user database
class User:
    def __init__(self, db, username, password):
        """
        Initializes variables for a single user database

        Args:
            self.db: Implicitly creates a new database if it doesn't exist
            self.cur: Cursor object to interact with the database
            self.uname: Username for the user
            self.pw: Password for the user
        """
        self.db = sql.connect(db, check_same_thread=True, cached_statements=32)
        self.cur = self.db.cursor()
        self.user = username
        self.pw = password

    def create_cred(self):
        with self.db:
            query = """
                    CREATE TABLE IF NOT EXISTS credentials (
                    cred_name TEXT PRIMARY KEY UNIQUE,
                    username TEXT NOT NULL UNIQUE CHECK(length(username) >= 8),
                    password TEXT NOT NULL CHECK(length(password) >= 8),
                    website TEXT,
                    meta_id INTEGER,
                    group_id INTEGER,
                    FOREIGN KEY (meta_id) REFERENCES metadata(meta_id),
                    FOREIGN KEY (group_id) REFERENCES grouped(group_id)
                    );
                    """
            self.cur.execute(query)

    def read_cred(self):
        with self.db:
            query = f"""
                    SELECT * FROM credentials
                    WHERE cred_name = ?;
                    """
            self.cur.execute(query, (self.user,)) # Prevent SQL injection

    def update_cred(self, attr, value):
        with self.db:
            query = f"""
                    UPDATE credentials
                    SET {attr} = ?
                    WHERE cred_name = ?;
                    """
            self.cur.execute(query, (value, self.user,))

    def delete_cred(self):
        with self.db:
            query = f"""
                    DELETE FROM credentials
                    WHERE cred_name = ?;
                    """
            self.cur.execute(query, (self.user,))


if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    database = username.lower() + ".db"

    user = User(database, username, password)

    # Test functions
    user.create_cred()
    user.read_cred()
    user.update_cred("cred_name", "xyz")
    user.delete_cred()
