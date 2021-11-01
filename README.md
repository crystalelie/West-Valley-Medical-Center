# West-Valley-Medical-Center #

# Overview #
West Valley Medical Center is a database driven web application designed to manage rooms, patients, physicians, treatments, and surgeries for the West Valley Medical Center. It does this by providing a listing of each of the entities as well as allowing users to add, modify, and delete information from the entities. 
The metropolitan area surround West Valley Medical Center has a population of around 100,000. On average, the medical center sees 30,000 patients per year and has 190 staffed rooms. Every time that a new patient visits the medical center, they have to provide multiple pieces of information and may see various physicians, go through various treatments and surgeries, and overall, will need to have their record stored for future visits. By having a backend database, West Valley Medical Center’s administrative staff is able to effectively store and process their patients’ data each day. Since the administrative staff consists of around 75 individuals, this database will allow them to work together to enter in patient information. With this database driven web application, we are able to meet the needs of the West Valley Medical Center and help them better serve their patients.

# Database Outline #
### Patients ###
An individual who visits the West Valley Medical Center needs to provide mandatory personal information to be added to their patient record at the hospital. Each patient provides basic information about themselves and has an assigned patient ID.
-	patientID: int, unique, not NULL, PK
-	ssn: varchar(9), unique, not NULL
-	firstName: varchar (255), not NULL
-	lastName: varchar (255), not NULL
-	streetAddress: varchar (255), not NULL
-	city: varchar (255), not NULL
-	state: varchar (2), not NULL
-	zip: varchar (5), not NULL
-	phone: varchar(12), not NULL

### Patient Details ###
An individual who visits the West Valley Medical Center will have more information added to their patient record at the hospital. This information is regarding their current stay at the hospital. This includes their patient id, physician id, and room id.
-	patientID, int, unique, not NULL, FK
-	physicianID: int, not Null, FK
-	nurseID: int, FK 

### Physicians ###
All physicians at the West Valley Medical Center will have their information recorded in the system. The necessary information includes their physician id, first name, last name, and their specialty.
-	physicianID: int, unique, not NULL, PK
-	firstName: varchar (255), not NULL
-	lastName: varchar (255), not NULL
-	specialty: varchar (255), not NULL

### Nurses ###
All nurses at the West Valley Medical Center will have their information recorded in the system. The necessary information includes their nurse id, first name, last name, and if they are registered or not.
-	nurseID: int, unique, not NULL, PK
-	firstName: varchar (255), not NULL
-	lastName: varchar (255),  not NULL
-	registered: BOOLEAN, not NULL

### Medications ###
All medications that Physicians at the West Valley Medical Center can prescribe will be included in the system. Each medication will have a medication id, medication name dosage and dosage unit.
-	medicationID: int, unique, not NULL, PK
-	medicationName: varchar (255), not NULL
-	dosage: int, not NULL
-	dosageUnit: varchar(255), not NULL

### Treatments ###
The West Valley Medical Center keeps records of all treatment plans that patients are going through during their stay. This can include one or more lines for each patient id, since a patient can take one or more medications.
-	treatmentID: int, auto_increment, not NULL, PK
-	patientID: int, not NULL, FK
-	medicationID: int, not NULL, FK

## Relationships ##
- M:M relationship between Medications and Patient Details is implemented with medicationID and patientID as a FKs in Treatments.
- 1:M relationship between Nurses and Patient Details is implemented with nurseID as a FK inside of Patient Details. 
- 1:1 relationship between Patients and Patient Details is implemented with patientID as a FK inside of Patients Details. 
- 1:M relationship between Nurses and Patient Details is implemented with nurseID as a FK inside of Patient Details.
