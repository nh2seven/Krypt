import sqlite3 as sql


class Admin:
    def __init__(self, db, admin_id, admin_name, admin_email, admin_key):
        """
        Initializes the variables for an admin

        Args:
            self.db: Implicitly creates a new database if it doesn't exist
            self.cur: Cursor object to interact with the database
            self.admin_id: Admin ID for the admin associated with a user's credentials
            self.admin_name: Admin name
            self.admin_email: Admin email
            self.admin_key: Admin key for access to the admin account
        """
        self.db = sql.connect(db, check_same_thread=True, cached_statements=32)
        self.cur = self.db.cursor()
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.admin_email = admin_email
        self.admin_key = admin_key

    def create_admin(self):
        with self.db:
            query = """
                    CREATE TABLE admin (
                    admin_id INTEGER PRIMARY KEY UNIQUE,
                    admin_pw TEXT NOT NULL UNIQUE CHECK(length(admin_pw) >= 8)
                    );
                    """
            self.cur.execute(query)

    def delete_admin(self): # Intended to be irreversible
        with self.db:
            query = """
                    DELETE FROM admin;
                    """
            self.cur.execute(query)


if __name__ == "__main__":
    database = "Admin.db"
    db_path = "db/app/" + database