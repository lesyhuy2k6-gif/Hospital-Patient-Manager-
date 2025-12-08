-- =====================================================
-- Hospital Management System - Database Schema
-- =====================================================
-- This file contains only table definitions.
-- For sample data, see seel.sql
-- =====================================================

-- 1. Drop the database if it exists (for fresh setup)
DROP DATABASE IF EXISTS hospital;

-- 2. Create the database
CREATE DATABASE hospital;

-- 3. Use the newly created database
USE hospital;

-- 4. Create the DOCTORS table
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100),
    phone VARCHAR(20),
    gender ENUM('Male', 'Female', 'Other')
);

-- 5. Create the PATIENTS table
CREATE TABLE patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    birthdate DATE,
    phone VARCHAR(20),
    gender ENUM('Male', 'Female', 'Other')
);

-- 6. Create the TREATMENTS table
CREATE TABLE treatments (
    treatment_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    cost DECIMAL(10,2) DEFAULT 0.00
);

-- 7. Create the SESSIONS table (The core table linking the others)
-- Note: The foreign key definitions here match the Python application's logic (ON DELETE SET NULL)
CREATE TABLE sessions (
    session_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    doctor_id INT,
    treatment_id INT,
    treatment_date DATE NOT NULL,

    -- Foreign Keys with cascade options for integrity
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
