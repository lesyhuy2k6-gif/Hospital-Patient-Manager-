# Hospital Management System

A Python-based hospital management application with a tkinter GUI for managing patients, doctors, treatments, and sessions. Includes global search, advanced reports, and a KPI dashboard.

## Features

- **Patient Management**: Add, update, delete patients with birthdates
- **Doctor Management**: Track doctors and their specialties
- **Treatment Management**: Manage treatment names and costs
- **Session Tracking**: Record patient-doctor-treatment sessions with dates
- **Global Search**: Search across all entities (patients, doctors, treatments) by name
- **Advanced Reports**: 
  - Inner join (sessions with patient/treatment details)
  - Left join (all patients with/without sessions)
  - Multi-table join (sessions with patient, doctor, treatment)
  - High-cost treatment analysis
  - Export reports to CSV
- **Dashboard**: 
  - Key Performance Indicators (Total Patients, Doctors, Sessions, Avg Treatment Cost, High-Cost Treatments)
  - Treatment cost distribution histogram
  - Export KPIs to CSV

## Installation & Setup

### Prerequisites
- Python 3.x (tested on Python 3.14+)
- MySQL server running locally (default: localhost, user: root, password: 1234)
- Required Python packages:
  ```
  pymysql
  matplotlib (optional, for charts)
  ```

### Install Dependencies
```bash
pip install pymysql matplotlib
```

### Database
The application automatically creates the required tables on first run:
- `patients` (patient_id, name, birthdate)
- `doctors` (doctor_id, name, specialty)
- `treatments` (treatment_id, name, cost)
- `sessions` (session_id, patient_id, doctor_id, treatment_id, treatment_date)

### Database Configuration
Edit `connection.py` if your MySQL settings differ from:
- Host: `localhost`
- User: `root`
- Password: `1234`
- Database: `hospital`

## Running the Application

### Method 1: Double-Click (Windows)
Double-click `run_app.bat` in the project folder.

### Method 2: Command Line
```bash
cd c:\Users\Duong\.vscode\python\test_app
python main.py
```

### Method 3: Python Terminal
```bash
python -c "from main import *; run_app()"
```

## Project Structure

```
test_app/
├── main.py              # Application entry point
├── ui.py                # Main UI with all tabs (Patients, Doctors, Treatments, Sessions, Global Search, Reports, Dashboard)
├── dashboard.py         # Dashboard tab (KPIs and cost distribution chart)
├── queries.py           # SQL query constants
├── services.py          # Database utilities and CRUD operations
├── connection.py        # Database connection helper
├── run_app.bat          # Quick launcher (Windows)
├── db_check.py          # Diagnostic script (check row counts)
├── run_queries.py       # Debug script (inspect raw query outputs)
├── test_format_checks.py # Test script (verify Global Search and Reports formatting)
└── README.md            # This file
```

## Tabs Overview

1. **Patients**: CRUD operations for patient records
2. **Doctors**: CRUD operations for doctor records
3. **Treatments**: CRUD operations for treatment records
4. **Sessions**: Create sessions linking patients, doctors, and treatments
5. **Global Search**: Search all entities by name keyword
6. **Reports**: Execute and export advanced SQL reports
7. **Dashboard**: View KPIs and treatment cost distribution chart

## Troubleshooting

### Database Connection Error
- Ensure MySQL server is running: `mysql -u root -p`
- Verify credentials in `connection.py`
- Check that the `hospital` database exists or allow the app to create it

### No Data in Global Search or Dashboard
- Check `db_check.py` output to confirm tables have data
- Run `python db_check.py` to see row counts

### Chart Not Displaying
- Ensure matplotlib is installed: `pip install matplotlib`
- If matplotlib is not available, the chart will show a message but the app will still function

### Cannot Run `run_app.bat`
- Right-click and select "Run as Administrator" if permission denied
- Or run from command line: `cd c:\Users\Duong\.vscode\python\test_app && python main.py`

## Development Notes

- **Database Cursor**: Uses `DictCursor` for consistent dict-based row access
- **Date Handling**: All dates are stored and displayed in `YYYY-MM-DD` format
- **Cost Values**: Stored as MySQL DECIMAL for accuracy
- **Temporary Files**: `db_check.py`, `run_queries.py`, and `test_format_checks.py` are diagnostic scripts and can be deleted if not needed

## Future Enhancements

- Add user authentication
- Implement appointment scheduling
- Add treatment outcome tracking
- Integrate email notifications
- Web interface (Flask/Django)
