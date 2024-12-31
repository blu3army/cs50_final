import sqlite3


class HashtagsDB():
    DATABASE = 'database/data/photofy.sqlite'

    def connect(self):
        self.con = sqlite3.connect(self.DATABASE)
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()
        self.con.close()

    def hashtags(self):
        self.connect()
        res = self.cur.execute('SELECT * FROM hashtags')
    
        return res.fetchall()

    def get_tops(self):
        self.connect()

        results = self.cur.execute("""
                        SELECT hashtags.title, COUNT(hashtag_id) 
                        FROM hashtags_photos 
                        JOIN hashtags ON hashtag_id = hashtags.id 
                        GROUP BY hashtag_id 
                        ORDER BY COUNT(hashtag_id) 
                        DESC LIMIT 5;
                        """)

        return results.fetchall()
    

    
    def get_by_text(self, text):
        self.connect()

        results = self.cur.execute("SELECT title FROM hashtags WHERE title LIKE ? LIMIT 10;", ('%' + text + '%',))

        return results.fetchall()


    def insert_many(self, data):
        self.connect()

        successful_list = []

        for title in data:
            try:
                self.cur.execute("INSERT INTO hashtags (title) VALUES (?)",  (title.lower(),))
                successful_list.append(title)
            except sqlite3.IntegrityError as e:

                if "UNIQUE constraint failed" in str(e):
                    print("Unique ok")
                else:
                    raise e

        self.con.commit()
        
        return successful_list
    
    
    def get_hashtags_ids(self, hashtags):
        self.connect()
        ids_list = []

        for title in hashtags:
            try:
                res = self.cur.execute("SELECT id FROM hashtags WHERE title = ?",  (title,))
                id = res.fetchone()[0]
                ids_list.append(id)
            except Exception as e:
                print(f'Exception when get hashtag id', e)

        return ids_list
    
    
    def create_photo_hashtags(self, photo_id, hashtags_ids_list):
        self.connect()
        results = []

        for hashtag_id in hashtags_ids_list:

            try:
                self.cur.execute("INSERT INTO hashtags_photos (photo_id, hashtag_id) VALUES (?, ?)",  (photo_id, hashtag_id,) )
                results.append(self.cur.lastrowid)

            except sqlite3.IntegrityError as e:
                print(str(e)) 

        self.con.commit()

        return results
    

hashtags_db = HashtagsDB()