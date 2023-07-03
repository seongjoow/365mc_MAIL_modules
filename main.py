from predictor import predict_complication

patient_id = "210007811"
date = "20221109"

def main(customer_id, date_of_surgery):

    ############### 전부 예시임. 지우고 적절하게 코드 작성할 것 ###############
    # 후유증 예측 함수 호출
    prediction = predict_complication(customer_id, date_of_surgery)
    return {
        "customer_id": customer_id,
        "date_of_surgery": date_of_surgery,
        "complication_prediction": prediction
    }
