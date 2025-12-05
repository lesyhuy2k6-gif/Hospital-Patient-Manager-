from models.create import create_record
from models.read import get_all, get_by_id
from models.update import update_record
from models.delete import delete_record

TABLE = "treatments"

def list_treatments():
    return get_all(TABLE)

def add_treatment(data):
    return create_record(TABLE, data)

def update_treatment(pid, data):
    return update_record(TABLE, pid, data)

def delete_treatment(pid):
    return delete_record(TABLE, pid)
