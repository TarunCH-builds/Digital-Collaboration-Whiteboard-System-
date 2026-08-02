import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'collabboard_secret_key_12345'

# Initialize SocketIO with eventlet for production-ready async performance
socketio = SocketIO(app, cors_allowed_origins="*")

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'collabboard.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Whiteboards Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS whiteboards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            board_name TEXT NOT NULL,
            created_by TEXT NOT NULL,
            created_date TEXT NOT NULL,
            canvas_data TEXT
        )
    ''')
    
    # Messages Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            board_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(board_id) REFERENCES whiteboards(id)
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- HTTP ROUTES ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                         (username, email, hashed_password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or Email already exists.', 'danger')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).プリfetch()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    # Fetch all boards
    boards = conn.execute('SELECT * FROM whiteboards ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('dashboard.html', username=session['username'], boards=boards)

@app.route('/board/create', methods=['POST'])
def create_board():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    board_name = request.form['board_name'].strip()
    if not board_name:
        flash('Board name cannot be empty.', 'danger')
        return redirect(url_for('dashboard'))
        
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO whiteboards (board_name, created_by, created_date, canvas_data) VALUES (?, ?, ?, ?)',
                 (board_name, session['username'], created_date, ''))
    board_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return redirect(url_for('whiteboard', board_id=board_id))

@app.route('/board/<int:board_id>')
def whiteboard(board_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    board = conn.execute('SELECT * FROM whiteboards WHERE id = ?', (board_id,)).fetchone()
    
    if not board:
        conn.close()
        flash('Whiteboard not found.', 'danger')
        return redirect(url_for('dashboard'))
        
    # Get recent chat messages (last 50)
    messages = conn.execute('SELECT * FROM messages WHERE board_id = ? ORDER BY id ASC LIMIT 50', (board_id,)).fetchall()
    conn.close()
    
    return render_template('whiteboard.html', board=board, username=session['username'], messages=messages)

@app.route('/board/save/<int:board_id>', methods=['POST'])
def save_board_state(board_id):
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    canvas_data = data.get('canvas_data', '')
    
    conn = get_db_connection()
    conn.execute('UPDATE whiteboards SET canvas_data = ? WHERE id = ?', (canvas_data, board_id))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Auto-saved successfully'})


# --- WEBSOCKET EVENT HANDLING ---

@socketio.on('join_board')
def handle_join_board(data):
    room = str(data['board_id'])
    username = data['username']
    join_room(room)
    
    # Notify others in room
    emit('status_message', {'msg': f"{username} has joined the workspace."}, to=room, include_self=False)

@socketio.on('leave_board')
def handle_leave_board(data):
    room = str(data['board_id'])
    username = data['username']
    leave_room(room)
    emit('status_message', {'msg': f"{username} has left the workspace."}, to=room)

@socketio.on('draw_event')
def handle_draw_event(data):
    room = str(data['board_id'])
    # Broadcast drawing updates to all other clients in the same board room
    emit('draw_event', data, to=room, include_self=False)

@socketio.on('cursor_move')
def handle_cursor_move(data):
    room = str(data['board_id'])
    emit('cursor_move', data, to=room, include_self=False)

@socketio.on('chat_message')
def handle_chat_message(data):
    room = str(data['board_id'])
    username = data['username']
    msg_text = data['message'].strip()
    timestamp = datetime.now().strftime('%H:%M')
    
    if msg_text:
        # Persist message to DB
        conn = get_db_connection()
        conn.execute('INSERT INTO messages (board_id, username, message, timestamp) VALUES (?, ?, ?, ?)',
                     (int(room), username, msg_text, timestamp))
        conn.commit()
        conn.close()
        
        emit('chat_message', {
            'username': username,
            'message': msg_text,
            'timestamp': timestamp
        }, to=room)

if __name__ == '__main__':
    init_db()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
