from db.connection import get_connection

def delete_record(table, record_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(f"DELETE FROM {table} WHERE id=%s", (record_id,))
        conn.commit()
