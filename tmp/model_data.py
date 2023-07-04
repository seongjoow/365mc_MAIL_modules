"""
1. 나스에서 "예측 수술을 제외한 모든 수술"에 대하여 좌표값 가져온 후, kpi 추출하여 데이터프레임으로 생성
1. DB에 있는 모든 수술에 대해 테이블 추출 및 전처리 거친 후, "예측 수술을 제외"하고 데이터프레임으로 생성
2. 둘을 조인
3. 모델에 넣을 형태로 만들기 ex) meta_data 제외

"""

import pandas as pd
import os
import tempfile
import paramiko
import pyodbc
import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from db_data_processing import load_and_rename_column_db_data, preprocess_ultra, preprocess_sex, leave_feature_columns, concat_surgeryid


### NAS에 있는 모든 수술번호 가져와서 저장 후, 포문 돌리기


# Get data from DB excpet one surgery
def get_train_data_from_db(patient_id: str, surgery_date: str) -> pd.DataFrame:

    # DB login info
    server = '52.231.39.219' 
    database = 'tsfmc_data' 
    username = 'mc365' 
    password = 'tkadbrdhmc1!'  
    file_path = './query.txt'

    engine = create_engine("mssql+pyodbc://" + username + ":" + password + "@" + server + "/" + database + "?driver=SQL+Server")


    # Open and read query
    with open(file_path, 'r', encoding='UTF8') as file:
        sql = file.read()


    # Connect to database
    with engine.begin() as conn:
        # Create text from query
        query = text(sql)
        # Save result to dataframe
        df = pd.read_sql_query(query, conn)

    
    # Except surgery based on specified patient_id and date_of_discovery
    db_data = df[~(df['고객번호'] == patient_id) & (df['수술일자'] == surgery_date)]
    

    # Close connection
    conn.close()

    return db_data


def db_data_processing(patient_id:str, surgery_date:str) -> pd.DataFrame:
    
    db_data = get_train_data_from_db(patient_id, surgery_date)
    ultra_data = preprocess_ultra(db_data)
    sex_data = preprocess_sex(ultra_data)
    feat_data = leave_feature_columns(sex_data)
    surgery_data = concat_surgeryid(feat_data)
    



    
    return



