from flask import Flask, session, render_template, redirect, request, jsonify
from database.users import init_tables, users_db
from services.supabase_init import supabase

app = Flask(__name__)

app.secret_key = b'9585a2ee9ee6044d1e0ba57e366f40d98961cc169f326c80c896d97fcf90381e'

# basedir = os.path.abspath(os.path.dirname(__file__))

init_tables()
#check_tables()

@app.route("/")
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html')



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
        re_password = password = request.form['re_password']

        # Chequeamos si no existe username

        # Chequeamos que ambos passwords sean iguales
        res = users_db.create_user(username, password)
        users_db.close()
        # Create user
        if res:
            # Get the user's ID for session
            res = users_db.user_by_username(username)
            users_db.close()

            session['id'] = res[0]
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

        res = users_db.user_by_username_password(username, password)

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
@app.route("/photo_upload", methods = ['GET', 'POST', 'DELETE'])
def photo():

    # Check if user is logged
    if not session['id']:
        return redirect('/')

    if request.method == 'GET':
        return render_template('/photo_upload.html')
    else:
        # En caso de hacer POST
        file = request.files['photo']
        #caption = request.form['caption']

        print(file)

        # supabase.storage.from_('photos').upload(
        #     file=file.stream,
        #     path="aslasdga.jpg"
        # )

        return redirect('/')








@app.route("/api/users")
def get_users():
    res = users_db.users()
    users_db.close()
    print(res)
    return jsonify({'users': res})


@app.route("/api/user_by_username/<username>")
def get_user(username):
    res = users_db.user_by_username(username)
    users_db.close()
    print(res)
    return jsonify({'message': res})






