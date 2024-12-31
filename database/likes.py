import sqlite3


class LikesDB():
    DATABASE = 'database/data/photofy.sqlite'

    def connect(self):
        self.con = sqlite3.connect(self.DATABASE)
        self.cur = self.con.cursor()
    
    def close(self):
        self.cur.close()
        self.con.close()


    def like_it(self, user_id, photo_id):
        self.connect()

        try:
            self.cur.execute("INSERT INTO likes (user_id, photo_id) VALUES (?, ?)", (int(user_id), int(photo_id),))
        except sqlite3.IntegrityError as e:
            print(str(e))
            return 0

        self.con.commit()

        return self.cur.lastrowid


    def unlike_it(self, user_id, photo_id):
        self.connect()

        self.cur.execute("DELETE FROM likes WHERE user_id = ? AND photo_id = ?", (int(user_id), int(photo_id),))

        self.con.commit()

        return self.cur.rowcount > 0


    # GET COUNT OF LIKES BY PHOTO_ID
    # SELECT photos.id, COUNT(*) FROM photos JOIN likes ON photos.id = likes.photo_id GROUP BY photos.id;
    # Return an array of photos_ids with their respective likes account
    def get_likescount_by_photos(self):
        self.connect()

        res = self.cur.execute("SELECT photos.id, COUNT(*) FROM photos JOIN likes ON photos.id = likes.photo_id GROUP BY photos.id")

        return res.fetchall()

    # GET PHOTOS ID IN WHAT USER LIKED THEM
    # SELECT photos.id FROM photos JOIN likes ON photos.id = likes.photo_id WHERE likes.user_id = 1;
    # Return an array of photos_ids
    def photos_ids_by_userlike_it(self, user_id):
        self.connect()

        res = self.cur.execute("SELECT photos.id FROM photos JOIN likes ON photos.id = likes.photo_id WHERE likes.user_id = ?", (int(user_id),) )

        return res.fetchall()

likes_db = LikesDB()