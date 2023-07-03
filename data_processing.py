# 데이터 조인 및 처리 모듈

import pandas as pd
from data_access_db import get_data_from_db
from data_access_nas import get_data_from_nas

def join_and_process_data(patient_id:str, date_of_surgery:str) -> pd.DataFrame:

    ############### 전부 예시임. 지우고 적절하게 코드 작성할 것 ###############
    nas_data = get_data_from_nas(patient_id, date_of_surgery)
    db_data = get_data_from_db(patient_id, date_of_surgery)
    
    # 필터링

    # kpi generator 
    
    # 데이터를 조인합니다.
    combined_data = pd.merge(nas_data, db_data, on='patient_id')  

    # 필요한 처리를 수행합니다. (결측치를 채우거나, 데이터를 스케일링하거나, 특성을 추출하는 등의 작업)
    processed_data = combined_data  # 실제 처리를 위한 코드
    return processed_data
