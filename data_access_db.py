# 데이터 접근 모듈

import pandas as pd
import sqlite3 # 예시 라이브러리

def get_data_from_nas(customer_id, date_of_surgery):

    ############### 전부 예시임. 지우고 적절하게 코드 작성할 것 ###############
    # NAS에 접근하여 데이터를 가져옵니다.
    nas_data = pd.DataFrame()  
    return nas_data

def get_data_from_db(customer_id, date_of_surgery):

    ############### 전부 예시임. 지우고 적절하게 코드 작성할 것 ###############
    conn = sqlite3.connect('example.db')
    query = f"SELECT * FROM table WHERE customer_id={customer_id} AND date_of_surgery='{date_of_surgery}'"
    db_data = pd.read_sql_query(query, conn)
    conn.close()
    return db_data
