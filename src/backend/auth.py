import os
from .init import InitUser, DatabaseTriggers
from src.modules.contextmanager import db_connect


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
        self.pw = password

    def create(self, pw):
        """Creates a new user database."""
        try:
            user = InitUser(self.db)
            user.init_user(pw)
            user.init_cred()
            user.init_group()
            user.init_audit()
            
            trigger = DatabaseTriggers(self.db)
            trigger.create_triggers()
            return True
        except Exception as e:
            print(f"Error creating user database: {e}")
            return False

    def login(self):
        """Verifies user login details."""
        with db_connect(self.db) as cur:
            query = "SELECT pwd FROM user"
            cur.execute(query)
            result = cur.fetchone()
            return result and result[0] == self.pw

    def change_password(self, current_pw, new_pw):
        """
        Change user's password after verifying current password.
        
        Args:
            current_pw (str): Current password for verification
            new_pw (str): New password to set
            
        Returns:
            bool: True if password was changed successfully
        """
        with db_connect(self.db) as cur:
            verify = "SELECT pwd FROM user"
            cur.execute(verify)
            result = cur.fetchone()
            if not result or result[0] != current_pw:
                return False
                
            update = "UPDATE user SET pwd = ?"
            cur.execute(update, (new_pw,))
            return True

    def logout(self):
        """Handles user logout"""
        print(f"{self.uname} logged out")

    def delete(self):
        """Deletes the user database"""
        db_path = "db/users/" + self.db
        if os.path.exists(db_path):
            os.remove(self.db)


if __name__ == "__main__":
    exit("Invalid entry point")
