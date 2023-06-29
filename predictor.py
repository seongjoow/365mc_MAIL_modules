# 후유증 예측 모듈

from sklearn.externals import joblib  # 예시. 사전에 학습된 모델을 불러오는 경우
from data_processing import join_and_process_data

def predict_complication(customer_id, date_of_surgery):

    ############### 전부 예시임. 지우고 적절하게 코드 작성할 것 ###############
    data = join_and_process_data(customer_id, date_of_surgery)
    
    # 사전에 학습된 모델을 불러옵니다.
    model = joblib.load('model.pkl')  
    
    # 예측을 수행합니다.
    prediction = model.predict(data)  
    
    return prediction
