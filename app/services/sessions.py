from models.create import create_record
from models.read import get_all, get_by_id
from models.update import update_record
from models.delete import delete_record

TABLE = "sessions"

def list_sessions():
    return get_all(TABLE)

def add_session(data):
    return create_record(TABLE, data)

def update_session(pid, data):
    return update_record(TABLE, pid, data)

def delete_session(pid):
    return delete_record(TABLE, pid)
