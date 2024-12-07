import sqlite3


class PhotosDB():
    DATABASE = 'database/photofy.db'

    def connect(self):
        self.con = sqlite3.connect(self.DATABASE)
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()
        self.con.close()

    def create_photo(self, url, caption, user_id):
        self.connect()

        self.cur.execute("INSERT INTO photos (url, caption, user_id) VALUES (?, ?, ?)", ( url, caption, int(user_id) ))
        self.con.commit()
        
        return self.cur.lastrowid

    def find(self):

        self.connect()

        results = self.cur.execute("SELECT * FROM photos ORDER BY created_at DESC")

        return results.fetchall()

    

photos_db = PhotosDB()