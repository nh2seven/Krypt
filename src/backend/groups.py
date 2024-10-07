import sqlite3 as sql


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

if __name__ == "__main__":
    group_id = int(input("Group ID: "))
    username = input("Username: ")
    database = username.lower() + ".db"

    group = Group(database, group_id)

    # Test functions
    group.create_group()
    group.read_group()
    group.update_group("group_name", "Test")
    group.delete_group()