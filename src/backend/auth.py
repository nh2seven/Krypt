import os
from .init import InitUser
from src.modules.contextmanager import db_connect


class Admin:
    def __init__(self, db, username, password):
        """
        Initializes the variables for an admin.

        Args:
            username (int): Username for the admin.
            password (str): Password for the admin.
        """
        self.db = db
        self.uname = username  # 1
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


class User:
    def __init__(self, db, username, password):
        """
        Initializes the variables for a user.

        Args:
            username (str): Username for the user.
            password (str): Password for the user.
        """
        self.db = db
        self.uname = username
        self.pw = password  # Encryption to be applied in an external module

    def create(self, pw):
        """Creates a new user database."""
        user = InitUser(self.db)  # Pass the user database name from frontend
        user.init_user(pw)
        user.init_cred()
        user.init_group()

    def login(self):
        """Verifies user login details."""
        with db_connect(self.db) as cur:
            query = "SELECT pwd FROM user"
            cur.execute(query)
            result = cur.fetchone()
            return result and result[0] == self.pw
            # Add redirect to user panel

    def logout(self):
        """Handles user logout"""
        print(f"{self.uname} logged out")
        # Redirect to login screen; encrypt data before logging out

    def delete(self):
        """Deletes the user database"""
        db_path = "db/users/" + self.db
        if os.path.exists(db_path):
            os.remove(self.db)
            # Redirect to login screen, print message


if __name__ == "__main__":
    exit("Invalid entry point")
