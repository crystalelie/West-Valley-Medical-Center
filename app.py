
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import requests
import sys
app = Flask(__name__)

app.config['MYSQL_USER'] = 
app.config['MYSQL_PASSWORD'] = 
app.config['MYSQL_HOST'] = 
app.config['MYSQL_DB'] = 
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
            cur.execute("SELECT DISTINCT dosageUnit FROM Medications WHERE dosageUnit != %s ORDER BY dosage ASC", [Unit])
            unit = cur.fetchall()

            return render_template('medupdate.html', name="Medication Update", headers=headers, info=info, id=id, unit=unit)

        elif request.form.get('New'):
            id = request.form['id']
            Name = request.form['1']
            Dosage = request.form['2']
            Unit = request.form['3']
            update_medications(Name, Dosage, Unit, id)

    if not request.form.get('Filter'):
        cur.execute("SELECT * FROM Medications ORDER BY medicationName ASC")
        meds = cur.fetchall()
    
    cur.execute("SELECT DISTINCT dosage FROM Medications ORDER BY dosage ASC")
    dos = cur.fetchall()

    cur.execute("SELECT DISTINCT dosageUnit FROM Medications ORDER BY dosage ASC")
    unit = cur.fetchall()

    return render_template('medications.html', meds=meds, dos=dos, unit=unit)

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
        cur.execute("SELECT * FROM Physicians ORDER BY lastName ASC")
        phys = cur.fetchall()

    cur.execute("SELECT DISTINCT firstName FROM Physicians ORDER BY firstName ASC")
    fname = cur.fetchall()
    cur.execute("SELECT DISTINCT lastName FROM Physicians ORDER BY lastName ASC")
    lname = cur.fetchall()
    cur.execute("SELECT DISTINCT specialty FROM Physicians ORDER BY specialty ASC")
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

            headers = ["Name", "Medication", "Frequency"]
            info = [cur_name, request.form['patID'], cur_med, request.form['medID'], cur_freq]
            return render_template('treatupdate.html', name="Treatment Update", headers=headers, info=info, id=id, all_names=all_names, all_meds=medications)

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
        cur.execute("Select t.treatmentID, concat(p.firstName, ' ', p.lastName) as name, m.medicationName, m.medicationID, t.patientID, frequency, p.firstName, p.lastName FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID ORDER BY name, medicationName ASC")
        treats = cur.fetchall()

    # Creating a dictionary of distinct patient names for FILTER drop down
    cur.execute("Select DISTINCT concat(p.firstName, ' ', p.lastName) as name, t.patientID FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID ORDER BY name ASC")
    names = cur.fetchall()

    # Creating a dictionary of distinct medication names for FILTER drop down
    cur.execute("Select DISTINCT m.medicationName, t.medicationID FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID ORDER BY m.medicationName ASC")
    medications = cur.fetchall()

    # Creating a dictionary of distinct frequencies for FILTER drop down
    cur.execute("Select DISTINCT frequency FROM Treatments ORDER BY frequency ASC")
    freq = cur.fetchall()

    # Creating drop down for patients and medications that are in the current table to choose to ADD
    cur.execute("Select patientID, concat(firstName, ' ', lastName) as name FROM Patients ORDER BY name ASC")
    add_name = cur.fetchall()


    cur.execute("Select medicationID, medicationName FROM Medications ORDER BY medicationName ASC")
    add_med = cur.fetchall()


    return render_template('treatments.html', treats=treats, names=names, meds=medications, freq=freq, add_name=add_name, add_med=add_med)

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
            fname = request.form['fname']
            lname = request.form['lname']
            registered = request.form['registered']

            query = ('INSERT INTO Nurses (firstName, lastName, registered) VALUES (%s, %s, %s)')
            cur.execute(query, (fname, lname, registered))
            mysql.connection.commit()

        # Update a nurse
        if request.form.get('update'):
            id = request.form['id']
            fname = request.form['fname']
            lname = request.form['lname']
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
                cur.execute('SELECT * FROM Nurses ORDER BY lastName, firstName')

            nurses = cur.fetchall()
            headings = ('First Name', 'Last Name', 'Registered', '')


    if not request.args.get('search'):
        cur.execute('SELECT * FROM Nurses ORDER BY lastName, firstName')
        nurses = cur.fetchall()
        headings = ('First Name', 'Last Name', 'Registered', '')

    return render_template('nurses.html', nurses = nurses, headings = headings)

@app.route('/updatenurse/<int:id>', methods=['GET', 'POST'])
def updatenurse(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Nurses WHERE Nurses.nurseID = %s', (id, ))
    nurse = cur.fetchall()

    return render_template('updatenurse.html', headers= ['First Name', 'Last Name', 'Registered'], nurse=nurse)

@app.route('/patients', methods=['GET', 'POST'])
def patients():
    cur = mysql.connection.cursor()

    states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

    if request.method == 'POST':

        # Add a patient 
        if request.form.get('add'):

            ssn = request.form['ssn']
            dob = request.form['dob'] 
            fname = request.form['fname'] 
            lname = request.form['lname']   
            street= request.form['street']  
            city = request.form['city']
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
            fname = request.form['fname'] 
            lname = request.form['lname']   
            street= request.form['street']  
            city = request.form['city']
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
                cur.execute("SELECT patientID, firstName, lastName, ssn, dob as db, streetAddress, city, state, zip, phone FROM Patients WHERE firstName = LOWER(%s) ORDER BY lastName, firstName", [fname])
            
            elif fname == "" and lname != "":
                cur.execute("SELECT patientID, firstName, lastName, ssn, dob as db, streetAddress, city, state, zip, phone FROM Patients WHERE lastName = LOWER(%s) ORDER BY lastName, firstName", [lname])
                
            elif fname != "" and lname != "":
                cur.execute("SELECT patientID, firstName, lastName, ssn, dob as db, streetAddress, city, state, zip, phone FROM Patients WHERE firstName = LOWER(%s) AND lastName= LOWER(%s) ORDER BY lastName, firstName",  [fname, lname])
                
            else:
                query = cur.execute("SELECT patientID, firstName, lastName, ssn, dob as db, streetAddress, city, state, zip, phone FROM Patients ORDER BY lastName, firstName")
                cur.execute(query)


            patients = cur.fetchall()

            headings = ("First Name", "Last Name", "SSN", "Date of Birth", "Street Address", "City", "State", "Zip Code", "Phone Number", "")
        

    if not request.args.get('search'):
        cur.execute("SELECT patientID, firstName, lastName, ssn,  DATE_FORMAT(dob, '%m-%d-%Y') as db, streetAddress, city, state, zip, phone FROM Patients ORDER BY lastName, firstName")
        patients = cur.fetchall()
        cur.execute("SELECT DATE_FORMAT(dob, '%m-%d-%Y') as db FROM Patients")
        db = cur.fetchall()
        headings = ("First Name", "Last Name", "SSN", "Date of Birth", "Street Address", "City", "State", "Zip Code", "Phone Number", "")
    
    return render_template('patients.html', patients = patients, headings = headings, states=states)

@app.route('/updatepatient/<int:id>', methods=['GET', 'POST'])
def updatepatient(id):
    states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Patients WHERE Patients.patientID = %s', (id, ))
    patient = cur.fetchall()
    headers = ["First Name", "Last Name", "SSN", "Date of Birth", "Street Address", "City", "State", "Zip Code", "Phone Number"]
    
    cur.execute('SELECT state FROM Patients WHERE patientID = %s', [id])
    curr_state= cur.fetchall()
    print("STATED" + str(curr_state[0]), file=sys.stderr)
    #del states[curr_state[0].state]
    return render_template('updatepatient.html', headers=headers, patient=patient, states=states)

@app.route('/patientdetails', methods=['GET', 'POST'])
def patientdetails():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
            
        # Add new patient details
        if request.form.get('add'):

            patient = request.form['patient']
            physician = request.form['physician']
            nurse = request.form['nurse']
            if nurse == '':
                query = 'INSERT INTO PatientDetails (patientID, physicianID) VALUES (%s, %s)'
                cur.execute(query, (patient, physician))
                mysql.connection.commit()
            else:
                query = 'INSERT INTO PatientDetails (patientID, physicianID, nurseID) VALUES (%s, %s, %s)'
                cur.execute(query, (patient, physician, nurse))
                mysql.connection.commit()

    # Update patient details 
        if request.form.get('update'):

            pid = request.form['pid']
            mdid = request.form['mdid']

            if request.form['nid']:
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
            cur.execute('''SELECT p.patientID, CONCAT(p.firstName, ' ', p.lastName) as patientName FROM Patients p WHERE p.patientID NOT IN '''
            '''(SELECT pd.patientID FROM PatientDetails pd)''')
            patients = cur.fetchall()

            # get physicians
            cur.execute('''SELECT Physicians.physicianID, CONCAT(Physicians.firstName, ' ', Physicians.lastName) as mdName FROM Physicians ''')
            physicians = cur.fetchall()

            # get nurses
            cur.execute('''SELECT Nurses.nurseID, CONCAT(Nurses.firstName, ' ', Nurses.lastName) nurseName FROM Nurses ''')
            nurses = cur.fetchall()

    if not request.args.get('search') or request.args.get('Reset'):

        # get data for directory table
        cur.execute('''SELECT p.patientID, CONCAT (p.firstName, ' ', p.lastName) as patient, CONCAT (md.firstName, ' ', md.lastName) as physician, IFNULL(concat(n.firstName, ' ', n.lastName), "None") as nurse'''
        ''' FROM PatientDetails pd'''
        ''' INNER JOIN Patients p ON pd.patientID = p.patientID''' 
        ''' INNER JOIN Physicians md ON pd.physicianID = md.physicianID''' 
        ''' LEFT JOIN Nurses n ON pd.nurseID = n.nurseID ORDER BY p.lastName, p.firstName''')
        pd = cur.fetchall()

        # get patients not already in PatientDetails
        cur.execute('''SELECT p.patientID, CONCAT(p.firstName, ' ', p.lastName) as patientName FROM Patients p WHERE p.patientID NOT IN '''
        '''(SELECT pd.patientID FROM PatientDetails pd) ORDER BY p.lastName, p.firstName''')
        patients = cur.fetchall()

        # get physicians
        cur.execute('''SELECT Physicians.physicianID, CONCAT(Physicians.firstName, ' ', Physicians.lastName) as mdName FROM Physicians ORDER BY Physicians.lastName, Physicians.firstName''')
        physicians = cur.fetchall()

        # get nurses
        cur.execute('''SELECT Nurses.nurseID, CONCAT(Nurses.firstName, ' ', Nurses.lastName) as nurseName FROM Nurses ORDER BY Nurses.lastName, Nurses.firstName''')
        nurses = cur.fetchall()

    headings = ('Patient', 'Physician', 'Nurse', '')
    return render_template('patientdetails.html', pd = pd, patients = patients, physicians = physicians, nurses = nurses, headings = headings)

@app.route('/updatepd/<int:id>', methods=['GET', 'POST'])
def updatepd(id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT p.patientID, CONCAT (p.firstName, ' ', p.lastName) as patient, md.physicianID, CONCAT (md.firstName, ' ', md.lastName) as physician, n.nurseID, IFNULL(concat(n.firstName, ' ', n.lastName), "None") as nurse'''
        ''' FROM PatientDetails pd'''
        ''' INNER JOIN Patients p ON pd.patientID = p.patientID''' 
        ''' INNER JOIN Physicians md ON pd.physicianID = md.physicianID''' 
        ''' LEFT JOIN Nurses n ON pd.nurseID = n.nurseID WHERE pd.patientID = %s''', (id, ))
    curr = cur.fetchall()

    cur.execute('SELECT physicianID, CONCAT(firstName, " ", lastName) as physName FROM Physicians WHERE physicianID NOT IN (SELECT physicianID FROM PatientDetails WHERE patientID = %s)', [id])
    all_phys = cur.fetchall()

    cur.execute('SELECT nurseID, CONCAT(firstName, " ", lastName) as nursName FROM Nurses WHERE nurseID NOT IN (SELECT nurseID FROM PatientDetails WHERE patientID = %s)', [id])
    all_nurse = cur.fetchall()

    if all_nurse == ():
        cur.execute('SELECT nurseID, CONCAT(firstName, " ", lastName) as nursName FROM Nurses')
        all_nurse = cur.fetchall()

    return render_template('updatepd.html', headers=['Patient', 'Physician', 'Nurse'], curr = curr, all_phys = all_phys, all_nurse=all_nurse)

if __name__ == "__main__":
    app.run('127.0.0.1', port=60000, debug=True)
