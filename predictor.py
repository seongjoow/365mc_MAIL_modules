# 후유증 예측 모듈

import os
import joblib
import pandas as pd
from data_processing import join_and_process_data


# Path to each model
model_paths = {
    '장액종': os.path.join("models", "장액종_RFmodel.pkl"),
    '멍': os.path.join("models", "멍_RFmodel.pkl"),
    '뭉침': os.path.join("models", "뭉침_RFmodel.pkl"),
    '울퉁불퉁': os.path.join("models", "울퉁불퉁_RFmodel.pkl")
}

# Load models
models = {}
for side_effect, path in model_paths.items():
        models[side_effect] = joblib.load(path)

def predict_sideeffect(patient_id, surgery_date):
    input_data = join_and_process_data(patient_id, surgery_date)

    # 모델에 넣을 데이터에서 메타 데이터를 제거합니다.
    input_data = input_data.drop(['SurgeryID, PatientID, SurgerDate, BodyPart'], axis=1)

    predictions = {}
    confidences = {}
    
    for side_effect, model in models.items():
        # Predict using each model
        prediction = model.predict(input_data)
        predictions[side_effect] = prediction

        # scikit-learn의 predict_proba 메서드를 사용하여 예측의 신뢰도를 계산합니다.
        confidence = model.predict_proba(input_data)
        confidences[side_effect] = confidence

    return predictions, confidences
