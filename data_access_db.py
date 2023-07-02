# DB 데이터 접근 모듈

import pandas as pd
import sqlalchemy
import pyodbc
from sqlalchemy.sql import text
from sqlalchemy import create_engine


def get_data_from_db(patient_id: str, date_of_surgery: str) -> pd.DataFrame:

    # DB 로그인 정보
    server = '52.231.39.219' 
    database = 'tsfmc_data' 
    username = 'mc365' 
    password = 'tkadbrdhmc1!'  
    file_path = './query.txt'

    engine = create_engine("mssql+pyodbc://" + username + ":" + password + "@" + server + "/" + database + "?driver=SQL+Server")


    # 쿼리문 열고 읽기
    with open(file_path, 'r', encoding='UTF8') as file:
        sql = file.read()


    # 데이터베이스 연결
    with engine.begin() as conn:
        # SQL 쿼리를 텍스트 형태로 생성
        query = text(sql)
        # 쿼리 실행 결과를 데이터프레임으로 저장
        df = pd.read_sql_query(query, conn)

    db_data = df[(df['고객번호'] == patient_id) & (df['수술일자'] == date_of_surgery)]
    
    # exception
    if (len(db_data) == 0):
        print("해당 고객번호와 수술일자를 가진 데이터가 없습니다.")
        print("고객번호:",patient_id, ", 수술일자:", date_of_surgery)


    # 연결 종료
    conn.close()

    return db_data

check = get_data_from_db('180000611', '20220620')
print(check)



