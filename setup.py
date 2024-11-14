import os

def dirs():
    # Create database directories
    db_root = "db/"
    if not os.path.exists(db_root):
        os.makedirs(db_root)

    db_users = os.path.join(db_root, "users/")
    if not os.path.exists(db_users):
        os.makedirs(db_users)

if __name__ == "__main__":
    exit("Invalid entry point")
