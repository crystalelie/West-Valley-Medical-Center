
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)

app.config['MYSQL_USER'] = 'cs340_eliec'
app.config['MYSQL_PASSWORD'] = '3704'
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_DB'] = 'cs340_eliec'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/medications', methods=['GET', 'POST'])
def medications():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Medications")
    meds = cur.fetchall()
    return render_template('medications.html', meds=meds)

@app.route('/nurses')
def nurses():
    return render_template('nurses.html')

@app.route('/patients')
def patients():
    return render_template('patients.html')

@app.route('/patientdetails')
def patientdetails():
    return render_template('patientdetails.html')

@app.route('/physicians', methods=['GET', 'POST'])
def physicians():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Physicians")
    phys = cur.fetchall()
    return render_template('physicians.html', phys=phys)


@app.route('/treatments', methods=['GET', 'POST'])
def treatments():
    cur = mysql.connection.cursor()
    cur.execute("Select t.treatmentID, concat(p.firstName, ' ', p.lastName) as name, m.medicationName, frequency FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID")
    treats = cur.fetchall()

    # Creating a dictionary of distinct patient names
    cur.execute("Select DISTINCT concat(p.firstName, ' ', p.lastName) as name FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID")
    names = cur.fetchall()

    # Creating a dictionary of distinct medication names
    cur.execute("Select DISTINCT m.medicationName FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID")
    medications = cur.fetchall()

    return render_template('treatments.html', treats=treats, names=names, meds=medications)

