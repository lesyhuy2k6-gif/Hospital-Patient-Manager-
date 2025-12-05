from db.connection import get_connection

def create_record(table, data: dict):
    conn = get_connection()
    with conn.cursor() as cur:
        fields = ",".join(data.keys())
        values = ",".join(["%s"] * len(data))
        sql = f"INSERT INTO {table}({fields}) VALUES ({values})"
        cur.execute(sql, list(data.values()))
        conn.commit()
        return cur.lastrowid
