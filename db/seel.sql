USE hospital;

-- INSERT PATIENTS (50 bệnh nhân)

INSERT INTO Patients (PatientName, BirthDate, Gender, Phone, Address) VALUES
('Nguyen Van A', '1989-02-10', 'Male', '0911111111', 'Hanoi'),
('Tran Thi B', '1992-07-20', 'Female', '0922222222', 'Hanoi'),
('Le Van C', '1985-03-15', 'Male', '0933333333', 'HCM'),
('Pham Thi D', '1990-11-22', 'Female', '0944444444', 'Danang'),
('Hoang Van E', '2001-05-14', 'Male', '0955555555', 'Hue'),
('Ngo Thi F', '1999-10-01', 'Female', '0966666666', 'Hanoi'),
('Phan Van G', '1978-01-19', 'Male', '0977777777', 'HCM'),
('Bui Thi H', '1982-04-07', 'Female', '0988888888', 'Haiphong'),
('Vo Van I', '1995-12-12', 'Male', '0999999999', 'Danang'),
('Dang Thi J', '1998-09-17', 'Female', '0900000001', 'Hanoi'),

('Nguyen Van K', '1983-09-23', 'Male', '0900000002', 'Hanoi'),
('Tran Thi L', '1991-04-04', 'Female', '0900000003', 'HCM'),
('Le Van M', '1997-08-09', 'Male', '0900000004', 'Danang'),
('Pham Thi N', '1980-11-18', 'Female', '0900000005', 'Hue'),
('Hoang Van O', '1979-06-26', 'Male', '0900000006', 'Hanoi'),
('Ngo Thi P', '1987-05-05', 'Female', '0900000007', 'Haiphong'),
('Phan Van Q', '1996-03-29', 'Male', '0900000008', 'HCM'),
('Bui Thi R', '1994-10-21', 'Female', '0900000009', 'Hanoi'),
('Vo Van S', '2000-01-01', 'Male', '0900000010', 'Danang'),
('Dang Thi T', '1993-02-16', 'Female', '0900000011', 'Hue'),

('Patient 21', '1984-06-10', 'Male', '0900000012', 'Hanoi'),
('Patient 22', '1985-06-11', 'Female', '0900000013', 'Hanoi'),
('Patient 23', '1986-06-12', 'Male', '0900000014', 'HCM'),
('Patient 24', '1987-06-13', 'Female', '0900000015', 'Danang'),
('Patient 25', '1988-06-14', 'Male', '0900000016', 'Hue'),
('Patient 26', '1989-06-15', 'Female', '0900000017', 'Hanoi'),
('Patient 27', '1990-06-16', 'Male', '0900000018', 'HCM'),
('Patient 28', '1991-06-17', 'Female', '0900000019', 'Haiphong'),
('Patient 29', '1992-06-18', 'Male', '0900000020', 'Danang'),
('Patient 30', '1993-06-19', 'Female', '0900000021', 'Hue'),

('Patient 31', '1980-01-10', 'Male', '0900000022', 'Hanoi'),
('Patient 32', '1981-02-11', 'Female', '0900000023', 'Hanoi'),
('Patient 33', '1982-03-12', 'Male', '0900000024', 'HCM'),
('Patient 34', '1983-04-13', 'Female', '0900000025', 'Danang'),
('Patient 35', '1984-05-14', 'Male', '0900000026', 'Hue'),
('Patient 36', '1985-06-15', 'Female', '0900000027', 'Hanoi'),
('Patient 37', '1986-07-16', 'Male', '0900000028', 'HCM'),
('Patient 38', '1987-08-17', 'Female', '0900000029', 'Haiphong'),
('Patient 39', '1988-09-18', 'Male', '0900000030', 'Danang'),
('Patient 40', '1989-10-19', 'Female', '0900000031', 'Hue'),

('Patient 41', '1990-11-10', 'Male', '0900000032', 'Hanoi'),
('Patient 42', '1991-12-11', 'Female', '0900000033', 'Hanoi'),
('Patient 43', '1992-01-12', 'Male', '0900000034', 'HCM'),
('Patient 44', '1993-02-13', 'Female', '0900000035', 'Danang'),
('Patient 45', '1994-03-14', 'Male', '0900000036', 'Hue'),
('Patient 46', '1995-04-15', 'Female', '0900000037', 'Hanoi'),
('Patient 47', '1996-05-16', 'Male', '0900000038', 'HCM'),
('Patient 48', '1997-06-17', 'Female', '0900000039', 'Haiphong'),
('Patient 49', '1998-07-18', 'Male', '0900000040', 'Danang'),
('Patient 50', '1999-08-19', 'Female', '0900000041', 'Hue');

-- INSERT DOCTORS (10 bác sĩ)

INSERT INTO Doctors (DoctorName, Specialty) VALUES
('Dr. Minh', 'Cardiology'),
('Dr. Hoa', 'Neurology'),
('Dr. Truong', 'Oncology'),
('Dr. Hanh', 'Dermatology'),
('Dr. Duc', 'Orthopedic'),
('Dr. Quynh', 'Pediatrics'),
('Dr. Phong', 'General Medicine'),
('Dr. Loc', 'Radiology'),
('Dr. Tuan', 'Urology'),
('Dr. Nhan', 'Gastroenterology');

-- INSERT TREATMENTS (12 phương pháp điều trị)

INSERT INTO Treatments (TreatmentName, StandardCost) VALUES
('Heart Checkup', 500000),
('MRI Scan', 1200000),
('Chemotherapy', 2500000),
('Skin Treatment', 800000),
('Bone X-Ray', 350000),
('Blood Test', 150000),
('Ultrasound', 450000),
('CT Scan', 1500000),
('Kidney Dialysis', 2200000),
('Endoscopy', 1100000),
('Physiotherapy', 300000),
('Vaccination', 200000);

-- INSERT TREATMENT SESSIONS (60 buổi điều trị)

INSERT INTO TreatmentSessions (PatientID, TreatmentID, DoctorID, TreatmentDate) VALUES
(1, 1, 1, '2024-01-05'),
(2, 2, 2, '2024-01-06'),
(3, 3, 3, '2024-01-07'),
(4, 4, 4, '2024-01-08'),
(5, 5, 5, '2024-01-09'),
(6, 6, 6, '2024-01-10'),
(7, 7, 7, '2024-01-11'),
(8, 8, 8, '2024-01-12'),
(9, 9, 9, '2024-01-13'),
(10, 10, 10, '2024-01-14'),

(11, 11, 1, '2024-02-01'),
(12, 12, 2, '2024-02-02'),
(13, 1, 3, '2024-02-03'),
(14, 2, 4, '2024-02-04'),
(15, 3, 5, '2024-02-05'),
(16, 4, 6, '2024-02-06'),
(17, 5, 7, '2024-02-07'),
(18, 6, 8, '2024-02-08'),
(19, 7, 9, '2024-02-09'),
(20, 8, 10, '2024-02-10'),

(21, 9, 1, '2024-03-01'),
(22, 10, 2, '2024-03-02'),
(23, 11, 3, '2024-03-03'),
(24, 12, 4, '2024-03-04'),
(25, 1, 5, '2024-03-05'),
(26, 2, 6, '2024-03-06'),
(27, 3, 7, '2024-03-07'),
(28, 4, 8, '2024-03-08'),
(29, 5, 9, '2024-03-09'),
(30, 6, 10, '2024-03-10'),

(31, 7, 1, '2024-04-01'),
(32, 8, 2, '2024-04-02'),
(33, 9, 3, '2024-04-03'),
(34, 10, 4, '2024-04-04'),
(35, 11, 5, '2024-04-05'),
(36, 12, 6, '2024-04-06'),
(37, 1, 7, '2024-04-07'),
(38, 2, 8, '2024-04-08'),
(39, 3, 9, '2024-04-09'),
(40, 4, 10, '2024-04-10'),

(41, 5, 1, '2024-05-01'),
(42, 6, 2, '2024-05-02'),
(43, 7, 3, '2024-05-03'),
(44, 8, 4, '2024-05-04'),
(45, 9, 5, '2024-05-05'),
(46, 10, 6, '2024-05-06'),
(47, 11, 7, '2024-05-07'),
(48, 12, 8, '2024-05-08'),
(49, 1, 9, '2024-05-09'),
(50, 2, 10, '2024-05-10');
