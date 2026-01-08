from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import random
import time

app = Flask(__name__)

# =========================================
# 1. LOAD MODEL & TEMAN-TEMANNYA
# =========================================
print("Sedang memuat model AI... Tunggu sebentar...")
model = joblib.load('fraud_detection_web/model/model_fraud_xgboost.pkl')
scaler = joblib.load('fraud_detection_web/model/scaler_fraud.pkl')
feature_names = joblib.load('fraud_detection_web/model/feature_names.pkl')
print("✅ Model Berhasil Dimuat!")

# =========================================
# 2. HELPER: GENERATOR DATA DUMMY
# =========================================
def generate_dummy_transaction():
    # Kita bikin data acak, tapi pola-nya kita atur biar kadang muncul Fraud
    is_fraud_scenario = random.random() < 0.15 # 15% kemungkinan muncul skenario fraud

    data = {}
    
    # Generate Fitur V1-V28 (Normal biasanya deket 0, Fraud biasanya ekstrim)
    for i in range(1, 29):
        col = f"V{i}"
        if is_fraud_scenario and col in ['V14', 'V12', 'V10']: # Fitur ciri khas fraud
            data[col] = random.uniform(-15, -5) # Bikin negatif gede
        elif is_fraud_scenario and col in ['V4', 'V11']:
            data[col] = random.uniform(5, 10)   # Bikin positif gede
        else:
            data[col] = random.uniform(-2, 2)   # Data normal (noise kecil)

    # Generate Time & Amount
    data['Time'] = random.uniform(0, 172000)
    data['Amount'] = random.uniform(1, 500) if not is_fraud_scenario else random.uniform(0, 100)

    return data

# =========================================
# 3. ROUTE UTAMA (DASHBOARD)
# =========================================
@app.route('/')
def home():
    return render_template('dashboard.html', features=feature_names)

# =========================================
# 4. ROUTE PREDIKSI MANUAL (Form Input)
# =========================================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.form.to_dict()
        for key in input_data:
            input_data[key] = float(input_data[key])
            
        # Logika Pemrosesan (Sama kayak sebelumnya)
        df_input = pd.DataFrame([input_data])
        if 'Amount' not in df_input.columns: df_input['Amount'] = 0
        if 'Time' not in df_input.columns: df_input['Time'] = 0
            
        df_input[['Amount', 'Time']] = scaler.transform(df_input[['Amount', 'Time']])
        df_final = df_input[feature_names]
        
        prediction = model.predict(df_final)[0]
        probability = model.predict_proba(df_final)[0][1]

        result = {
            'class': 'fraud' if prediction == 1 else 'normal',
            'text': '🚨 FRAUD TERDETEKSI!' if prediction == 1 else '✅ Transaksi Aman',
            'probability': f"{probability*100:.2f}%"
        }
        return jsonify(result) # Kita return JSON biar dashboard bisa nangkep tanpa reload

    except Exception as e:
        return jsonify({'error': str(e)})

# =========================================
# 5. ROUTE SIMULASI (OTOMATIS)
# =========================================
@app.route('/simulate')
def simulate():
    # 1. Bikin data dummy
    raw_data = generate_dummy_transaction()
    
    # 2. Proses persis kayak data asli
    df_input = pd.DataFrame([raw_data])
    
    # Simpan nilai asli buat ditampilin di log sebelum discale
    display_amount = df_input['Amount'].values[0]
    
    # Scaling & Filtering
    df_input[['Amount', 'Time']] = scaler.transform(df_input[['Amount', 'Time']])
    df_final = df_input[feature_names]
    
    # 3. Prediksi Real-time
    prediction = model.predict(df_final)[0]
    probability = model.predict_proba(df_final)[0][1]

    if prediction == 1:
        print(f"📧 [EMAIL SENT] To: admin@bank.com | Subject: ALERT Transaction {raw_data.get('id', 'Manual')} BLOCKED!")
    
    return jsonify({
        'id': f"TRX-{random.randint(10000, 99999)}",
        'amount': f"${display_amount:.2f}",
        'prediction': int(prediction),
        'probability': f"{probability*100:.2f}%",
        'timestamp': time.strftime("%H:%M:%S")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)