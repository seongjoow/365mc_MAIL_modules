from data_access_nas import get_data_from_nas
from kpi_generator import generate_kpi

patient_id = "210038775"
surgery_date = "20230215"
surgery_id = patient_id + surgery_date

df_nas = get_data_from_nas(surgery_id)
df_nas.to_csv('coord_test.csv', index=False)

# df_kpi = generate_kpi(surgery_id)
# df_kpi.to_csv('kpi_test.csv', index=False)

# print(df_kpi)