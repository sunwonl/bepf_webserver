import pandas as pd
import pymysql


db_conn_info = {'host': '52.205.235.146',
                'db': 'bepf',
                'user': 'root',
                'password': 'elxlfoq123!'}


if __name__ == '__main__':
    conn = pymysql.connect(**db_conn_info)

    cur = conn.cursor()

    cur.execute('show tables')

    for r in cur.fetchall():
        print(r)
