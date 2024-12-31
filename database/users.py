import sqlite3


class UsersDB():
    DATABASE = 'database/data/photofy.sqlite'

    def connect(self):
        self.con = sqlite3.connect(self.DATABASE)
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()
        self.con.close()

    def create_user(self, username, hash_value):
        self.connect()

        if not username or not hash_value:
        
            return False
        else:
       
            self.cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_value))
            self.con.commit()
            
            # rowcount es 1 en caso de inserción exitosa
            return self.cur.lastrowid
        

    def users(self):
        self.connect()
        res = self.cur.execute('SELECT * FROM users')
    
        return res.fetchall()
    
    def user_by_username(self, username):
        self.connect()
        
        res = self.cur.execute('SELECT * FROM users WHERE username = ?', (username,))

        return res.fetchone()

    def user_by_username_password(self, username, hash_value):
        self.connect()
        
        res = self.cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hash_value,))

        return res.fetchone()
        



users_db = UsersDB()







