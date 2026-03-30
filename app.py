from flask import Flask, request, redirect, render_template, url_for
import sqlite3
import os
print("DB PATH:", os.path.abspath('data.db'))
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
    print("FORM HIT")  
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

    
    return redirect(url_for('view'))

# 🔥 ADD THIS PART
@app.route('/view')
def view():
    if request.args.get("key") != "admin123":
        return "Unauthorized"
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    data = c.fetchall()
    conn.close()

    return render_template("view.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)