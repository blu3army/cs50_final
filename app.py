from flask import Flask, session, render_template, redirect, request, jsonify
from services.supabase_init import supabase
from database.users import users_db
from database.photos import photos_db
from database.hashtags import hashtags_db
from database.likes import likes_db
from database.init_database import init_tables
import hashlib
import re
import uuid

app = Flask(__name__)

app.secret_key = SECRET_KEY
#app.secret_key = os.getenv('SECRET_KEY')

# basedir = os.path.abspath(os.path.dirname(__file__))


@app.route("/")
def index():
    
    # Get parameters
    # order
    # trendtime
    # hashtag 
    page = request.args.get('page') or '1'
    
    order = request.args.get('order') or 'date' # likes or date
    trendtime = request.args.get('trendtime') or 'alltimes' # weekly, montly, yearly or alltimes
    hashtag = request.args.get('hashtag') or None

    #print(order, trendtime, hashtag)

    photos = photos_db.find(order=order, trendtime=trendtime, hashtag=hashtag, page= (int(page)-1))

    photos_db.close()

    if 'id' in session:
        # Search likes by user
        photos_likes_ids = likes_db.photos_ids_by_userlike_it(session['id'])
        
        photos_likes_ids = list(map( lambda x: x[0], photos_likes_ids ))
        
        for i, photo in enumerate(photos):
            # Si el id de la photo está en la lista de photos likes
            if photo[0] in photos_likes_ids:
                photos[i] = photos[i] + (True,)
            else:
                photos[i] = photos[i] + (False,)

        likes_db.close()

    # return jsonify({
    #     'photos': photos
    # })

    
    #print(f"photos: {photos}")
    return render_template('index.html', session=session, photos=photos, order=order, trendtime=trendtime, hashtag=hashtag, page=int(page))


@app.route('/user/<username>')
def user(username):
    page = request.args.get('page') or '1'

    photos = photos_db.find_by_user( username=username, page= (int(page)-1))

    photos_db.close()

    if 'id' in session:
        # Search likes by user
        photos_likes_ids = likes_db.photos_ids_by_userlike_it(session['id'])
        
        photos_likes_ids = list(map( lambda x: x[0], photos_likes_ids ))
        
        for i, photo in enumerate(photos):
            # Si el id de la photo está en la lista de photos likes
            if photo[0] in photos_likes_ids:
                photos[i] = photos[i] + (True,)
            else:
                photos[i] = photos[i] + (False,)

        likes_db.close()



    return render_template('profile.html', photos=photos, username=username, session=session, page=int(page))


# HASHTAGS
@app.route('/top_hashtags')
def top_hashtags():

    results = hashtags_db.get_tops()
    hashtags_db.close()

    hashtags = list( map( lambda x: {'title': x[0], 'count': x[1]}, results) )

    return jsonify({"hashtags": hashtags})


@app.route('/search_hashtag/<text>')
def search_hashtag(text):

    results = hashtags_db.get_by_text(text.lower())
    hashtags_db.close()

    hashtags = list( map( lambda x: {'title': x[0]}, results) )


    return jsonify({"hashtags": hashtags})



# LOGIN SYSTEM

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():

    # Sign out, by the way
    session.pop('id', None)
    session.pop('username', None)
    
    if request.method == 'GET':
        
        return render_template('sign_up.html')
    else:
        # Create User
        username = request.form['username']
        password = request.form['password']
        re_password = request.form['re_password']

        # Chequeamos si no existe username
        if not username:
            return 'Not username'
        
        if not password or not re_password:
            return 'Not password'
        
        # Chequeamos que ambos passwords sean iguales
        if password != re_password:
            return 'Passwords must be equals'
        
        # Get hash value from password
        hash_object = hashlib.sha256(password.encode())
        hash_value = hash_object.hexdigest()

       
        id = users_db.create_user(username=username, hash_value=hash_value)
        users_db.close()
        # Create user
        if id > 0:
            # Get the user's ID for session
            res = users_db.user_by_username(username)
            users_db.close()

            session['id'] = id
            session['username'] = res[3]

            return redirect("/")
        else:
            return redirect("/sign_up")
        

@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():

    # Sign out, by the way
    session.pop('id', None)
    session.pop('username', None)
    
    if request.method == 'GET':
        return render_template("sign_in.html")
    else:

        username = request.form['username']
        password = request.form['password']

        if not username:
            return 'Require an username'
        
        if not password:
            return 'Please type your password'
        
        # Get hash value from password
        hash_object = hashlib.sha256(password.encode())
        hash_value = hash_object.hexdigest()

        res = users_db.user_by_username_password(username, hash_value)

        users_db.close()

        if res:
            session['id'] = res[0]
            session['username'] = res[3]

            return redirect('/') 
        else:
            return redirect('/sign_in')


@app.route("/sign_out")
def logout():
    session.pop('id', None)
    session.pop('username', None)
    
    return redirect("/")


# PHOTO UP
@app.route("/photo_new", methods = ['GET', 'POST', 'DELETE'])
def photo_new():

    # Check if user is logged
    if not session['id']:
        return redirect('/')

    if request.method == 'GET':
        return render_template('/photo_new.html', session=session)
    
    else:

        if not session["id"]:
            return "You need to been logged"

        # Photo url     
        url = request.form['url']  
        # Caption
        caption = request.form['caption'] or None

        # Get hashtags from the caption
        caption_hashtags_list = re.findall(r'\s*#[\w\d-]+\s*', f" {caption} ")

        # Parseamos hashtags list
        hashtags = list(map( 
            lambda tag: tag.strip()[1:], # Put down the # character  
            caption_hashtags_list
        ))

        # Create hashtags if doesn't exist
        success_list = hashtags_db.insert_many(hashtags[:10]) # MAXIMO 10 HASHTAGS
        hashtags_db.close()

        # Create photo post
        photo_id = photos_db.create_photo(url, caption, session["id"])
        photos_db.close()

        # Get hashtags ids
        hashtags_ids = hashtags_db.get_hashtags_ids(hashtags)

        # Create relation between photo and hashtags
        relation_ids = hashtags_db.create_photo_hashtags(photo_id, set(hashtags_ids))

        hashtags_db.close()

        print(
            jsonify({
                "url": url,
                "caption": caption,
                "photo_id": photo_id,
                "hashtags": hashtags,
                "new hashtags": success_list,
                "hashtags ids": hashtags_ids,
                "relations ids": relation_ids,
                #"hashtags": hashtags
            })
        )

        return redirect(f'/')
       

@app.route('/photo_upload', methods = ['POST'])
def photo_upload():

    if not 'file' in request.files:
        return "There's no file"
        
    file = request.files['file']

    if file.filename == '':
        return "We need a file to be provided"

    # Give file an unique filename
    filename = uuid.uuid4().hex #secure_filename(file.filename)
    # Get from FileStorage
    file_contents = file.read()


    try:
        #file.save(filename)
        response = supabase.storage.from_('photos').upload(
            path=filename,
            file=file_contents,
            file_options={
                'content-type': file.mimetype
            }
        )
        
        url = supabase.storage.from_('photos').get_public_url(response.path)       
        
        return jsonify({
            "msg": "file upload successful", 
            "url": url
        })
      

    except Exception as e:
        return f"Error uploading file: {str(e)}"

    

# LIKES
@app.route('/like_it/<photo_id>', methods = ['GET'])
def like_it(photo_id):

    if not 'id' in session:
        return jsonify({"msg": "You need to be logged"})
    
    user_id = session['id']

    id = likes_db.like_it(user_id, photo_id)
    likes_db.close()

    return jsonify({"id": id, "msg": f"Created ok user {user_id}, photo {photo_id}"})

@app.route('/unlike_it/<photo_id>', methods = ['GET'])
def unlike_it(photo_id):

    if not 'id' in session:
        return jsonify({"msg": "You need to be logged"})
    
    user_id = session['id']

    res = likes_db.unlike_it(user_id, photo_id)
    likes_db.close()

    return jsonify({"res": res, "msg": f"Unliked ok user {user_id}, photo {photo_id}"})



# CONFIGURATIONS

@app.route('/api/init_database')
def init_database():
    
    init_tables()

    return redirect('/')

@app.route("/api/users")
def get_users():
    res = users_db.users()
    users_db.close()
    print(res)
    return jsonify({'users': res})


@app.route('/api/photos')
def get_photos():
    
    res = photos_db.photos()
    photos_db.close()
    
    return jsonify({'photos': res})


@app.route('/api/hashtags')
def get_hashtags():

    res = hashtags_db.hashtags()
    hashtags_db.close()

    return jsonify({'hashtags': res})

@app.route('/api/refresh_usernames')
def refresh_usernames():

    #photos_db.refresh_usernames()

    return jsonify({})

@app.route("/api/user_by_username/<username>")
def get_user(username):
    res = users_db.user_by_username(username)
    users_db.close()
    print(res)
    return jsonify({'message': res})






