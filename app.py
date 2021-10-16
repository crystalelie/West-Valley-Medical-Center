
from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'cs340_eliec'
app.config['MYSQL_PASSWORD'] = '3704'
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_DB'] = 'cs340_eliec'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Running queries to be used within each route
cur = mysql.connection.cursor()
cur.execute("SELECT * FROM Patients")
pat = cur.fetchall()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/medications')
def medications():
    return render_template('medications.html')

@app.route('/nurses')
def nurses():
    return render_template('nurses.html')

@app.route('/patients')
def patients():
    return render_template('patients.html')

@app.route('/patientdetails')
def patientdetails():
    return render_template('patientdetails.html')

@app.route('/physicians')
def physicians():
    return render_template('physicians.html')

@app.route('/treatments')
def treatments():
    return render_template('treatments.html')


if __name__ == "__main__":
    app.run('127.0.0.1', port=5004, debug=True)

