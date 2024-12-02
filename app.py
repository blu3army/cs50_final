from flask import Flask, session, render_template, redirect, request, jsonify
from database import init_tables, check_tables, create_user, users

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

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():

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
        
        create_user(username, password)

        return redirect("/")


@app.route("/api/users")
def get_users():
    res = users()
    print(res)
    return jsonify({'message': res[0]})



@app.route("/login", methods=['GET', 'POST'])
def login():
    session['username'] = 'nikolai10'

    return redirect("/")


@app.route("/sign_out")
def logout():
    session.pop('username', None)
    
    return redirect("/")