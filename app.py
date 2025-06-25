from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Ensure database exists
DB_PATH = "editor.db"
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS document (id INTEGER PRIMARY KEY, content TEXT)''')
    # Insert initial row if empty
    c.execute("SELECT COUNT(*) FROM document")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO document (content) VALUES ('')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT content FROM document WHERE id=1")
    content = c.fetchone()[0]
    conn.close()
    return render_template('editor.html', content=content)

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    new_content = data.get('content', '')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE document SET content = ? WHERE id = 1", (new_content,))
    conn.commit()
    conn.close()
    return jsonify({"status": "saved"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
