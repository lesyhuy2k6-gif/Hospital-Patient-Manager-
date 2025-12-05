import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",    # put your MySQL password here
        database="hospital"
    )
    