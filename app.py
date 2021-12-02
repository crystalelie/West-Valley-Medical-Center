
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
    dos = 0

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
            if request.form['filter1'] == "Med":
                med = request.form['result']
                cur.execute("SELECT * FROM Medications WHERE medicationID = %s", [med])
                meds = cur.fetchall()

            elif request.form['filter1'] == "Dos":
                dosage = request.form['result1']
                cur.execute("SELECT * FROM Medications WHERE dosage = %s", [dosage])
                meds = cur.fetchall()

            elif request.form['filter1'] == 'Unit':
                unit = request.form['result2']
                cur.execute("SELECT * FROM Medications WHERE dosageUnit = %s", [unit])
                meds = cur.fetchall()

        elif request.form.get('Update'):
            id = request.form['id']
            Name = request.form['name']
            Dosage = request.form['dosage']
            Unit = request.form['unit']
            headers = ["Name", "Dosage", "Unit"]
            info = [Name, Dosage, Unit]
            return render_template('medupdate.html', name="Medication Update", headers=headers, info=info, id=id, length=len(info))

        elif request.form.get('New'):
            id = request.form['id']
            Name = request.form['1']
            Dosage = request.form['2']
            Unit = request.form['3']
            update_medications(Name, Dosage, Unit, id)

    if not request.form.get('Filter'):
        cur.execute("SELECT * FROM Medications")
        meds = cur.fetchall()
    
    cur.execute("SELECT DISTINCT dosage FROM Medications")
    dos = cur.fetchall()

    return render_template('medications.html', meds=meds, dos=dos)

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
    cur.execute("SELECT * FROM Physicians")
    phys = cur.fetchall()

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
            return render_template('physicianupdate.html', name="Physician Update", headers=headers, info=info, id=id, length=len(info))

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

            elif request.form['filter1'] == 'spec':
                spec = request.form['result2']
                cur.execute("SELECT * FROM Physicians WHERE specialty = %s", [spec])
                phys = cur.fetchall()

    if not request.form.get('Filter'):
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
    cur.execute("Select t.treatmentID, concat(p.firstName, ' ', p.lastName) as name, m.medicationName, t.medicationID, t.patientID, frequency, p.firstName, p.lastName FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID")
    treats = cur.fetchall()

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
            cur_name = request.form['fname'] + " " + request.form['lname']

            cur.execute("Select DISTINCT concat(p.firstName, ' ', p.lastName) as name, p.patientID FROM Patients p WHERE p.firstName !=%s and p.lastName !=%s", [request.form['fname'], request.form['lname']])
            all_names = cur.fetchall()

            cur_med = request.form['medication']
            cur.execute("Select DISTINCT m.medicationName, m.medicationID FROM Medications m WHERE m.medicationName !=%s", [cur_med])
            medications = cur.fetchall()

            cur_freq = request.form['frequency']
            cur.execute("Select DISTINCT frequency FROM Treatments WHERE frequency !=%s", [cur_freq])
            all_freq = cur.fetchall()

            headers = ["Name", "Medication", "Frequency"]
            info = [cur_name, request.form['patID'], cur_med, request.form['medID'], cur_freq]
            return render_template('treatupdate.html', name="Treatment Update", headers=headers, info=info, id=id, all_names=all_names, all_meds=medications, all_freq=all_freq)

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

    if not request.form.get('Filter'):
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
    cur.execute("UPDATE Treatments SET patientID=%s, medicationID=%s, frequency=%s WHERE treatmentID=%s", [patient, medication, frequency, id])
    mysql.connection.commit()
    return


@app.route('/nurses', methods=['GET', 'POST'])
def nurses():
    cur = mysql.connection.cursor()

    if request.method == 'POST':

        # Add a nurse
        if request.form.get('add'):
            fname = request.form['fname'].capitalize() 
            lname = request.form['lname'].capitalize() 
            registered = request.form['registered']

            query = ('INSERT INTO Nurses (firstName, lastName, registered) VALUES (%s, %s, %s)')
            cur.execute(query, (fname, lname, registered))
            mysql.connection.commit()

        # Update a nurse
        if request.form.get('update'):
            id = request.form['id']
            fname = request.form['fname'].capitalize() 
            lname = request.form['lname'].capitalize() 
            registered = request.form['registered']

            query = ('UPDATE Nurses SET firstName=%s, lastName=%s, registered=%s WHERE nurseID=%s')
            cur.execute(query, (fname, lname, registered, id))
            mysql.connection.commit()

        # Delete a nurse
        if request.form.get('delete'):
            id = request.form['id']
            cur.execute('DELETE FROM Nurses WHERE Nurses.nurseID = %s', (id, ))
            mysql.connection.commit()

    if request.method == 'GET':
        # Search for nurse
        if request.args.get('search'):
            fname = request.args['fname'].lower()
            lname = request.args['lname'].lower()

            if fname != '' and lname == '':
                cur.execute('SELECT * FROM Nurses WHERE Nurses.firstName = LOWER(%s)', (fname, ))
            elif fname == '' and lname != '':
                cur.execute('SELECT * FROM Nurses WHERE Nurses.lastName = LOWER(%s)', (lname, ))
            elif fname != '' and lname != '':
                cur.execute('SELECT * FROM Nurses WHERE Nurses.firstName = LOWER(%s) and Nurses.lastName = LOWER(%s)', (fname, lname))
            else: 
                cur.execute('SELECT * FROM Nurses')

            nurses = cur.fetchall()
            headings = ('First Name', 'Last Name', 'Registered', '')


    if not request.args.get('search'):
        cur.execute('SELECT * FROM Nurses')
        nurses = cur.fetchall()
        headings = ('First Name', 'Last Name', 'Registered', '')

    return render_template('nurses.html', nurses = nurses, headings = headings)

@app.route('/updatenurse/<int:id>', methods=['GET', 'POST'])
def updatenurse(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Nurses WHERE Nurses.nurseID = %s', (id, ))
    nurse = cur.fetchall()
    return render_template('updatenurse.html', nurse=nurse)

@app.route('/patients', methods=['GET', 'POST'])
def patients():
    cur = mysql.connection.cursor()

    if request.method == 'POST':

        # Add a patient 
        if request.form.get('add'):

            ssn = request.form['ssn']
            dob = request.form['dob'] 
            fname = request.form['fname'].capitalize()
            lname = request.form['lname'].capitalize()   
            street= request.form['street']  
            city = request.form['city'].capitalize()
            state = request.form['state']
            zip = request.form['zip']
            phone = request.form['phone']

            query = 'INSERT INTO Patients (ssn, dob, firstName, lastName, streetAddress, city, state, zip, phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cur.execute(query, (ssn, dob, fname, lname, street, city, state, zip, phone))
            mysql.connection.commit()
    
        # Update a patient
        if request.form.get('update'):

            id = request.form['id']
            ssn = request.form['ssn']
            dob = request.form['dob'] 
            fname = request.form['fname'].capitalize()  
            lname = request.form['lname'].capitalize()    
            street= request.form['street']  
            city = request.form['city'].capitalize() 
            state = request.form['state']
            zip = request.form['zip']
            phone = request.form['phone']

            query = 'UPDATE Patients SET ssn=%s, dob=%s, firstName=%s, lastName=%s, streetAddress=%s, city=%s, state=%s, zip=%s, phone=%s WHERE patientID = %s'
            cur.execute(query, (ssn, dob, fname, lname, street, city, state, zip, phone, id))
            mysql.connection.commit()

        # Delete a patient
        if request.form.get('delete'):
            
            id = request.form['id']
            cur.execute('DELETE FROM Patients WHERE Patients.patientID = %s', (id, ))
            mysql.connection.commit()

    if request.method == 'GET': 

        # search for patient
        if request.args.get('search'):
            
            fname = request.args['fname'].lower()
            lname = request.args['lname'].lower()

            if fname != "" and lname == "":
                query = 'SELECT * FROM Patients WHERE Patients.firstName = LOWER(%s)'
                cur.execute(query, (fname, ))
            
            elif fname == "" and lname != "":
                query = 'SELECT * FROM Patients WHERE Patients.lastName = lOWER(%s)'
                cur.execute(query, (lname, ))
            elif fname != "" and lname != "":
                query = 'SELECT * FROM Patients WHERE Patients.firstName = LOWER(%s) and Patients.lastName = LOWER(%s)'
                cur.execute(query, (fname, lname))
            else:
                query = 'SELECT * FROM Patients'
                cur.execute(query)

            patients = cur.fetchall()
            headings = ("SSN", "DOB", "First Name", "Last Name", "Street Address", "City", "State", "Zip Code", "Phone Number", "")
        

    if not request.args.get('search'):
        cur.execute("SELECT * FROM Patients")
        patients = cur.fetchall()
        headings = ("SSN", "DOB", "First Name", "Last Name", "Street Address", "City", "State", "Zip Code", "Phone Number", "")
    
    return render_template('patients.html', patients = patients, headings = headings)

@app.route('/updatepatient/<int:id>', methods=['GET', 'POST'])
def updatepatient(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Patients WHERE Patients.patientID = %s', (id, ))
    patient = cur.fetchall()
    return render_template('updatepatient.html', patient=patient)

@app.route('/patientdetails', methods=['GET', 'POST'])
def patientdetails():
    cur = mysql.connection.cursor()

    if request.method == 'POST':

        # Add new patient details
        if request.form.get('add'):

            patient = request.form['patient']
            physician = request.form['physician']

            if request.form['nurse'] != 'None':
                nurse = request.form['nurse']
                query = 'INSERT INTO PatientDetails (patientID, physicianID, nurseID) VALUES (%s, %s, %s)'
                cur.execute(query, (patient, physician, nurse))
                mysql.connection.commit()
            
            else:
                query = 'INSERT INTO PatientDetails (patientID, physicianID, nurseID) VALUES (%s, %s, NULL)'
                cur.execute(query, (patient, physician))
                mysql.connection.commit()

    # Update patient details 
        if request.form.get('update'):

            pid = request.form['pid']
            mdid = request.form['mdid']

            if request.form['nid'] != 'None':
                nid = request.form['nid']
                query = 'UPDATE PatientDetails SET physicianID=%s, nurseID=%s WHERE patientID=%s'
                cur.execute(query, (mdid, nid, pid))
                mysql.connection.commit()
            else: 
                query = 'UPDATE PatientDetails SET physicianID=%s, nurseID=NULL WHERE patientID=%s'
                cur.execute(query, (mdid, pid))
                mysql.connection.commit()

    # Delete patient details 
        if request.form.get('delete'):
            id = request.form['id']
            cur.execute('DELETE FROM PatientDetails WHERE patientID=%s', (id, ))
            mysql.connection.commit()


    if request.method == 'GET':

        # Search for patient details
        if request.args.get('search'):

            # get data for directory table
            patient = request.args['patient']
            cur.execute('''SELECT p.patientID, CONCAT (p.firstName, ' ', p.lastName) as patient, md.physicianID, CONCAT (md.firstName, ' ', md.lastName) as physician, n.nurseID, CONCAT (n.firstName, ' ', n.lastName) as nurse'''
            ''' FROM PatientDetails pd'''
            ''' INNER JOIN Patients p ON pd.patientID = p.patientID''' 
            ''' INNER JOIN Physicians md ON pd.physicianID = md.physicianID''' 
            ''' LEFT JOIN Nurses n ON pd.nurseID = n.nurseID'''
            ''' WHERE p.patientID = %s''', (patient, ))
            pd = cur.fetchall()

            # get patients not already in PatientDetails
            cur.execute('''SELECT Patients.patientID, CONCAT(Patients.firstName, ' ', Patients.lastName) as patientName FROM Patients WHERE Patients.patientID NOT IN '''
            '''(SELECT PatientDetails.patientID FROM PatientDetails)''')
            patients = cur.fetchall()

            # get physicians
            cur.execute('''SELECT Physicians.physicianID, CONCAT(Physicians.firstName, ' ', Physicians.lastName) as mdName FROM Physicians ''')
            physicians = cur.fetchall()

            # get nurses
            cur.execute('''SELECT Nurses.nurseID, CONCAT(Nurses.firstName, ' ', Nurses.lastNAme) nurseName FROM Nurses ''')
            nurses = cur.fetchall()

    if not request.args.get('search'):

        # get data for directory table
        cur.execute('''SELECT p.patientID, CONCAT (p.firstName, ' ', p.lastName) as patient, CONCAT (md.firstName, ' ', md.lastName) as physician, concat(n.firstName, ' ', n.lastName) as nurse'''
        ''' FROM PatientDetails pd'''
        ''' INNER JOIN Patients p ON pd.patientID = p.patientID''' 
        ''' INNER JOIN Physicians md ON pd.physicianID = md.physicianID''' 
        ''' LEFT JOIN Nurses n ON pd.nurseID = n.nurseID''')
        pd = cur.fetchall()

        # get patients not already in PatientDetails
        cur.execute('''SELECT Patients.patientID, CONCAT(Patients.firstName, ' ', Patients.lastName) as patientName FROM Patients WHERE Patients.patientID NOT IN '''
        '''(SELECT PatientDetails.patientID FROM PatientDetails)''')
        patients = cur.fetchall()

        # get physicians
        cur.execute('''SELECT Physicians.physicianID, CONCAT(Physicians.firstName, ' ', Physicians.lastName) as mdName FROM Physicians ''')
        physicians = cur.fetchall()

        # get nurses
        cur.execute('''SELECT Nurses.nurseID, CONCAT(Nurses.firstName, ' ', Nurses.lastNAme) as nurseName FROM Nurses ''')
        nurses = cur.fetchall()

    headings = ('Patient', 'Physician', 'Nurse', '')
    return render_template('patientdetails.html', pd = pd, patients = patients, physicians = physicians, nurses = nurses, headings = headings)

@app.route('/updatepd/<int:id>', methods=['GET', 'POST'])
def updatepd(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM PatientDetails WHERE PatientDetails.patientID = %s', (id, ))
    pd = cur.fetchall()

    # get patient's name 
    cur.execute('''SELECT CONCAT(Patients.firstName, ' ', Patients.lastName) as patientName FROM Patients WHERE Patients.patientID=%s''', (id, ))
    patientname = cur.fetchall()

    # get physicians
    cur.execute('''SELECT Physicians.physicianID, CONCAT(Physicians.firstName, ' ', Physicians.lastName) as mdName FROM Physicians ''')
    physicians = cur.fetchall()

    # get nurses
    cur.execute('''SELECT Nurses.nurseID, CONCAT(Nurses.firstName, ' ', Nurses.lastNAme) nurseName FROM Nurses ''')
    nurses = cur.fetchall()

    return render_template('updatepd.html', pd = pd, physicians = physicians, nurses = nurses, patientname = patientname)


if __name__ == "__main__":
    app.run('127.0.0.1', port=5010, debug=True)

