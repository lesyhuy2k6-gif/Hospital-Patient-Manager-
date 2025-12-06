import services as s
con = s.get_connection()
if not con:
    print('NO_CONN')
else:
    cur = con.cursor()
    try:
        cur.execute('SELECT COUNT(*) AS cnt FROM patients')
        print('patients:', cur.fetchone())
        cur.execute('SELECT COUNT(*) AS cnt FROM doctors')
        print('doctors:', cur.fetchone())
        cur.execute('SELECT COUNT(*) AS cnt FROM treatments')
        print('treatments:', cur.fetchone())
        cur.execute('SELECT COUNT(*) AS cnt FROM sessions')
        print('sessions:', cur.fetchone())
    except Exception as e:
        print('ERR', e)
    finally:
        con.close()
