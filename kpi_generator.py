from kpi_2_2 import Kpi
import pandas as pd
import gc
import os
from data_access_nas import get_data_from_nas


def generate_kpi(surgery_id: str) -> pd.DataFrame:
    df_coord = get_data_from_nas(surgery_id)

    # Options를 설정합니다.
    cam = 1
    section_size = 5*1800 # section_size = 분*1800
    acceptable_missing_frames = 3
    max_section_number = 56

    try:
        sample_obj = Kpi(
        patientID = surgery_id[0:9],
        date = surgery_id[9:17],
        cam = cam,
        section_size= section_size,
        acceptable_missing_frames = acceptable_missing_frames,
        max_section_number = max_section_number,
        df_coord = df_coord
        )

        result_dict = sample_obj.return_result_dict()
        del sample_obj
    
    except Exception as e:
        print(f"KPI 객체를 생성하지 않음: {e}")
    
    gc.collect()

    # 수술 KPI를 데이터프레임으로 변환합니다.
    result_df = pd.DataFrame(result_dict, index=[0])
    
    return result_df
