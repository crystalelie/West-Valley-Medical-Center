-- *** QUERIES FOR MEDICATIONS PAGE ***

-- get all medications to display them in medications directory
SELECT * FROM medications;

-- add a new medication
INSERT INTO medications (medicationName, dosage, dosageUnit)
VALUES (:medicationNameInput, :dosageInput, :dosageUnit_from_dropdown_Input);   

-- update a medication based on submission of the update medication form 
UPDATE medications 
SET medicationName = :medicationNameInput, dosage = :dosageInput, dosageUnit = :dosageUnit_from_dropdown_Input
WHERE medicationID = :medicationIID_from_update_form; 

-- filtering based on either medication name, dosage, or dosage unit
-- filter by medication name
SELECT * FROM Medications WHERE medicationName:medicationNameInput

-- filter by dosage
SELECT * FROM Medications WHERE dosage:dosageInput

-- filter by dosage unit
SELECT * FROM Medications WHERE dosageUnit:dosageUnitInput

-- for filter form, filling with distinct dosages on the drop down
SELECT DISTINCT dosage FROM Medications

-- delete a medication 
DELETE FROM medications
WHERE medicationID = :medicationID_from_table_row_where_delete_button_used;



-- *** QUERIES FOR NURSES PAGE ***

-- get all nurses to display them in nurse directory 
SELECT * FROM nurses;

-- add a new nurse 
INSERT INTO nurses (firstName, lastName, registered)
VALUES (:firstNameInput, :lastNameInput, :registered_status_from_dropdown_input);

-- update a nurse based on submission of the update nurse form 
UPDATE nurses
SET firstName = :firstNameInput, lastName = :lastNameInput, registered = :registered_status_from_dropdown_input
WHERE nurseID = :nurseID_from_update_form;

-- get nurses based on submission of the search nurses form (if only first OR last name given)
SELECT firstName, lastName, registeted 
FROM nurses
WHERE firstName = :nameInput OR lastName = :nameInput;

-- get nurses based on submission of the search nurses form (if first AND last name given)
SELECT *
FROM nurses
WHERE firstName = :firstNameInput AND lastName = :lastNameInput;

-- delete a nurse
DELETE FROM nurses
WHERE nurseID = :nurseID_from_table_row_where_delete_button_used;



-- *** QUERIES FOR PATIENTS PAGE ***

-- get all patients to display them in patient directory
SELECT * FROM patients;

-- add a patient
INSERT INTO patients (ssn, dob, firstName, lastName, streetAddress, city, state, zip, phone)
VALUES (:ssnInput, :dobInput, :firstNameInput, :lastNameInput, :streetAddressInput, :cityInput, :stateInput, :zipInput, :phoneInput);

-- update a patient based on submission of update patient form 
UPDATE patients
SET ssn = :ssnInput, dob = dobInput, firstName = :firstNameInput, lastName = :lastNameInput, streetAddress = :streetAddressInput, city = :cityInput, state = :stateInput, zip = :zipInput, phone = :phoneInput
WHERE patientID = :patientID_from_upate_form;

-- get patient based on submission of patient search form (if only first OR last name given)
SELECT * FROM patients
WHERE firstName = :nameInput OR lastName = :nameInput;

-- get patient based on submission of patient search form (if first and last name given)
SELECT * FROM patients
WHERE firstName = :firstNameInput AND lastName = :lastNameInput; 

-- delete a patient
DELETE FROM patients
WHERE patientID = :patientID_from_table_row_where_delete_button_used;


-- *** QUERIES FOR PATIENT DETAILS PAGE ***

-- get all patient details to display them in patient details directory
SELECT * FROM patient_details;

-- add patient details
INSERT INTO patient_details (patientID, physicianID, nurseID)
VALUES (:patientID_input, :physicianID_input, :nurseID_input);

-- update patient details based on submission of update patient details form 
UPDATE patient_details 
SET physicianID = :physicianID_input, nurseID = :nurseID_input
WHERE patientID = :patientID_input

-- get patient based on submission of search patient details form 
SELECT * FROM patient_details
WHERE patientID = :patientID_input;

-- delete a patient detail
DELETE FROM patient_details
WHERE patientID = :patientID_from_table_row_where_delete_button_used;



-- *** QUERIES FOR PHYSICIANS PAGE ***

-- get all physicians to display in physicians directory
SELECT * FROM physicians;

-- add a new physician
INSERT INTO physicians (firstName, lastName, specialty)
VALUES(:firstNameInput, :lastNameInput, :specialtyInput);

-- update a physician based on submission of update physician form 
UPDATE physicians
SET firstName = :firstNameInput, lastName = :lastNameInput, specialty = :specialtyInput
WHERE physicianID = :physicianID_input 

-- filtering based on either physician first name, last name, or specialty

-- filter by first name
SELECT * FROM Physicians WHERE firstName:firstNameInput

-- filter by last name
SELECT * FROM Physicians WHERE lastName:lastNameInput

-- filter by specialty
SELECT * FROM Physicians WHERE specialty:specialtyInput

-- for filter form, filling with distinct first names on the drop down
SELECT DISTINCT firstName FROM Physicians

-- for filter form, filling with distinct last names on the drop down
SELECT DISTINCT lastName FROM Physicians

-- for filter form, filling with distinct specialties on the drop down
SELECT DISTINCT specialty FROM Physicians

-- delete a physician
DELETE FROM physicians
WHERE physicianID = :physicianID_from_table_row_where_delete_button_used;



-- *** QUERIES FOR TREATMENTS PAGE ***

-- get all treatments to display in treatments directory
Select t.treatmentID, concat(p.firstName, ' ', p.lastName) as name, m.medicationName, t.medicationID, t.patientID, frequency, p.firstName, p.lastName 
FROM Treatments t 
LEFT JOIN Patients p on t.patientID = p.patientID 
LEFT JOIN Medications m on t.medicationID = m.medicationID

-- add a new treatment
INSERT INTO treatments (patientID, medicationID, medicationFrequency)
VALUES (:patientID_input, :medicationID_input, :medicationFrequency_input);

-- update a treatment based on submission of update treatment form 
UPDATE treatments
SET patientID = :patientID_input, medicationID = :medicationID_input, medicationFrequency = :medicationFrequency_input
WHERE treatmentID = :treatmentID_input

-- Update page drop down for Distinct values for patient, medication and frequency
-- Patient
Select DISTINCT concat(p.firstName, ' ', p.lastName) as name, p.patientID FROM Patients p WHERE p.firstName != firstNameInput and p.lastName != lastNameInput

-- Medication
Select DISTINCT m.medicationName, m.medicationID FROM Medications m WHERE m.medicationName != medicationNameInput

-- Frequency
Select DISTINCT frequency FROM Treatments WHERE frequency != frequencyInput


-- filtering based on either patient, medication, or frequency

-- filter by patient
Select concat(p.firstName, ' ', p.lastName) as name, m.medicationName, frequency FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID WHERE t.patientID:patientIDInput

-- filter by medication
Select concat(p.firstName, ' ', p.lastName) as name, m.medicationName, frequency FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID WHERE t.medicationID:medicationIDInput

-- filter by frequency
Select concat(p.firstName, ' ', p.lastName) as name, m.medicationName, frequency FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID WHERE t.frequency:frequencyInput

-- for filter form, filling with distinct patient names on the drop down
Select DISTINCT concat(p.firstName, ' ', p.lastName) as name, t.patientID FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID

-- for filter form, filling with distinct medication names on the drop down
Select DISTINCT m.medicationName, t.medicationID FROM Treatments t LEFT JOIN Patients p on t.patientID = p.patientID LEFT JOIN Medications m on t.medicationID = m.medicationID

-- for filter form, filling with distinct frequencies on the drop down
Select DISTINCT frequency FROM Treatments

-- for add form, drop down of all patients in the system
Select concat(firstName, ' ', lastName) as name, patientID FROM Patients

-- for add form, drop down of all medications in the system
Select medicationName, medicationID FROM Medications

-- delete a treatment
DELETE FROM treatments
WHERE treatmentID = :treatmentID_from_table_row_where_delete_button_used;




