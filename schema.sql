-- ==========================================
-- HOSPITAL PATIENT MANAGER - SCHEMA
-- ==========================================

DROP DATABASE IF EXISTS hospital;
CREATE DATABASE hospital;
USE hospital;

-- ======================
-- 1. PATIENT
-- ======================
CREATE TABLE Patients (
    PatientID INT AUTO_INCREMENT PRIMARY KEY,
    PatientName VARCHAR(100) NOT NULL,
    BirthDate DATE NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL,
    Phone VARCHAR(20),
    Address VARCHAR(255)
);

-- ======================
-- 2. DOCTORS
-- ======================
CREATE TABLE Doctors (
    DoctorID INT AUTO_INCREMENT PRIMARY KEY,
    DoctorName VARCHAR(100) NOT NULL,
    Specialty VARCHAR(100) NOT NULL
);

-- ======================
-- 3. TREATMENTS
-- ======================
CREATE TABLE Treatments (
    TreatmentID INT AUTO_INCREMENT PRIMARY KEY,
    TreatmentName VARCHAR(150) NOT NULL UNIQUE,
    StandardCost DECIMAL(10,2) NOT NULL CHECK(StandardCost > 0)
);

-- ======================
-- 4. TREATMENT SESSIONS
-- {PatientID, TreatmentID} → TreatmentDate
-- ======================
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