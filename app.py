from flask import Flask
from flask import jsonify
from flask import request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.debug = True

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'MyNewPass'
app.config['MYSQL_DATABASE_DB'] = 'ios_test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/api')
def index():
    return "Here we are!"


@app.route('/api/users', methods=['GET'])
def users():
    cursor = mysql.connect().cursor()
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    cursor.close()

    return jsonify(users)


@app.route('/api/users/<int:user_id>', methods=['GET'])
def user_by_id(user_id):
    cursor = mysql.connect().cursor()
    cursor.execute('SELECT * FROM Users WHERE user_id = %s LIMIT 1', [user_id])

    user = cursor.fetchall()
    cursor.close()

    return jsonify(user)
    

@app.route('/api/users/add', methods=['POST'])
def add_user():
    params = request.get_json(force=True)
    username = params.get('user_name')
    userid = params.get('user_id')

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Users (user_name, user_id) VALUES (%s, %s)', (username, userid))
    conn.commit()
    cursor.close()

    return jsonify({'status' : 'Created'})

@app.route('/api/users/delete', methods=['DELETE'])
def delete_user():
    pass

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error':'Not Found'})


app.run()
