import sqlite3
from datetime import datetime

class PhotosDB():
    DATABASE = 'database/photofy.db'
    LIMIT = 5

    def connect(self):
        self.con = sqlite3.connect(self.DATABASE)
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()
        self.con.close()

    def create_photo(self, url, caption, user_id):
        self.connect()

        # Get author username
        res = self.cur.execute('SELECT username FROM users WHERE id = ?', (user_id,))
        username = res.fetchone()[0]

        self.cur.execute('INSERT INTO photos (created_at, url, caption, user_id, author_username) VALUES (?, ?, ?, ?, ?)', ( datetime.now(), url, caption, int(user_id), username ))
        self.con.commit()
        
        return self.cur.lastrowid

    def find(self, order = 'date', trendtime = 'alltimes', hashtag = None, page = 1):
        # allowed_columns = ['photos.created_at', 'COUNT(likes.id)']
        # if order_by not in allowed_columns:
        #     order_by = 'photos.created_at'

        offset = page * self.LIMIT


        order_by = 'photos.created_at' if order == 'date' else 'COUNT(likes.id)'
        
        self.connect()
       
        # In case is hashtag exists
        if hashtag:
            # SELECT * FROM photos JOIN hashtags_photos AS hp ON photos.id = hp.photo_id WHERE hp.hashtag_id = 18;
            hashtag_id = self.cur.execute("SELECT id FROM hashtags WHERE title = ?", (hashtag,))
            
            results = self.cur.execute(f"""
                                       SELECT photos.id, photos.created_at, photos.url, photos.caption, photos.user_id, COUNT(likes.id), photos.author_username  
                                       FROM photos 
                                       JOIN hashtags_photos AS hp ON photos.id = hp.photo_id
                                       LEFT JOIN likes ON likes.photo_id = photos.id
                                       WHERE hp.hashtag_id = ?
                                       GROUP BY photos.id
                                       ORDER BY photos.created_at DESC
                                       LIMIT ? 
                                       OFFSET ?
                                       """, 
                                       (hashtag_id.fetchone()[0], self.LIMIT, offset,)
                                    )
            
            return results.fetchall()
        



        
        if trendtime == 'alltimes' or order == 'date':
            #results = self.cur.execute("SELECT * FROM photos ORDER BY created_at DESC")
            results = self.cur.execute(f"""
                                       SELECT photos.id, photos.created_at, photos.url, photos.caption, photos.user_id, COUNT(likes.id), photos.author_username  
                                       FROM photos 
                                       LEFT JOIN likes ON photos.id = likes.photo_id 
                                       GROUP BY photos.id 
                                       ORDER BY {order_by} DESC
                                       LIMIT ? 
                                       OFFSET ?
                                       """, (self.LIMIT, offset,))

            return results.fetchall()

        else:

            time_start = ('now', '-1 month')
            time_end = ('now',)

            match trendtime:
                case 'weekly':
                    time_start = ('now','-7 days')
                    time_end = ('now',)                                
                case 'yearly':
                    time_start = ('now', '-1 year')
                    time_end = ('now',)

            #print(f"datetime {time_start[0]} {time_start[1]} {time_end[0]}")

            results = self.cur.execute(f"""
                                       SELECT photos.id, photos.created_at, photos.url, photos.caption, photos.user_id, COUNT(likes.id), photos.author_username 
                                       FROM photos 
                                       LEFT JOIN likes ON photos.id = likes.photo_id 
                                       GROUP BY photos.id 
                                       HAVING photos.created_at >= datetime(?, ?) AND photos.created_at < datetime(?)
                                       ORDER BY {order_by} DESC
                                       LIMIT ? 
                                       OFFSET ?
                                       """, (time_start[0], time_start[1], time_end[0], self.LIMIT, offset,))

            return results.fetchall()






    
    def find_by_user(self, username, page = 1):

        self.connect()

        offset = page * self.LIMIT

        results = self.cur.execute(f"""
                                       SELECT photos.id, photos.created_at, photos.url, photos.caption, photos.user_id, COUNT(likes.id), photos.author_username  
                                       FROM photos 
                                       LEFT JOIN likes ON photos.id = likes.photo_id
                                       WHERE photos.author_username = ?                                                                      
                                       GROUP BY photos.id 
                                       ORDER BY photos.created_at DESC
                                       LIMIT ? 
                                       OFFSET ?
                                       """, (username, self.LIMIT, offset,))

        return results.fetchall()


    




    def refresh_usernames(self):
        self.connect()

        # Get all photos
        res = self.cur.execute('SELECT id, user_id FROM photos')
        
        photos = res.fetchall()

        for photo in photos:
            res = self.cur.execute('SELECT username FROM users WHERE id = ?', (photo[1],))
            username = res.fetchone()[0]

            print(f'username = {username} user_id {photo[1]}')
            
            self.cur.execute('UPDATE photos SET author_username = ? WHERE user_id = ?', (username, photo[1],))

        self.con.commit()


photos_db = PhotosDB()