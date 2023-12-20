import sqlite3
from const import db_path

class DatabaseWrapper:
    def __init__(self):
        self.db_name = db_path

    def db_query(self, cmd, args=[], fetchone=True):
        database = sqlite3.connect(self.db_name, timeout=30)
        sql = database.cursor().execute(cmd, args)
        data = sql.fetchone()[0] if fetchone else sql.fetchall()
        database.close()
        return data

    def db_execute(self, cmd, args=[]):
        database = sqlite3.connect(self.db_name, timeout=30)
        database.cursor().execute(cmd, args)
        database.commit()
        database.close()

    def create_tables(self):
        self.db_execute(
            """CREATE TABLE IF NOT EXISTS USERS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username VARCHAR(50) NOT NULL UNIQUE,
            Main VARCHAR(50) NOT NULL,
            Success VARCHAR(50) NOT NULL DEFAULT False,
            Trials int NOT NULL DEFAULT 0,
            Time int NOT NULL DEFAULT 0,
            Rtime int NOT NULL DEFAULT 0,
            Ctime VARCHAR(100) NOT NULL DEFAULT None,
            Password VARCHAR(50) NOT NULL DEFAULT None,
            Reported int NOT NULL DEFAULT 0)
            ;"""
        )

    def ADD(self, username, main):
        self.db_execute(
            """
        INSERT INTO USERS(Username, Main)
        VALUES(?, ?);
        """, args=[username, main],)

    def UPDATE(self, ID, QUERY, VALUE):
        if QUERY in ('Time', 'Trials'):
            self.db_execute(
                f"""
                UPDATE USERS 
                SET {QUERY} = {QUERY} + {VALUE}
                WHERE ID=?;
                """, args=[ID],
            )
        else :
            self.db_execute(
                f"""
                UPDATE USERS 
                SET {QUERY} = ?
                WHERE ID=?;
                """, args=[VALUE, ID],
            )

    def GET(self, ID, QUERY):
        return self.db_query(
        f"""
        SELECT {QUERY}
        FROM USERS
        WHERE ID=?
        """,
            args=[ID],
            fetchone=False,
        )[0][0]

    def DELETE(self, ID):
        self.db_execute(
            """
        DELETE FROM USERS
        WHERE ID=?;
        """, args=[ID])

    def COUNT(self):
        return self.db_query(
            """
        SELECT COUNT(*) FROM USERS;
        """, fetchone=False,
        )[0][0]

