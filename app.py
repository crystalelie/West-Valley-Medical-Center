
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

    if request.method == 'POST':
        # Add a new medication
        if request.form.get('Add'):
            name = request.form['name']
            dosage = request.form['dosage']
            unit = request.form['unit']
            add_medication(name, dosage, unit)

        # Delete A medication
        elif request.form.get('Delete'):
            id = request.form['id']
            delete_medication(id)

        # Search for an item
        if request.form.get('Filter'):
            if request.form['filter1'] == "Name":
                name = request.form['result']
                cur.execute("SELECT * FROM Medications WHERE medicationName = %s", [name])
                meds = cur.fetchall()

            elif request.form['filter1'] == "Dosage":
                dosage = request.form['result']
                cur.execute("SELECT * FROM Medications WHERE dosage = %s", [dosage])
                meds = cur.fetchall()

            elif request.form['filter1'] == 'Unit':
                unit = request.form['result']
                cur.execute("SELECT * FROM Medications WHERE dosageUnit = %s", [unit])
                meds = cur.fetchall()

        elif request.form.get('Update'):
            id = request.form['id']
            Name = request.form['name']
            Dosage = request.form['dosage']
            Unit = request.form['unit']
            headers = ["Name", "Dosage", "Unit"]
            info = [Name, Dosage, Unit]
            return render_template('update.html', name="Medication Update", headers=headers, info=info, id=id, length=len(info))

        elif request.form.get('New'):
            id = request.form['id']
            Name = request.form['1']
            Dosage = request.form['2']
            Unit = request.form['3']
            update_medications(Name, Dosage, Unit, id)

    if not request.form.get('Filter'):
        cur.execute("SELECT * FROM Medications")
        meds = cur.fetchall()
    
    return render_template('medications.html', meds=meds)

def add_medication(name, dosage, unit):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Medications (medicationID, medicationName, dosage, dosageUnit) VALUES (IFNULL(%s, DEFAULT(medicationID)), %s, %s, %s)", ["NULL", name, dosage, unit])
    mysql.connection.commit()
    return

def delete_medication(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Medications WHERE medicationID = %s", [id])
    mysql.connection.commit()
    return

def update_medications(Name, Dosage, Unit, id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Medications SET medicationName=%s, dosage=%s, dosageUnit=%s WHERE medicationID=%s", [Name, Dosage, Unit, id])
    mysql.connection.commit()
    return

@app.route('/physicians', methods=['GET', 'POST'])
def physicians():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Add a new physician
        if request.form.get('Add'):
            fname = request.form['fname']
            lname = request.form['lname']
            specialty = request.form['specialty']
            add_physician(fname, lname, specialty)

        # Delete A physician
        elif request.form.get('Delete'):
            id = request.form['id']
            delete_physician(id)

        # Updating A Physician
        elif request.form.get('Update'):
            id = request.form['id']
            fname = request.form['fname']
            lname = request.form['lname']
            spec = request.form['specialty']
            headers = ["First Name", "Last Name", "Specialty"]
            info = [fname, lname, spec]
            return render_template('update.html', name="Physician Update", headers=headers, info=info, id=id, length=len(info))

        elif request.form.get('New'):
            id = request.form['id']
            fname = request.form['1']
            lname = request.form['2']
            spec = request.form['3']
            update_physicians(fname, lname, spec, id)

        # Filtering the results
        if request.form.get('Filter'):
            if request.form['filter1'] == "fname":
                fname = request.form['result']
                cur.execute("SELECT * FROM Physicians WHERE firstName = %s", [fname])
                phys = cur.fetchall()

            elif request.form['filter1'] == "lname":
                lname = request.form['result1']
                cur.execute("SELECT * FROM Physicians WHERE lastName = %s", [lname])
                phys = cur.fetchall()

            elif request.form['filter1'] == 'specialty':
                spec = request.form['result2']
                cur.execute("SELECT * FROM Physicians WHERE specialty = %s", [spec])
                phys = cur.fetchall()

    if not request.form.get('Filter1'):
        cur.execute("SELECT * FROM Physicians")
        phys = cur.fetchall()
        cur.execute("SELECT DISTINCT firstName FROM Physicians")
        fname = cur.fetchall()
        cur.execute("SELECT DISTINCT lastName FROM Physicians")
        lname = cur.fetchall()
        cur.execute("SELECT DISTINCT specialty FROM Physicians")
        spec = cur.fetchall()

    return render_template('physicians.html', phys=phys, fname=fname, lname=lname, spec=spec)

def add_physician(fname, lname, specialty):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Physicians (physicianID, firstName, lastName, specialty) VALUES (IFNULL(%s, DEFAULT(physicianID)), %s, %s, %s)", ["NULL", fname, lname, specialty])
    mysql.connection.commit()
    return

def delete_physician(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Physicians WHERE physicianID = %s", [id])
    mysql.connection.commit()
    return
    
def update_physicians(fname, lname, specialty, id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Physicians SET firstName=%s, lastName=%s, specialty=%s WHERE physicianID=%s", [fname, lname, specialty, id])
    mysql.connection.commit()
    return

@app.route('/treatments', methods=['GET', 'POST'])
def treatments():
    cur = mysql.connection.cursor()
    if request.method == 'POST':

        # Add a new treatment
        if request.form.get('Add'):
            pat = request.form['name']
            med = request.form['medication']
            freq = request.form['frequency']
            add_treatment(pat, med, freq)

        # Delete A Treatment
        elif request.form.get('Delete'):
            id = request.form['id']
            delete_treatment(id)

        # Update a Treatment
        elif request.form.get('Update'):
            id = request.form['id']
            fname = request.form['fname'] + " " + request.form['lname']
            cur.execute("Select DISTINCT concat(p.firstName, ' ', p.lastName) as name, t.patientID FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID")
            names = cur.fetchall()
            medication = request.form['medication']

            frequency = request.form['frequency']
            headers = ["Name", "Medication", "Frequency"]
            info = [fname, medication, frequency]
            return render_template('update.html', name="Treatment Update", headers=headers, info=info, id=id, length=len(info))

        elif request.form.get('New'):
            id = request.form['id']
            patient = request.form['1']
            medication = request.form['2']
            frequency = request.form['3']
            update_treatments(patient, medication, frequency, id)


        # Filtering the results
        elif request.form.get('Filter'):
            if request.form['filter1'] == "Pat":
                pat = request.form['result']
                cur.execute("Select concat(p.firstName, ' ', p.lastName) as name, m.medicationName, frequency FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID WHERE t.patientID = %s", [pat])
                treats = cur.fetchall()

            elif request.form['filter1'] == "Med":
                med = request.form['result1']
                cur.execute("Select concat(p.firstName, ' ', p.lastName) as name, m.medicationName, frequency FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID WHERE t.medicationID = %s", [med])
                treats = cur.fetchall()

            elif request.form['filter1'] == 'Freq':
                freq = request.form['result2']
                cur.execute("Select concat(p.firstName, ' ', p.lastName) as name, m.medicationName, frequency FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID WHERE t.frequency = %s", [freq])
                treats = cur.fetchall()


    if request.method == 'GET' or request.form.get('Add') or request.form.get('Delete') or request.form.get('Update'):
        cur.execute("Select t.treatmentID, concat(p.firstName, ' ', p.lastName) as name, m.medicationName, t.medicationID, t.patientID, frequency, p.firstName, p.lastName FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID")
        treats = cur.fetchall()

    # Creating a dictionary of distinct patient names
    cur.execute("Select DISTINCT concat(p.firstName, ' ', p.lastName) as name, t.patientID FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID")
    names = cur.fetchall()

    # Creating a dictionary of distinct medication names
    cur.execute("Select DISTINCT m.medicationName, t.medicationID FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID")
    medications = cur.fetchall()

    # Creating a dictionary of distinct frequencies
    cur.execute("Select DISTINCT frequency FROM Treatments")
    freq = cur.fetchall()

    return render_template('treatments.html', treats=treats, names=names, meds=medications, freq=freq)

def add_treatment(pat, med, freq):
    cur = mysql.connection.cursor()
    query = "INSERT INTO Treatments (treatmentID, patientID, medicationID, frequency) VALUES (IFNULL(%s, DEFAULT(treatmentID)), %s, %s, %s)"
    record = ("NULL", pat, med, freq)
    cur.execute(query, record)
    mysql.connection.commit()
    return

def delete_treatment(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Treatments WHERE treatmentID = %s", [id])
    mysql.connection.commit()
    return

def update_treatments(patient, medication, frequency, id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Treatmentss SET patientID=%s, medicationID=%s, frequency=%s WHERE treatmentID=%s", [patient, medication, frequency, id])
    mysql.connection.commit()
    return


@app.route('/nurses')
def nurses():
    return render_template('nurses.html')

@app.route('/patients')
def patients():
    return render_template('patients.html')

@app.route('/patientdetails')
def patientdetails():
    return render_template('patientdetails.html')

