# West-Valley-Medical-Center #

- [Overview](#overview)
- [Database Outline](#database-outline)
- [Relationships](#relationships)
- [ER Diagram](#er-diagram)
- [Schema](#schema)
- [UI Screenshots](#ui-screenshots)

# Overview #
West Valley Medical Center is a database driven web application designed to manage rooms, patients, physicians, treatments, and surgeries for the West Valley Medical Center. It does this by providing a listing of each of the entities as well as allowing users to add, modify, and delete information from the entities. 

The metropolitan area surround West Valley Medical Center has a population of around 100,000. On average, the medical center sees 30,000 patients per year and has 190 staffed rooms. Every time that a new patient visits the medical center, they have to provide multiple pieces of information and may see various physicians, go through various treatments and surgeries, and overall, will need to have their record stored for future visits. By having a backend database, West Valley Medical Center’s administrative staff is able to effectively store and process their patients’ data each day. Since the administrative staff consists of around 75 individuals, this database will allow them to work together to enter in patient information. With this database driven web application, we are able to meet the needs of the West Valley Medical Center and help them better serve their patients.

# Database Outline #
### Patients ###
An individual who visits the West Valley Medical Center needs to provide mandatory personal information to be added to their patient record at the hospital. Each patient provides basic information about themselves and has an assigned patient ID.
- patientID: int(11), auto_increment, not NULL, PK
- firstName: varchar (255), not NULL
- lastName: varchar (255), not NULL
- ssn: varchar(9), not NULL
- dob: date, not NULL
- streetAddress: varchar (255), not NULL
- city: varchar (255), not NULL
- state: varchar (2), not NULL
- zip: varchar (5), not NULL
- phone: varchar(12), not NULL


### Patient Details ###
An individual who visits the West Valley Medical Center will have more information added to their patient record at the hospital. This information is regarding their current stay at the hospital. This includes their patient id, physician id, and room id.
- patientID, int(11), not NULL, PK, FK
- physicianID: int(11), DEFAULT NULL, FK
- nurseID: int(11), DEFAULT NULL, FK


### Physicians ###
All physicians at the West Valley Medical Center will have their information recorded in the system. The necessary information includes their physician id, first name, last name, and their specialty.
-	physicianID: int(11), auto_increment, not NULL, PK
-	firstName: varchar (255), not NULL
-	lastName: varchar (255), not NULL
-	specialty: varchar (255), not NULL

### Nurses ###
All nurses at the West Valley Medical Center will have their information recorded in the system. The necessary information includes their nurse id, first name, last name, and if they are registered or not.
-	nurseID: int(11), auto_increment,  not NULL, PK
-	firstName: varchar (255), not NULL
-	lastName: varchar (255),  not NULL
-	registered: tinyint(1), not NULL

### Medications ###
All medications that Physicians at the West Valley Medical Center can prescribe will be included in the system. Each medication will have a medication id, medication name dosage and dosage unit.
-	medicationID: int(11), auto_increment, not NULL, PK
-	medicationName: varchar (255), not NULL
-	dosage: int(11), not NULL
-	dosageUnit: varchar(2), not NULL

### Treatments ###
The West Valley Medical Center keeps records of all treatment plans that patients are going through during their stay. This can include one or more lines for each patient id, since a patient can take one or more medications.
- treatmentID: int(11), auto_increment, not NULL, PK
- patientID: int(11), not NULL, FK
- medicationID: int(11), not NULL, FK
- frequency: varchar(4), not NULL


# Relationships #
- M:M relationship between Medications and Patient Details is implemented with medicationID and patientID as a FKs in Treatments.
- 1:M relationship between Nurses and Patient Details is implemented with nurseID as a FK inside of Patient Details. This relationship allows for partial participation.
- 1:1 relationship between Patients and Patient Details is implemented with patientID as a FK inside of Patients Details. 
- 1:M relationship between Physicians and Patient Details is implemented with physicianID as a FK inside of Patient Details. This relationship allows for partial participation.


# ER Diagram #
![Screen Shot 2021-11-26 at 11 37 24 AM](https://user-images.githubusercontent.com/71612128/143620289-7cd3404e-3af1-4c46-adf0-d3ffde690fce.png)


# Schema #
![Screen Shot 2021-11-26 at 11 18 34 AM](https://user-images.githubusercontent.com/71612128/143620306-58890ea5-f1db-473f-9655-815877231845.png)

# UI Screenshots
