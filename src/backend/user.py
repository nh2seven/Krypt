import sqlite3 as sql


# Handle a single user database
class Credentials:
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


class Group:
    def __init__(self, db, group_id):
        """
        Initializes the group for a single user database

        Args:
            self.db: Implicitly creates a new database if it doesn't exist
            self.cur: Cursor object to interact with the database
            self.group_id: Group ID for the group associated with a user's credentials
        """
        self.db = sql.connect(db, check_same_thread=True, cached_statements=32)
        self.cur = self.db.cursor()
        self.group_id = group_id

    def create_group(self):
        with self.db:
            query = """
                    CREATE TABLE grouped (
                    group_id PRIMARY KEY UNIQUE
                    , group_name TEXT NOT NULL
                    );
                    """
            self.cur.execute(query)

    def read_group(self):
        with self.db:
            query = f"""
                    SELECT * FROM grouped
                    WHERE group_id = ?;
                    """
            self.cur.execute(query, (self.group_id,))

    def update_group(self, attr, value):
        with self.db:
            query = f"""
                    UPDATE grouped
                    SET {attr} = ?
                    WHERE group_id = ?;
                    """
            self.cur.execute(query, (value, self.group_id,))

    def delete_group(self): 
        with self.db:
            query = f"""
                    DELETE FROM grouped
                    WHERE group_id = ?;
                    """
            self.cur.execute(query, (self.group_id,))


class Metadata:
    def __init__(self, db, meta_id):
        """
        Initializes the metadata associated with a single user database

        Args:
            self.db: Implicitly creates a new database if it doesn't exist
            self.cur: Cursor object to interact with the database
            self.meta_id: Metadata ID for the metadata associated with a user's credentials
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
    username = input("Username: ")
    password = input("Password: ")
    database = username.lower() + ".db"
    meta_id = int(input("Metadata ID: "))
    group_id = int(input("Group ID: "))

    user = Credentials(database, username, password)
    meta = Metadata(database, meta_id)
    group = Group(database, group_id)

    # Test functions
    user.create_cred()
    user.read_cred()
    user.update_cred("cred_name", "xyz")
    user.delete_cred()

    meta.create_meta()
    meta.read_meta()
    meta.update_meta("description", "Test")
    meta.delete_meta()

    group.create_group()
    group.read_group()
    group.update_group("group_name", "Test")
    group.delete_group()