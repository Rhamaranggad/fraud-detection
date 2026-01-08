# 🕵️‍♂️ CyberGuard AI: Real-Time Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![XGBoost](https://img.shields.io/badge/Algorithm-XGBoost-orange)
![Flask](https://img.shields.io/badge/Framework-Flask-red)

## 📌 Overview
CyberGuard AI adalah dashboard monitoring transaksi kartu kredit berbasis **Machine Learning**. Sistem ini dirancang untuk mendeteksi transaksi penipuan (fraud) secara real-time dengan akurasi tinggi menggunakan model **XGBoost**. 

Project ini mensimulasikan aliran data transaksi dan memberikan tindakan otomatis (**Auto-Block**) jika terdeteksi adanya indikasi fraud berdasarkan pola data fitur V1-V28 (hasil PCA).

## 🚀 Fitur Utama
- **Real-Time Monitoring:** Simulasi transaksi masuk setiap 1.5 detik.
- **AI-Powered Prediction:** Klasifikasi otomatis menggunakan model XGBoost yang dioptimasi.
- **Risk Score Analysis:** Menampilkan probabilitas tingkat resiko di setiap transaksi.
- **Automated Response:** Sistem langsung memberikan status `⛔ BLOCKED` pada transaksi yang mencurigakan.
- **Cyberpunk Dashboard:** Antarmuka modern yang responsif dan interaktif.

## 🧠 Model Performance
Model telah dilatih menggunakan teknik **SMOTE** untuk menangani imbalance data dan **Feature Selection** untuk performa maksimal.
- **Top Features:** V14, V12, V10, V4, V11 (Fitur kunci pendeteksi fraud).
- **Hasil:** Model sangat sensitif terhadap nilai ekstrim pada fitur V14 (Negatif tinggi).

## 🛠️ Tech Stack
- **Backend:** Python (Flask)
- **Machine Learning:** XGBoost, Scikit-Learn, Pandas, Joblib
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
- **Deployment:** PythonAnywhere / Render

## 📦 Cara Instalasi (Lokal)
1. Clone repository ini:
   ```bash
   git clone [https://github.com/Rhamaranggad/fraud-detection.git](https://github.com/Rhamaranggad/fraud-detection.git)