from flask import Flask, request, redirect, render_template
import sqlite3
import os

app = Flask(__name__)

# Create DB
conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS contacts
             (name TEXT, email TEXT, subject TEXT, message TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO contacts VALUES (?, ?, ?, ?)",
              (name, email, subject, message))
    conn.commit()
    conn.close()

    return "Form submitted successfully!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)