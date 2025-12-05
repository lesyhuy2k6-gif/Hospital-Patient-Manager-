from db.connection import get_connection

def update_record(table, record_id, data: dict):
    conn = get_connection()
    with conn.cursor() as cur:
        updates = ",".join([f"{k}=%s" for k in data.keys()])
        sql = f"UPDATE {table} SET {updates} WHERE id=%s"
        cur.execute(sql, list(data.values()) + [record_id])
        conn.commit()
