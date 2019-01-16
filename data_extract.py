import pandas as pd
import pymysql


db_conn_info = {'host': '127.0.0.1',
                'db': 'bepf',
                'user': 'root',
                'password': 'elxlfoq12#'}

if __name__ == '__main__':
    conn = pymysql.connect(**db_conn_info)

