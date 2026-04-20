from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import numpy as np


app = Flask(__name__)
CORS(app)

model         = joblib.load('models/best_model.pkl')
feature_names = joblib.load('models/feature_names.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Student Performance API is running!'})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        gender_map      = {'male': 1, 'female': 0}
        prep_map        = {'completed': 1, 'none': 0}
        lunch_map       = {'standard': 1, 'free/reduced': 0}
        ethnicity_map   = {'group A': 0, 'group B': 1, 'group C': 2,
                           'group D': 3, 'group E': 4}
        education_map   = {"associate's degree": 0, "bachelor's degree": 1,
                           "high school": 2, "master's degree": 3,
                           "some college": 4, "some high school": 5}

        input_data = np.array([[
            gender_map[data['gender']],
            ethnicity_map[data['ethnicity']],
            education_map[data['parental_education']],
            lunch_map[data['lunch']],
            prep_map[data['test_prep']]
        ]])

        prediction  = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        return jsonify({
            'prediction':  int(prediction),
            'result':      'PASS ✅' if prediction == 1 else 'FAIL ❌',
            'probability': round(float(probability) * 100, 2),
            'message':     f"Student is likely to {'Pass' if prediction==1 else 'Fail'} with {round(float(probability)*100,2)}% confidence"
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
   import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
scaler = joblib.load('models/scaler.pkl')
input_data = scaler.transform(input_data)

    