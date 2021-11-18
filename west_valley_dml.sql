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

-- get medications based on submission of the search medications form 
SELECT medicationName, dosage, dosageUnit 
FROM medication
WHERE medicationName = :medicationNameInput;

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

-- get physician based on submission of search by specialty form 
SELECT * FROM physicians
WHERE specialty = :specialtyInput;

-- delete a physician
DELETE FROM physicians
WHERE physicianID = :physicianID_from_table_row_where_delete_button_used;



-- *** QUERIES FOR TREATMENTS PAGE ***

-- get all treatments to display in treatments directory
SELECT * FROM treatments

-- add a new treatment
INSERT INTO treatments (patientID, medicationID, medicationFrequency)
VALUES (:patientID_input, :medicationID_input, :medicationFrequency_input);

-- update a treatment based on submission of update treatment form 
UPDATE treatments
SET patientID = :patientID_input, medicationID = :medicationID_input, medicationFrequency = :medicationFrequency_input
WHERE treatmentID = :treatmentID_input

-- get treatment based on submission of filter by patient form 
SELECT * FROM treatments
WHERE patientID = :patientID_input

-- delete a treatment
DELETE FROM treatments
WHERE treatmentID = :treatmentID_from_table_row_where_delete_button_used;




