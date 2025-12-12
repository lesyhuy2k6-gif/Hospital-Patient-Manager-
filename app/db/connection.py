# connection.py
import os
import pymysql
import pymysql.cursors
from tkinter import messagebox

# Path to the configuration file (now simple, as it's in the same directory)
ENV_FILE_PATH = "app/db/.env"

def parse_env_file(file_path):
    """
    Reads the .env file using a simple relative path and returns a dictionary 
    of key-value pairs.
    """
    config = {}
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                # 1. Strip leading/trailing whitespace
                line = line.strip()
                
                # 2. Skip empty lines or comments
                if not line or line.startswith('#'):
                    continue
                
                # 3. Handle lines that contain the '=' sign
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # 4. Remove surrounding quotes
                    if value.startswith(('"', "'")) and value.endswith(('"', "'")):
                        value = value[1:-1]
                        
                    config[key] = value

    except FileNotFoundError:
        messagebox.showerror("Configuration Error", f"Configuration file not found: {file_path}")
        # Note: If running main.py from the root, the path will still be relative to the root.
        # Ensure your main script is configured to recognize the db folder as a module path.
        return None
    except Exception as e:
        messagebox.showerror("Configuration Error", f"Error reading configuration file: {e}")
        return None
        
    return config

# Load configuration from the .env file
DB_ENV_VARS = parse_env_file(ENV_FILE_PATH)

# Set DB_CONFIG using loaded variables or empty dictionary if loading failed
if DB_ENV_VARS is None:
    DB_CONFIG = {} 
else:
    DB_CONFIG = {
        "host": DB_ENV_VARS.get("DB_HOST"),
        "user": DB_ENV_VARS.get("DB_USER"),
        "passwd": DB_ENV_VARS.get("DB_PASSWORD"),
        "database": DB_ENV_VARS.get("DB_NAME")
    }

def get_connection():
    """Returns a new MySQL connection or None if an error occurs."""
    
    # Check for successful configuration loading and required keys
    required_keys = ["host", "user", "passwd", "database"]
    if any(DB_CONFIG.get(k) is None for k in required_keys):
        if DB_ENV_VARS is not None:
             messagebox.showerror("Configuration Error", "One or more required database keys (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) are missing from the .env file.")
        return None
         
    try:
        return pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            passwd=DB_CONFIG["passwd"],
            database=DB_CONFIG["database"],
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        messagebox.showerror("Connection Error", f"Failed to connect to MySQL: {e}")
        return None