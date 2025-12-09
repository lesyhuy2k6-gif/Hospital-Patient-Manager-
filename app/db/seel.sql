-- =====================================================
-- Hospital Management System - GENERATED SAMPLE DATA
-- =====================================================
-- This file contains INSERT statements for new sample data.
-- Assumes tables: doctors, patients, treatments, sessions
-- =====================================================

USE hospital;

-- Clean existing data to avoid conflicts, if you are re-running this on the same database
-- DELETE FROM sessions;
-- DELETE FROM patients;
-- DELETE FROM doctors;
-- DELETE FROM treatments;

-- =====================================================
-- INSERT DOCTORS (12 Doctors)
-- =====================================================

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
-- INSERT PATIENTS (50 Patients with Vietnamese Names)
-- =====================================================

INSERT INTO patients (name, birthdate, phone, gender) VALUES
('Nguyễn Văn An', '1985-04-12', '0911111111', 'Male'),
('Trần Thị Bình', '1998-11-20', '0922222222', 'Female'),
('Lê Hoàng Trung', '1955-01-01', '0933333333', 'Male'),
('Phạm Thị Mai', '1989-02-10', '0944444444', 'Female'),
('Đỗ Văn Hùng', '1992-07-20', '0955555555', 'Male'),
('Hoàng Thị Lan', '1985-03-15', '0966666666', 'Female'),
('Vũ Minh Đức', '1990-11-22', '0977777777', 'Male'),
('Ngô Thanh Thủy', '2001-05-14', '0988888888', 'Female'),
('Bùi Văn Công', '1999-10-01', '0999999999', 'Male'),
('Dương Thị Hương', '1978-01-19', '0900000010', 'Female'),
('Phan Đình Thái', '1982-04-07', '0900000011', 'Male'),
('Hồ Thị Yến', '1995-12-12', '0900000012', 'Female'),
('Cao Văn Lợi', '1998-09-17', '0900000013', 'Male'),
('Đặng Thị Kim', '1983-09-23', '0900000014', 'Female'),
('Nguyễn Tiến Đạt', '1991-04-04', '0900000015', 'Male'),
('Trần Văn Sơn', '1997-08-09', '0900000016', 'Male'),
('Lý Thị Ánh', '1980-11-18', '0900000017', 'Female'),
('Vương Minh Khôi', '1979-06-26', '0900000018', 'Male'),
('Hoàng Văn Long', '1987-05-05', '0900000019', 'Male'),
('Đào Thị Ngọc', '1996-03-29', '0900000020', 'Female'),
('Lâm Văn Hiếu', '1984-06-10', '0900000021', 'Male'),
('Nguyễn Thị Thu', '1985-06-11', '0900000022', 'Female'),
('Bùi Minh Cường', '1986-06-12', '0900000023', 'Male'),
('Trần Anh Thư', '1987-06-13', '0900000024', 'Female'),
('Phạm Văn Kiên', '1988-06-14', '0900000025', 'Male'),
('Hồ Thị Vân', '1989-06-15', '0900000026', 'Female'),
('Võ Văn Phước', '1990-06-16', '0900000027', 'Male'),
('Đinh Thị Tuyết', '1991-06-17', '0900000028', 'Female'),
('Lê Văn Tài', '1992-06-18', '0900000029', 'Male'),
('Nguyễn Thùy Linh', '1993-06-19', '0900000030', 'Female'),
('Cao Minh Nhật', '1981-01-20', '0900000031', 'Male'),
('Vũ Thị Mai Anh', '1994-10-21', '0900000032', 'Female'),
('Phan Văn Nam', '1976-02-22', '0900000033', 'Male'),
('Trần Thị Hải', '1986-12-23', '0900000034', 'Female'),
('Đỗ Minh Tuấn', '1995-07-24', '0900000035', 'Male'),
('Lê Thị Hồng', '1988-03-25', '0900000036', 'Female'),
('Hoàng Văn Dũng', '1975-09-26', '0900000037', 'Male'),
('Nguyễn Thị Quỳnh', '1990-05-27', '0900000038', 'Female'),
('Bùi Văn Hòa', '1999-08-28', '0900000039', 'Male'),
('Dương Thị Thảo', '1982-11-29', '0900000040', 'Female'),
('Phan Minh Quang', '1977-04-30', '0900000041', 'Male'),
('Hồ Văn Việt', '1993-01-01', '0900000042', 'Male'),
('Cao Thị Ngân', '1980-02-02', '0900000043', 'Female'),
('Vũ Văn Hậu', '1996-03-03', '0900000044', 'Male'),
('Đặng Minh Trí', '1984-04-04', '0900000045', 'Male'),
('Lê Thị Thanh', '1997-05-05', '0900000046', 'Female'),
('Trần Văn Khang', '1983-06-06', '0900000047', 'Male'),
('Phạm Thị Nhung', '1999-07-07', '0900000048', 'Female'),
('Nguyễn Văn Thành', '1979-08-08', '0900000049', 'Male'),
('Đỗ Thị Thu Hà', '1985-09-09', '0900000050', 'Female');

-- =====================================================
-- INSERT TREATMENTS (15 Treatments)
-- =====================================================

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
('Stress Test', 250.00),          -- New
('Minor Surgery', 3500.00),      -- New
('Psychological Assessment', 500.00); -- New

-- =====================================================
-- INSERT SESSIONS (75 Treatment Sessions)
-- =====================================================
-- Using a mix of dates for better coverage (Late 2024 to early 2025)

INSERT INTO sessions (patient_id, doctor_id, treatment_id, treatment_date) VALUES
-- October 2024 (Cardiology, Pediatrics, Orthopedics, General Practice)
(1, 4, 1, '2024-10-01'), -- Nguyễn Văn An - Consultation
(1, 1, 4, '2024-10-15'), -- Nguyễn Văn An - Echocardiogram
(2, 2, 1, '2024-11-05'), -- Trần Thị Bình - Consultation
(3, 3, 2, '2024-11-10'), -- Lê Hoàng Trung - X-Ray
(4, 1, 13, '2024-10-25'),-- Phạm Thị Mai - Stress Test
(5, 5, 1, '2024-10-02'), -- Đỗ Văn Hùng - Consultation
(6, 6, 8, '2024-10-03'), -- Hoàng Thị Lan - Blood Test
(7, 7, 6, '2024-10-04'), -- Vũ Minh Đức - Chemotherapy
(8, 8, 7, '2024-10-05'), -- Ngô Thanh Thủy - Skin Treatment
(9, 9, 3, '2024-10-06'), -- Bùi Văn Công - Physical Therapy
(10, 10, 12, '2024-10-07'),-- Dương Thị Hương - Vaccination

-- November 2024 (Mix of Specialties)
(11, 11, 15, '2024-11-01'),-- Phan Đình Thái - Psychological Assessment
(12, 12, 1, '2024-11-02'),-- Hồ Thị Yến - Consultation
(13, 1, 4, '2024-11-03'), -- Cao Văn Lợi - Echocardiogram
(14, 2, 12, '2024-11-04'),-- Đặng Thị Kim - Vaccination
(15, 3, 10, '2024-11-05'),-- Nguyễn Tiến Đạt - CT Scan
(16, 4, 2, '2024-11-06'), -- Trần Văn Sơn - X-Ray
(17, 5, 13, '2024-11-07'),-- Lý Thị Ánh - Stress Test
(18, 6, 9, '2024-11-08'),-- Vương Minh Khôi - Ultrasound
(19, 7, 6, '2024-11-09'),-- Hoàng Văn Long - Chemotherapy
(20, 8, 7, '2024-11-10'),-- Đào Thị Ngọc - Skin Treatment

-- December 2024 (Mix of Specialties)
(21, 9, 3, '2024-12-01'),-- Lâm Văn Hiếu - Physical Therapy
(22, 10, 11, '2024-12-02'),-- Nguyễn Thị Thu - Physiotherapy
(23, 11, 1, '2024-12-03'),-- Bùi Minh Cường - Consultation
(24, 12, 15, '2024-12-04'),-- Trần Anh Thư - Psychological Assessment
(25, 1, 4, '2024-12-05'), -- Phạm Văn Kiên - Echocardiogram
(26, 2, 12, '2024-12-06'),-- Hồ Thị Vân - Vaccination
(27, 3, 10, '2024-12-07'),-- Võ Văn Phước - CT Scan
(28, 4, 8, '2024-12-08'),-- Đinh Thị Tuyết - Blood Test
(29, 5, 5, '2024-12-09'),-- Lê Văn Tài - MRI Scan
(30, 6, 9, '2024-12-10'),-- Nguyễn Thùy Linh - Ultrasound
(31, 7, 6, '2024-12-11'),-- Cao Minh Nhật - Chemotherapy
(32, 8, 7, '2024-12-12'),-- Vũ Thị Mai Anh - Skin Treatment

-- January 2025 (Mix of Specialties, incl. Minor Surgery)
(33, 9, 14, '2025-01-01'),-- Phan Văn Nam - Minor Surgery
(34, 10, 11, '2025-01-02'),-- Trần Thị Hải - Physiotherapy
(35, 11, 1, '2025-01-03'),-- Đỗ Minh Tuấn - Consultation
(36, 12, 15, '2025-01-04'),-- Lê Thị Hồng - Psychological Assessment
(37, 1, 4, '2025-01-05'), -- Hoàng Văn Dũng - Echocardiogram
(38, 2, 12, '2025-01-06'),-- Nguyễn Thị Quỳnh - Vaccination
(39, 3, 10, '2025-01-07'),-- Bùi Văn Hòa - CT Scan
(40, 4, 8, '2025-01-08'),-- Dương Thị Thảo - Blood Test
(41, 5, 5, '2025-01-09'),-- Phan Minh Quang - MRI Scan
(42, 6, 9, '2025-01-10'),-- Hồ Văn Việt - Ultrasound
(43, 7, 6, '2025-01-11'),-- Cao Thị Ngân - Chemotherapy
(44, 8, 7, '2025-01-12'),-- Vũ Văn Hậu - Skin Treatment
(45, 9, 3, '2025-01-13'),-- Đặng Minh Trí - Physical Therapy
(46, 10, 11, '2025-01-14'),-- Lê Thị Thanh - Physiotherapy
(47, 11, 1, '2025-01-15'),-- Trần Văn Khang - Consultation
(48, 12, 15, '2025-01-16'),-- Phạm Thị Nhung - Psychological Assessment

-- February 2025 (Additional Sessions and follow-ups)
(49, 1, 13, '2025-02-01'),-- Nguyễn Văn Thành - Stress Test
(50, 2, 12, '2025-02-02'),-- Đỗ Thị Thu Hà - Vaccination
(1, 3, 10, '2025-02-03'), -- Nguyễn Văn An - CT Scan (Follow-up)
(2, 4, 8, '2025-02-04'), -- Trần Thị Bình - Blood Test (Follow-up)
(3, 5, 5, '2025-02-05'), -- Lê Hoàng Trung - MRI Scan
(4, 6, 9, '2025-02-06'), -- Phạm Thị Mai - Ultrasound
(5, 7, 1, '2025-02-07'), -- Đỗ Văn Hùng - Consultation (Follow-up)
(6, 8, 7, '2025-02-08'), -- Hoàng Thị Lan - Skin Treatment
(7, 9, 3, '2025-02-09'), -- Vũ Minh Đức - Physical Therapy
(8, 10, 11, '2025-02-10'),-- Ngô Thanh Thủy - Physiotherapy
(9, 11, 14, '2025-02-11'),-- Bùi Văn Công - Minor Surgery
(10, 12, 1, '2025-02-12'),-- Dương Thị Hương - Consultation
(11, 1, 4, '2025-02-13'),-- Phan Đình Thái - Echocardiogram
(12, 2, 12, '2025-02-14'),-- Hồ Thị Yến - Vaccination
(13, 3, 10, '2025-02-15'),-- Cao Văn Lợi - CT Scan
(14, 4, 8, '2025-02-16'),-- Đặng Thị Kim - Blood Test
(15, 5, 5, '2025-02-17'),-- Nguyễn Tiến Đạt - MRI Scan
(16, 6, 9, '2025-02-18'),-- Trần Văn Sơn - Ultrasound
(17, 7, 6, '2025-02-19'),-- Lý Thị Ánh - Chemotherapy
(18, 8, 7, '2025-02-20'),-- Vương Minh Khôi - Skin Treatment
(19, 9, 3, '2025-02-21'),-- Hoàng Văn Long - Physical Therapy
(20, 10, 11, '2025-02-22'),-- Đào Thị Ngọc - Physiotherapy
(21, 11, 1, '2025-02-23'),-- Lâm Văn Hiếu - Consultation

-- Final Session to reach 75
(22, 12, 15, '2025-02-24');-- Nguyễn Thị Thu - Psychological Assessment

-- =====================================================