CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

-- ==========================
-- PATIENTS TABLE
-- ==========================
DROP TABLE IF EXISTS TreatmentSessions;
DROP TABLE IF EXISTS Treatments;
DROP TABLE IF EXISTS Doctors;
DROP TABLE IF EXISTS Patients;

CREATE TABLE Patients (
    PatientID INT AUTO_INCREMENT PRIMARY KEY,
    PatientName VARCHAR(100) NOT NULL,
    BirthDate DATE NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL,
    Phone VARCHAR(15),
    Address VARCHAR(255)
);

-- ==========================
-- DOCTORS TABLE
-- ==========================
CREATE TABLE Doctors (
    DoctorID INT AUTO_INCREMENT PRIMARY KEY,
    DoctorName VARCHAR(100) NOT NULL,
    Specialty VARCHAR(100) NOT NULL
);

-- ==========================
-- TREATMENTS TABLE
-- ==========================
CREATE TABLE Treatments (
    TreatmentID INT AUTO_INCREMENT PRIMARY KEY,
    TreatmentName VARCHAR(100) NOT NULL,
    StandardCost INT NOT NULL
);

-- ==========================
-- TREATMENT SESSIONS
-- ==========================
CREATE TABLE TreatmentSessions (
    SessionID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT NOT NULL,
    TreatmentID INT NOT NULL,
    DoctorID INT NOT NULL,
    TreatmentDate DATE NOT NULL,

    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (TreatmentID) REFERENCES Treatments(TreatmentID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
        ON DELETE CASCADE ON UPDATE CASCADE
);
