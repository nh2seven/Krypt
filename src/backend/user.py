from .init import InitUser as iu
from src.modules.contextmanager import db_connect


class Credentials:
    def __init__(self, db):
        """
        Handle user credentials.

        Args:
        db (str): Database path.
        """
        self.db = db

    def add_cred(self, title, username, password, url, notes, group_id):
        with db_connect(self.db) as cur:
            query = """INSERT INTO credentials (title, username, password, url, notes, group_id) VALUES (?, ?, ?, ?, ?, ?);"""
            params = (title, username, password, url, notes, group_id)
            cur.execute(query, params)

    def get_cred(self, title):
        with db_connect(self.db) as cur:
            query = """SELECT * FROM credentials WHERE title = ?;"""
            cur.execute(query, (title,))

    def modify_cred(self, new_title, username, password, url, notes, group_id, title):
        with db_connect(self.db) as cur:
            query = """UPDATE credentials SET title = ?, username = ?, password = ?, url = ?, notes = ?, group_id = ? WHERE title = ?;"""
            params = (new_title, username, password, url, notes, group_id, title)
            cur.execute(query, params)

    def remove_cred(self, title):
        with db_connect(self.db) as cur:
            query = """DELETE FROM credentials WHERE title = ?;"""
            cur.execute(query, (title,))


class Groups:
    def __init__(self, db):
        """
        Handle user groups.

        Args:
        db (str): Database path.
        """
        self.db = db

    def create_group(self):
        group = iu(self.db)
        group.init_cred()

    def add_group(self, title):
        """Add a new group"""
        with db_connect(self.db) as cur:
            query = """INSERT INTO groups (title) VALUES (?);"""
            cur.execute(query, (title,))
            return cur.lastrowid

    def get_groups(self):
        """Get all groups with credential counts"""
        with db_connect(self.db) as cur:
            query = """
            SELECT g.group_id, g.title, COUNT(c.cred_id) as cred_count
            FROM groups g
            LEFT JOIN credentials c ON g.group_id = c.group_id
            GROUP BY g.group_id, g.title
            ORDER BY g.title;
            """
            cur.execute(query)
            return cur.fetchall()
        
    def get_group(self, group_id):
        """Get group by ID"""
        with db_connect(self.db) as cur:
            query = """SELECT * FROM groups WHERE group_id = ?;"""
            cur.execute(query, (group_id,))
            return cur.fetchone()

    def get_gid(self, title):
        with db_connect(self.db) as cur:
            query = """SELECT group_id FROM groups WHERE title = ?;"""
            cur.execute(query, (title,))
            result = cur.fetchone()
            return result[0] if result else None


    def modify_group(self, new_title, group_id):
        with db_connect(self.db) as cur:
            query = """UPDATE groups SET title = ? WHERE group_id = ?;"""
            cur.execute(query, (new_title, group_id))

    def delete_group(self, group_id):
        with db_connect(self.db) as cur:
            query1 = """UPDATE credentials SET group_id = NULL WHERE group_id = ?;"""
            query2 = """DELETE FROM groups WHERE group_id = ?;"""
            cur.execute(query1, (group_id,))
            cur.execute(query2, (group_id,))


class Audit:
    def __init__(self, db):
        """
        Handle user audit.

        Args:
        db (str): Database path.
        """
        self.db = db

    def create_audit(self):
        audit = iu(self.db)
        audit.init_audit()

    def add_log(self, action_type, details):
        """Inserts an entry into the auditlog table."""
        with db_connect(self.db) as cur:
            insert_auditlog = """
            INSERT INTO auditlog (action_type, details) 
            VALUES (?, ?);
            """
            cur.execute(insert_auditlog, (action_type, details))


if __name__ == "__main__":  # Dummy code, to be replaced
    database = "user.db"
    cred = Credentials(database)
    group = Groups(database)
    audit = Audit(database)