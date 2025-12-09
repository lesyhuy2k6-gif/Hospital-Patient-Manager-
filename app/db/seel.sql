-- =====================================================
-- Hospital Management System - GENERATED SAMPLE DATA (ASCII Names)
-- =====================================================
-- This file contains INSERT statements with patient names
-- converted to standard ASCII (no Vietnamese tones/diacritics).
-- Assumes tables: doctors, patients, treatments, sessions
-- =====================================================

USE hospital;

-- =====================================================
-- INSERT DOCTORS (12 Doctors)
-- =====================================================
-- No change here, keeping the English names and simple Vietnamese names.

INSERT INTO doctors (name, specialty, phone, gender) VALUES
('Dr. Alistair Finch', 'Cardiology', '0911111111', 'Male'),
('Dr. Evelyn Reed', 'Pediatrics', '0922222222', 'Female'),
('Dr. Marcus Cole', 'Orthopedics', '0933333333', 'Male'),
('Dr. Sofia Perez', 'General Practice', '0944444444', 'Female'),
('Dr. Minh', 'Cardiology', '0955555555', 'Male'),
('Dr. Hoa', 'Neurology', '0966666666', 'Female'),
('Dr. Truong', 'Oncology', '0977777777', 'Male'),
('Dr. Hanh', 'Dermatology', '0988888888', 'Female'),
('Dr. Duc', 'Orthopedics', '0999999999', 'Male'),
('Dr. Quynh', 'Pediatrics', '0900000010', 'Female'),
('Dr. Viet Anh', 'Internal Medicine', '0900000011', 'Male'),
('Dr. Mai Lan', 'Psychiatry', '0900000012', 'Female');

-- =====================================================
-- INSERT PATIENTS (50 Patients - Non-Diacritical Vietnamese Names)
-- =====================================================

INSERT INTO patients (name, birthdate, phone, gender) VALUES
('Nguyen Van An', '1985-04-12', '0911111111', 'Male'),
('Tran Thi Binh', '1998-11-20', '0922222222', 'Female'),
('Le Hoang Trung', '1955-01-01', '0933333333', 'Male'),
('Pham Thi Mai', '1989-02-10', '0944444444', 'Female'),
('Do Van Hung', '1992-07-20', '0955555555', 'Male'),
('Hoang Thi Lan', '1985-03-15', '0966666666', 'Female'),
('Vu Minh Duc', '1990-11-22', '0977777777', 'Male'),
('Ngo Thanh Thuy', '2001-05-14', '0988888888', 'Female'),
('Bui Van Cong', '1999-10-01', '0999999999', 'Male'),
('Duong Thi Huong', '1978-01-19', '0900000010', 'Female'),
('Phan Dinh Thai', '1982-04-07', '0900000011', 'Male'),
('Ho Thi Yen', '1995-12-12', '0900000012', 'Female'),
('Cao Van Loi', '1998-09-17', '0900000013', 'Male'),
('Dang Thi Kim', '1983-09-23', '0900000014', 'Female'),
('Nguyen Tien Dat', '1991-04-04', '0900000015', 'Male'),
('Tran Van Son', '1997-08-09', '0900000016', 'Male'),
('Ly Thi Anh', '1980-11-18', '0900000017', 'Female'),
('Vuong Minh Khoi', '1979-06-26', '0900000018', 'Male'),
('Hoang Van Long', '1987-05-05', '0900000019', 'Male'),
('Dao Thi Ngoc', '1996-03-29', '0900000020', 'Female'),
('Lam Van Hieu', '1984-06-10', '0900000021', 'Male'),
('Nguyen Thi Thu', '1985-06-11', '0900000022', 'Female'),
('Bui Minh Cuong', '1986-06-12', '0900000023', 'Male'),
('Tran Anh Thu', '1987-06-13', '0900000024', 'Female'),
('Pham Van Kien', '1988-06-14', '0900000025', 'Male'),
('Ho Thi Van', '1989-06-15', '0900000026', 'Female'),
('Vo Van Phuoc', '1990-06-16', '0900000027', 'Male'),
('Dinh Thi Tuyet', '1991-06-17', '0900000028', 'Female'),
('Le Van Tai', '1992-06-18', '0900000029', 'Male'),
('Nguyen Thuy Linh', '1993-06-19', '0900000030', 'Female'),
('Cao Minh Nhat', '1981-01-20', '0900000031', 'Male'),
('Vu Thi Mai Anh', '1994-10-21', '0900000032', 'Female'),
('Phan Van Nam', '1976-02-22', '0900000033', 'Male'),
('Tran Thi Hai', '1986-12-23', '0900000034', 'Female'),
('Do Minh Tuan', '1995-07-24', '0900000035', 'Male'),
('Le Thi Hong', '1988-03-25', '0900000036', 'Female'),
('Hoang Van Dung', '1975-09-26', '0900000037', 'Male'),
('Nguyen Thi Quynh', '1990-05-27', '0900000038', 'Female'),
('Bui Van Hoa', '1999-08-28', '0900000039', 'Male'),
('Duong Thi Thao', '1982-11-29', '0900000040', 'Female'),
('Phan Minh Quang', '1977-04-30', '0900000041', 'Male'),
('Ho Van Viet', '1993-01-01', '0900000042', 'Male'),
('Cao Thi Ngan', '1980-02-02', '0900000043', 'Female'),
('Vu Van Hau', '1996-03-03', '0900000044', 'Male'),
('Dang Minh Tri', '1984-04-04', '0900000045', 'Male'),
('Le Thi Thanh', '1997-05-05', '0900000046', 'Female'),
('Tran Van Khang', '1983-06-06', '0900000047', 'Male'),
('Pham Thi Nhung', '1999-07-07', '0900000048', 'Female'),
('Nguyen Van Thanh', '1979-08-08', '0900000049', 'Male'),
('Do Thi Thu Ha', '1985-09-09', '0900000050', 'Female');

-- =====================================================
-- INSERT TREATMENTS (15 Treatments)
-- =====================================================
-- No change here, using the expanded list of 15 treatments.

INSERT INTO treatments (name, cost) VALUES
('Initial Consultation', 150.00),
('X-Ray Scan', 75.50),
('Physical Therapy', 90.00),
('Echocardiogram', 320.00),
('MRI Scan', 1200.00),
('Chemotherapy', 2500.00),
('Skin Treatment', 800.00),
('Blood Test', 150.00),
('Ultrasound', 450.00),
('CT Scan', 1500.00),
('Physiotherapy', 300.00),
('Vaccination', 200.00),
('Stress Test', 250.00),
('Minor Surgery', 3500.00),
('Psychological Assessment', 500.00);

-- =====================================================
-- INSERT SESSIONS (75 Treatment Sessions)
-- =====================================================
-- Session data uses Patient IDs 1-50, Doctor IDs 1-12, and Treatment IDs 1-15.

INSERT INTO sessions (patient_id, doctor_id, treatment_id, treatment_date) VALUES
-- October 2024
(1, 4, 1, '2024-10-01'),
(1, 1, 4, '2024-10-15'),
(2, 2, 1, '2024-11-05'),
(3, 3, 2, '2024-11-10'),
(4, 1, 13, '2024-10-25'),
(5, 5, 1, '2024-10-02'),
(6, 6, 8, '2024-10-03'),
(7, 7, 6, '2024-10-04'),
(8, 8, 7, '2024-10-05'),
(9, 9, 3, '2024-10-06'),
(10, 10, 12, '2024-10-07'),

-- November 2024
(11, 11, 15, '2024-11-01'),
(12, 12, 1, '2024-11-02'),
(13, 1, 4, '2024-11-03'),
(14, 2, 12, '2024-11-04'),
(15, 3, 10, '2024-11-05'),
(16, 4, 2, '2024-11-06'),
(17, 5, 13, '2024-11-07'),
(18, 6, 9, '2024-11-08'),
(19, 7, 6, '2024-11-09'),
(20, 8, 7, '2024-11-10'),

-- December 2024
(21, 9, 3, '2024-12-01'),
(22, 10, 11, '2024-12-02'),
(23, 11, 1, '2024-12-03'),
(24, 12, 15, '2024-12-04'),
(25, 1, 4, '2024-12-05'),
(26, 2, 12, '2024-12-06'),
(27, 3, 10, '2024-12-07'),
(28, 4, 8, '2024-12-08'),
(29, 5, 5, '2024-12-09'),
(30, 6, 9, '2024-12-10'),
(31, 7, 6, '2024-12-11'),
(32, 8, 7, '2024-12-12'),

-- January 2025
(33, 9, 14, '2025-01-01'),
(34, 10, 11, '2025-01-02'),
(35, 11, 1, '2025-01-03'),
(36, 12, 15, '2025-01-04'),
(37, 1, 4, '2025-01-05'),
(38, 2, 12, '2025-01-06'),
(39, 3, 10, '2025-01-07'),
(40, 4, 8, '2025-01-08'),
(41, 5, 5, '2025-01-09'),
(42, 6, 9, '2025-01-10'),
(43, 7, 6, '2025-01-11'),
(44, 8, 7, '2025-01-12'),
(45, 9, 3, '2025-01-13'),
(46, 10, 11, '2025-01-14'),
(47, 11, 1, '2025-01-15'),
(48, 12, 15, '2025-01-16'),

-- February 2025 (Additional Sessions and follow-ups)
(49, 1, 13, '2025-02-01'),
(50, 2, 12, '2025-02-02'),
(1, 3, 10, '2025-02-03'),
(2, 4, 8, '2025-02-04'),
(3, 5, 5, '2025-02-05'),
(4, 6, 9, '2025-02-06'),
(5, 7, 1, '2025-02-07'),
(6, 8, 7, '2025-02-08'),
(7, 9, 3, '2025-02-09'),
(8, 10, 11, '2025-02-10'),
(9, 11, 14, '2025-02-11'),
(10, 12, 1, '2025-02-12'),
(11, 1, 4, '2025-02-13'),
(12, 2, 12, '2025-02-14'),
(13, 3, 10, '2025-02-15'),
(14, 4, 8, '2025-02-16'),
(15, 5, 5, '2025-02-17'),
(16, 6, 9, '2025-02-18'),
(17, 7, 6, '2025-02-19'),
(18, 8, 7, '2025-02-20'),
(19, 9, 3, '2025-02-21'),
(20, 10, 11, '2025-02-22'),
(21, 11, 1, '2025-02-23'),

-- Final Session to reach 75
(22, 12, 15, '2025-02-24');

-- =====================================================