import sqlite3
from datetime import datetime

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

        self.cur.execute("INSERT INTO photos (created_at, url, caption, user_id) VALUES (?, ?, ?, ?)", ( datetime.now(), url, caption, int(user_id) ))
        self.con.commit()
        
        return self.cur.lastrowid

    def find(self):

        self.connect()

        #results = self.cur.execute("SELECT * FROM photos ORDER BY created_at DESC")
        results = self.cur.execute("SELECT photos.id, photos.created_at, photos.url, photos.caption, photos.user_id, COUNT(likes.id) FROM photos LEFT JOIN likes ON photos.id = likes.photo_id GROUP BY photos.id ORDER BY photos.created_at DESC")

        return results.fetchall()

    

photos_db = PhotosDB()