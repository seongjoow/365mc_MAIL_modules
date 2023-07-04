# 후유증 예측 모듈

import os
import joblib
import pandas as pd
from data_processing import join_and_process_data


# Path to each model
model_paths = {
    '장액종': os.path.join("models", ".pkl"),
    '멍': os.path.join("models", ".pkl"),
    '뭉침': os.path.join("models", ".pkl"),
    '울퉁불퉁': os.path.join("models", ".pkl")
}

# Load models
models = {}
for side_effect, path in model_paths.items():
        models[side_effect] = joblib.load(path)

def predict_sideeffect(patient_id, surgery_date):
    input_data = join_and_process_data(patient_id, surgery_date)

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
