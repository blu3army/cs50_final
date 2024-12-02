import sqlite3

DATABASE = 'photofy.db'

def check_tables():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    print(f"Tables are: {res.fetchall()}")
    con.close()


def create_user(username, password):
    if not username or not password:
        return False
    else:
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        res = cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        con.commit()
        con.close()

def users():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    res = cur.execute('SELECT * FROM users;')
   
    return res.fetchall()


def init_tables():
    # con represents the connection 
    con = sqlite3.connect(DATABASE)

    # In order to execute SQL statements and fetch results from SQL queries, we will need to use a database cursor.
    cur = con.cursor()

    # Users table
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    bio TEXT
                );''')

    # Photos table
    cur.execute('''CREATE TABLE IF NOT EXISTS photos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    url VARCHAR,
                    caption TEXT,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );''')
    
    # ON DELETE SET NULL    Sets department_id to NULL when parent is deleted
    # ON DELETE CASCADE     # Deletes employee if department is deleted
    # ON DELETE RESTRICT    # Prevents deletion of parent if child exists
    # ON DELETE NO ACTION   # Default behavior, raises error

    # Likes table
    cur.execute('''CREATE TABLE IF NOT EXISTS likes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL,
                    photo_id INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(photo_id) REFERENCES photos(id),
                    UNIQUE(user_id, photo_id)
    );''')

    # Hashtags
    cur.execute('''CREATE TABLE IF NOT EXISTS hashtags(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    title VARCHAR UNIQUE
                );''')
    
    # Hashtags - photos
    cur.execute('''CREATE TABLE IF NOT EXISTS hashtags_photos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    photo_id INTEGER NOT NULL,
                    hashtag_id INTEGER NOT NULL,
                    FOREIGN KEY (photo_id) REFERENCES photos(id),
                    FOREIGN KEY (hashtag_id) REFERENCES hashtags(id),
                    UNIQUE(photo_id, hashtag_id)
                );''')

    con.commit()

    con.close()
