from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import subprocess
import threading
import webbrowser
#1
app = Flask(__name__, template_folder='templates', static_folder='templates/assets')

user_last_message_time = {}
message_delay = 15

conn = sqlite3.connect('forum.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute('SELECT * FROM messages ORDER BY id DESC')
    messages = c.fetchall()
    conn.close()
    return render_template('index.html', messages=messages)

import time

user_last_message_time = {}
message_delay = 15  # Задержка в секундах

def can_send_message(user_ip):
    current_time = time.time()
    last_message_time = user_last_message_time.get(user_ip, 0)
    return (current_time - last_message_time) >= message_delay

def update_last_message_time(user_ip):
    user_last_message_time[user_ip] = time.time()

@app.route('/')
def mainw():
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute('SELECT * FROM messages ORDER BY id DESC')
    messages = c.fetchall()
    conn.close()
    return render_template('index.html', messages=messages)

@app.route('/add', methods=['POST'])
def add():
    user_ip = request.remote_addr
    if not can_send_message(user_ip):
        remaining_seconds = int(user_last_message_time[user_ip] + message_delay - time.time())
        return jsonify({'success': False, 'remainingSeconds': remaining_seconds})

    message = request.form['message']
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (content) VALUES (?)', (message,))
    conn.commit()
    conn.close()
    update_last_message_time(user_ip)
    return jsonify({'success': True, 'remainingSeconds': 0})



if __name__ == '__main__':
    server_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    server_thread.start()

    subprocess_cmd = ['ssh', '-R', 'mtfk:80:localhost:5000', 'serveo.net']
    subprocess.Popen(subprocess_cmd)
