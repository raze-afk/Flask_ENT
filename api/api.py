import flask
import sqlite3
from flask import request, jsonify, render_template


app = flask.Flask(__name__)
app.config["DEBUG"] = True

def connect():
    conn = sqlite3.connect('../database.db')
    conn.row_factory = sqlite3.Row
    return conn

#------------------------------------------------------------------------------
# Home
#------------------------------------------------------------------------------


@app.route('/', methods=['GET'])
def home():
    return '<h1>Distant Reading Archive</h1>'

#------------------------------------------------------------------------------
# Show User
#------------------------------------------------------------------------------

@app.route('/api/show/user', methods=['GET'])
def showUser():
    if 'id' in request.args:
        try:
            id = int(request.args['id'])
            conn = connect()
            cursor = conn.execute('SELECT * FROM user WHERE id ='+ str(id))
            user = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return jsonify(user), 200
        except sqlite3.Error as error:
            return error, 500
    
    conn = connect()
    cursor = conn.execute('SELECT * FROM user')
    listUser = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(listUser), 200

#------------------------------------------------------------------------------
# Delete User
#------------------------------------------------------------------------------

@app.route('/api/delete/user', methods=['GET'])
def deleteUser():
    if 'id' in request.args:
        try:
            id = int(request.args['id'])
            conn = connect()
            cursor = conn.execute('DELETE FROM user WHERE id ='+ str(id))
            conn.commit()
            conn.close()
            return "<p>user "+str(id)+" as been delete", 200
        except sqlite3.Error as error:
            return error, 500
    return "you must have id in get parameter", 400

#------------------------------------------------------------------------------
# Create User
#------------------------------------------------------------------------------

@app.route('/api/create/user', methods=['POST'])
def createUser():
    try:
        data = request.json
        name = data.get('nom')
        firstName = data.get('prenom')
        email = data.get('email')
        password = data.get('password')
        status = data.get('status')
        
        if status in ['admin','etudiant', 'professeur']:
            conn = connect()
            cursor = conn.execute('INSERT INTO user (nom, prenom, mail, mdp, status) VALUES (?, ?, ?, ?, ?)', (name, firstName, email, password, status))
            conn.commit()
            conn.close()
            return "user as been add", 200
        else:
            return "did you modify the option status?"

    except sqlite3.Error as error:
        return error, 500

#------------------------------------------------------------------------------
# Update User
#------------------------------------------------------------------------------

@app.route('/api/update/user', methods=['POST'])
def updateUser():
    try:
        data = request.json
        if data.get('nom'):
            dataUpdate = 'nom'
            upData = data.get('nom')
        elif data.get('prenom'):
            dataUpdate = 'prenom'
            upData = data.get('prenom')
        elif data.get('email'):
            dataUpdate = 'mail'
            upData = data.get('email')
        elif data.get('password')
            dataUpdate = mdp
            upData = data.get('password')
        elif data.get('status'):
            dataUpdate = 'status'
            upData = data.get('status')

        conn = connect()
        cursor = conn.execute('UPDATE user SET ? = ?', (dataUpdate, updata))


        
    except sqlite3.Error as error:
        return error, 500


app.run()
