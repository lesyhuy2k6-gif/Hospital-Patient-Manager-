from models.create import create_record
from models.read import get_all, get_by_id
from models.update import update_record
from models.delete import delete_record

TABLE = "doctors"

def list_doctors():
    return get_all(TABLE)

def add_doctor(data):
    return create_record(TABLE, data)

def update_doctor(pid, data):
    return update_record(TABLE, pid, data)

def delete_doctor(pid):
    return delete_record(TABLE, pid)
