-- phpMyAdmin SQL Dump
-- version 5.1.1-1.el7.remi
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 10, 2021 at 01:49 AM
-- Server version: 10.4.21-MariaDB-log
-- PHP Version: 7.4.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_eliec`
--

-- --------------------------------------------------------

--
-- Table structure for table `Medications`
--
DROP TABLE IF EXISTS `Medications`;
CREATE TABLE `Medications` (
  `medicationID` int(11) NOT NULL,
  `medicationName` varchar(255) NOT NULL,
  `dosage` int(11) NOT NULL,
  `dosageUnit` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Medications`
--

INSERT INTO `Medications` (`medicationID`, `medicationName`, `dosage`, `dosageUnit`) VALUES
(1, 'Ibuprofen', 200, 'mg'),
(2, 'Amoxicillin', 300, 'mg'),
(3, 'Diphenhydramine', 50, 'mg'),
(4, 'Prozac', 60, 'mg'),
(5, 'Xanax', 1, 'mg');

-- --------------------------------------------------------

--
-- Table structure for table `Nurses`
--

DROP TABLE IF EXISTS `Nurses`;
CREATE TABLE `Nurses` (
  `nurseID` int(11) NOT NULL,
  `firstName` varchar(255) NOT NULL,
  `lastName` varchar(255) NOT NULL,
  `registered` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Nurses`
--

INSERT INTO `Nurses` (`nurseID`, `firstName`, `lastName`, `registered`) VALUES
(1, 'Janet', 'Freeman', 1),
(2, 'Kelly', 'Franklin', 0),
(3, 'Dale', 'Ohlsen', 1),
(4, 'Kristen', 'Simmons', 1),
(5, 'Tyler', 'Johnson', 1);

-- --------------------------------------------------------

--
-- Table structure for table `PatientDetails`
--

DROP TABLE IF EXISTS `PatientDetails`;
CREATE TABLE `PatientDetails` (
  `patientID` int(11) NOT NULL,
  `physicianID` int(11) NOT NULL,
  `nurseID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `PatientDetails`
--

INSERT INTO `PatientDetails` (`patientID`, `physicianID`, `nurseID`) VALUES
(1, 1, 1),
(2, 2, NULL),
(3, 3, 3),
(4, 4, 4),
(5, 5, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `Patients`
--
DROP TABLE IF EXISTS `Patients`;
CREATE TABLE `Patients` (
  `patientID` int(11) NOT NULL,
  `ssn` varchar(9) NOT NULL,
  `dob` date NOT NULL,
  `firstName` varchar(255) NOT NULL,
  `lastName` varchar(255) NOT NULL,
  `streetAddress` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(2) NOT NULL,
  `zip` varchar(5) NOT NULL,
  `phone` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Patients`
--

INSERT INTO `Patients` (`patientID`, `ssn`, `dob`, `firstName`, `lastName`, `streetAddress`, `city`, `state`, `zip`, `phone`) VALUES
(1, '111111111', '1996-01-05', 'Jane', 'Doe', '901 E Van Buren St.', 'Phoenix', 'AZ', '85006', '111-222-1111'),
(2, '222222222', '1990-11-15', 'John', 'Smith', '1111 W Linden St.', 'Goodyear', 'AZ', '85338', '222-333-2222'),
(3, '333333333', '1964-03-17', 'Pat', 'Michel', '123 N Kesler St.', 'Goodyear', 'AZ', '85338', '333-444-3333'),
(4, '444444444', '1980-12-05', 'Austin', 'Barkley', '5555 S Park St.', 'Avondale', 'AZ', '86444', '444-555-4444'),
(5, '555555555', '1975-06-12', 'Theresa', 'Lee', '3333 Tumbleweed Rd.', 'Phoenix', 'AZ', '85006', '555-666-5555');

-- --------------------------------------------------------

--
-- Table structure for table `Physicians`
--

DROP TABLE IF EXISTS `Physicians`;
CREATE TABLE `Physicians` (
  `physicianID` int(11) NOT NULL,
  `firstName` varchar(255) NOT NULL,
  `lastName` varchar(255) NOT NULL,
  `specialty` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Physicians`
--

INSERT INTO `Physicians` (`physicianID`, `firstName`, `lastName`, `specialty`) VALUES
(1, 'Reid', 'Adams', 'Emergency'),
(2, 'Mary', 'Smith', 'Epidemiologist'),
(3, 'John', 'Cannon', 'Epidemiologist'),
(4, 'Lisa', 'Carmody', 'Gastroenterologist'),
(5, 'Blake', 'Lee', 'Emergency');

-- --------------------------------------------------------

--
-- Table structure for table `Treatments`
--

DROP TABLE IF EXISTS `Treatments`;
CREATE TABLE `Treatments` (
  `treatmentID` int(11) NOT NULL,
  `patientID` int(11) NOT NULL,
  `medicationID` int(11) NOT NULL,
  `frequency` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Treatments`
--

INSERT INTO `Treatments` (`treatmentID`, `patientID`, `medicationID`, `frequency`) VALUES
(1, 1, 1, '1Q4H'),
(2, 1, 2, 'TID'),
(3, 3, 1, '1Q4H'),
(4, 4, 3, 'QD'),
(5, 5, 5, 'TID');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Medications`
--
ALTER TABLE `Medications`
  ADD PRIMARY KEY (`medicationID`);

--
-- Indexes for table `Nurses`
--
ALTER TABLE `Nurses`
  ADD PRIMARY KEY (`nurseID`);

--
-- Indexes for table `PatientDetails`
--
ALTER TABLE `PatientDetails`
  ADD PRIMARY KEY (`patientID`),
  ADD KEY `fk_physicianID` (`physicianID`),
  ADD KEY `fk_nurseID` (`nurseID`);

--
-- Indexes for table `Patients`
--
ALTER TABLE `Patients`
  ADD PRIMARY KEY (`patientID`);

--
-- Indexes for table `Physicians`
--
ALTER TABLE `Physicians`
  ADD PRIMARY KEY (`physicianID`);

--
-- Indexes for table `Treatments`
--
ALTER TABLE `Treatments`
  ADD PRIMARY KEY (`treatmentID`),
  ADD KEY `fk_patientID_1` (`patientID`),
  ADD KEY `fk_medicationID` (`medicationID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Medications`
--
ALTER TABLE `Medications`
  MODIFY `medicationID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Nurses`
--
ALTER TABLE `Nurses`
  MODIFY `nurseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Patients`
--
ALTER TABLE `Patients`
  MODIFY `patientID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Physicians`
--
ALTER TABLE `Physicians`
  MODIFY `physicianID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Treatments`
--
ALTER TABLE `Treatments`
  MODIFY `treatmentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `PatientDetails`
--
ALTER TABLE `PatientDetails`
  ADD CONSTRAINT `fk_nurseID` FOREIGN KEY (`nurseID`) REFERENCES `Nurses` (`nurseID`),
  ADD CONSTRAINT `fk_patientID` FOREIGN KEY (`patientID`) REFERENCES `Patients` (`patientID`),
  ADD CONSTRAINT `fk_physicianID` FOREIGN KEY (`physicianID`) REFERENCES `Physicians` (`physicianID`);

--
-- Constraints for table `Treatments`
--
ALTER TABLE `Treatments`
  ADD CONSTRAINT `fk_medicationID` FOREIGN KEY (`medicationID`) REFERENCES `Medications` (`medicationID`),
  ADD CONSTRAINT `fk_patientID_1` FOREIGN KEY (`patientID`) REFERENCES `Patients` (`patientID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
