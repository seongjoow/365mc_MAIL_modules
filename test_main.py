from data_access_nas import get_data_from_nas
from kpi_generator import generate_kpi


# # Parameters for test (김대겸씨)
# patient_id = '180000611'
# surgery_date = '20220620'


# patient_id = '180006545'
# surgery_date = '20221020'

patient_id = "210038775"
surgery_date = "20230215"
surgery_id = patient_id + surgery_date

# df_nas = get_data_from_nas(surgery_id)
# df_nas.to_csv('coord_test.csv', index=False)

df_kpi = generate_kpi(surgery_id)
df_kpi.to_csv('kpi_test.csv', index=False)

# print(df_kpi)