import sqlite3

class DBHelper: 
    def __init__(self, dbname="coinvalet.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        cursorObj = self.conn.cursor()
        stmt = "CREATE TABLE if not exists users (chatid text PRIMARY KEY, username text, password text, apiKey text, secretKey text)"
        cursorObj.execute(stmt)
        self.conn.commit()

    def add_user(self, credentials: tuple):
        cursorObj = self.conn.cursor()
        stmt = "INSERT INTO users (chatid, username, password, apiKey, secretKey) VALUES (?, ?, ?, ?, ?)"
        cursorObj.execute(stmt, credentials)
        self.conn.commit()

    def delete_user(self, chatid: str):
        cursorObj = self.conn.cursor()
        stmt = "DELETE FROM users WHERE chatid = (?)"
        cursorObj.execute(stmt, (chatid, ))
        self.conn.commit()

    def get_users_cred(self):
        cursorObj = self.conn.cursor()
        stmt = "SELECT * FROM users"
        cursorObj.execute(stmt)
        rows = cursorObj.fetchall()
        users = []
        for row in rows:
            users.append(row[0])
        return users