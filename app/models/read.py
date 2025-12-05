from db.connection import get_connection

def get_all(table):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {table}")
        return cur.fetchall()

def get_by_id(table, record_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {table} WHERE id=%s", (record_id,))
        return cur.fetchone()
