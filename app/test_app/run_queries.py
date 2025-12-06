from connection import get_connection
import queries

def run():
    conn = get_connection()
    cur = conn.cursor()

    print('\nRunning G_SEARCH (sample 5 rows):')
    cur.execute(queries.G_SEARCH)
    rows = cur.fetchmany(5)
    for r in rows:
        print(r)

    print('\nRunning Q_TREATMENT_COST_DISTRIBUTION (sample 10 rows):')
    cur.execute(queries.Q_TREATMENT_COST_DISTRIBUTION)
    rows2 = cur.fetchmany(10)
    for r in rows2:
        print(r)

    conn.close()

if __name__ == '__main__':
    run()
