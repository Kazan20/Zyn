from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send
import sqlite3
import random
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Initialize the database
def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT UNIQUE,
                    username TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS codes (
                    phone_number TEXT,
                    code TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Generate a specific code based on the phone number
def generate_code(phone_number):
    return str(random.randint(1000, 9999))  # Simple code generation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    phone_number = request.form['phone_number']
    code = generate_code(phone_number)

    # Save the code in the database
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO codes (phone_number, code) VALUES (?, ?)", (phone_number, code))
    conn.commit()
    conn.close()

    # For demonstration, we'll return the code. In a real system, you'd send this via SMS.
    return jsonify({"code": code})

@app.route('/verify', methods=['POST'])
def verify():
    phone_number = request.form['phone_number']
    entered_code = request.form['code']

    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("SELECT code FROM codes WHERE phone_number=?", (phone_number,))
    saved_code = c.fetchone()
    
    if saved_code and saved_code[0] == entered_code:
        # Successful verification, allow user to set username
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route('/set_username', methods=['POST'])
def set_username():
    phone_number = request.form['phone_number']
    username = request.form['username']

    # Save the username to the users table
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (phone_number, username) VALUES (?, ?)", (phone_number, username))
    c.execute("INSERT INTO logins (phone_number) VALUES (?)", (phone_number,))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    join_room(room)
    send(f"{data['username']} joined the room '{room}'.", to=room)

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data['room']
    leave_room(room)
    send(f"{data['username']} left the room '{room}'.", to=room)

@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    send(f"{data['username']}: {data['message']}", to=room)

if __name__ == '__main__':
    init_db()  # Initialize the database
    socketio.run(app, debug=True)
