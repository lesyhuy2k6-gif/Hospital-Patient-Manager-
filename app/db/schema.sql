use hospital;

INSERT INTO treatments (treatment_id, name, cost) VALUES
(5, 'Annual Check-up', 180.00),
(6, 'Blood Test Panel', 45.00),
(7, 'Flu Vaccination', 30.00),
(8, 'Minor Surgery', 550.00),
(9, 'MRI Scan', 600.00),
(10, 'Dental Cleaning', 120.00),
(11, 'Psychological Evaluation', 250.00),
(12, 'Medication Review', 50.00),
(13, 'Suture Removal', 40.00),
(14, 'Allergy Test', 110.00),
(15, 'Joint Injection', 195.00);
INSERT INTO doctors (doctor_id, name, specialty) VALUES
(5, 'Dr. Ben Carter', 'Dermatology'),
(6, 'Dr. Chloe Davis', 'Neurology'),
(7, 'Dr. Daniel Evans', 'Gastroenterology'),
(8, 'Dr. Fiona Green', 'Oncology'),
(9, 'Dr. George Harris', 'Urology'),
(10, 'Dr. Hannah Ibsen', 'Endocrinology'),
(11, 'Dr. Ivan Jones', 'Pulmonology'),
(12, 'Dr. Jasmine King', 'Psychiatry');
-- Disable safe updates for the following loop/inserts if you run into issues
-- SET SQL_SAFE_UPDATES = 0; 

-- This script uses a simple iterative method (UNION ALL) to generate 46 more sessions.
-- The number of sessions can be increased by duplicating a block or using a stored procedure/loop.
-- We use a date range of the last 180 days for the treatment_date.
-- MAX_PATIENT_ID = 50, MAX_DOCTOR_ID = 12, MAX_TREATMENT_ID = 15

INSERT INTO sessions (patient_id, doctor_id, treatment_id, treatment_date)
SELECT
    FLOOR(1 + (RAND() * 50)) AS patient_id,     -- Random ID between 1 and 50
    FLOOR(1 + (RAND() * 12)) AS doctor_id,      -- Random ID between 1 and 12
    FLOOR(1 + (RAND() * 15)) AS treatment_id,   -- Random ID between 1 and 15
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 180) DAY) AS treatment_date -- Random date in the last 180 days
FROM
    -- A simple way to generate 46 rows using UNION ALL
    (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10) AS a,
    (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) AS b
LIMIT 46;