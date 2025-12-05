from models.create import create_record
from models.read import get_all, get_by_id
from models.update import update_record
from models.delete import delete_record

TABLE = "patients"

def list_patients():
    return get_all(TABLE)

def add_patient(data):
    return create_record(TABLE, data)

def update_patient(pid, data):
    return update_record(TABLE, pid, data)

def delete_patient(pid):
    return delete_record(TABLE, pid)
