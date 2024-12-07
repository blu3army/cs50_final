import sqlite3


class LikesDB():
    DATABASE = 'database/photofy.db'

    def connect(self):
        self.con = sqlite3.connect(self.DATABASE)
        self.cur = self.con.cursor()


    def like_it(self, user_id, photo_id):
        self.connect()

        self.cur.execute("INSERT INTO likes (user_id, photo_id) VALUES (?, ?)", (int(user_id), int(photo_id),))

        self.con.commit()

        return self.cur.lastrowid


    def unlike_it(self, user_id, photo_id):
        self.connect()

        self.cur.execute("DELETE FROM likes WHERE user_id = ? AND photo_id = ?", (int(user_id), int(photo_id),))

        self.con.commit()



likes_db = LikesDB()