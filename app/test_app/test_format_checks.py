from connection import get_connection
import queries as q
from ui import fmt_date
from datetime import datetime, date
import decimal

def check_global_search():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(q.G_SEARCH, ('%','%','%'))
    rows = cur.fetchmany(5)
    if not rows:
        print('No rows returned from G_SEARCH')
        return
    cols = list(rows[0].keys())
    print('G_SEARCH columns:', cols)
    for r in rows:
        vals = [r[c] for c in cols]
        vals = [fmt_date(v) if isinstance(v, (datetime, date)) else v for v in vals]
        print('formatted row:', vals)
    conn.close()

def check_report():
    conn = get_connection()
    cur = conn.cursor()
    sql = '''
        SELECT p.name AS Patient, t.name AS Treatment, s.treatment_date AS Date, t.cost AS Cost
        FROM sessions s
        JOIN patients p ON s.patient_id = p.patient_id
        JOIN treatments t ON s.treatment_id = t.treatment_id
        ORDER BY s.treatment_date DESC
        LIMIT 5
    '''
    cur.execute(sql)
    rows = cur.fetchall()
    if not rows:
        print('No rows returned from report SQL')
        return
    cols = list(rows[0].keys())
    print('Report columns:', cols)
    for r in rows:
        vals = [r[c] for c in cols]
        vals = [fmt_date(v) if isinstance(v, (datetime, date)) else (float(v) if isinstance(v, decimal.Decimal) else v) for v in vals]
        print('formatted report row:', vals)
    conn.close()

if __name__ == '__main__':
    check_global_search()
    check_report()
