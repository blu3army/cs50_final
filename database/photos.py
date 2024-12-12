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

    def find(self, order = 'date', trendtime = 'alltimes'):
        # allowed_columns = ['photos.created_at', 'COUNT(likes.id)']
        # if order_by not in allowed_columns:
        #     order_by = 'photos.created_at'


        order_by = 'photos.created_at' if order == 'date' else 'COUNT(likes.id)'
        
        self.connect()

        if trendtime == 'alltimes' or order == 'date':
            #results = self.cur.execute("SELECT * FROM photos ORDER BY created_at DESC")
            results = self.cur.execute(f"SELECT photos.id, photos.created_at, photos.url, photos.caption, photos.user_id, COUNT(likes.id) FROM photos LEFT JOIN likes ON photos.id = likes.photo_id GROUP BY photos.id ORDER BY {order_by} DESC")

            return results.fetchall()

        else:

            time_start = ('now', '-1 month')
            time_end = ('now')

            match trendtime:
                case 'weekly':
                    time_start = ('now','-7 days')
                    time_end = ('now')                                
                case 'yearly':
                    time_start = ('now', '-1 year')
                    time_end = ('now')

            results = self.cur.execute(f"""
                                       SELECT photos.id, photos.created_at, photos.url, photos.caption, photos.user_id, COUNT(likes.id) 
                                       FROM photos 
                                       LEFT JOIN likes ON photos.id = likes.photo_id 
                                       GROUP BY photos.id 
                                       HAVING created at >= ? AND created_at < ?
                                       ORDER BY {order_by} DESC
                                       """, (time_start, time_end))

            return results.fetchall()




    

photos_db = PhotosDB()