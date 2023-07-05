from predictor import predict_sideeffect


def predict_and_return(patient_id: str, surgery_date: str):

    # 후유증 예측 함수 호출
    predictions, confidences = predict_sideeffect(patient_id, surgery_date)

    return patient_id, surgery_date, predictions, confidences
