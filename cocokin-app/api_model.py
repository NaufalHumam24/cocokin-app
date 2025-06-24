from flask import Flask, request, jsonify
from flask_cors import CORS
from catboost import CatBoostClassifier
import numpy as np

app = Flask(__name__)
CORS(app)

# Load model
try:
    model = CatBoostClassifier()
    model.load_model("model_rekomendasi_jurusan(catboost).cbm")
except Exception as e:
    print("Gagal memuat model:", e)
    model = None

# Mapping
map_jawaban = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
map_kategori = {
    1: 'Sains & Teknologi',
    2: 'Sosial & Humaniora',
    3: 'Bisnis & Ekonomi',
    4: 'Seni & Desain'
}

deskripsi_kategori = {
    'Sains & Teknologi': 'Kamu suka hal teknis, analitis, dan senang menyelesaikan masalah logis.',
    'Sosial & Humaniora': 'Kamu peduli isu sosial, suka berinteraksi dan memahami manusia.',
    'Bisnis & Ekonomi': 'Kamu cenderung logis, suka strategi, dan tertarik dunia usaha serta keuangan.',
    'Seni & Desain': 'Kamu ekspresif, kreatif, dan menyukai hal-hal yang visual dan estetik.'
}

rekomendasi_kategori = {
    'Sains & Teknologi': ['Teknik Informatika', 'Teknik Elektro', 'Matematika', 'Teknik Sipil'],
    'Sosial & Humaniora': ['Psikologi', 'Ilmu Komunikasi', 'Sosiologi', 'Hukum'],
    'Bisnis & Ekonomi': ['Manajemen Bisnis', 'Akuntansi', 'Ekonomi Pembangunan', 'Kewirausahaan'],
    'Seni & Desain': ['Desain Komunikasi Visual', 'Seni Rupa', 'Arsitektur Interior', 'Animasi']
}

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model belum dimuat dengan benar.'}), 500

    data = request.get_json()
    jawaban = data.get('jawaban', [])

    if not jawaban or len(jawaban) != 20:
        return jsonify({'error': 'Data jawaban harus terdiri dari 20 huruf A/B/C/D'}), 400

    if not all(j in ['A', 'B', 'C', 'D'] for j in jawaban):
        return jsonify({'error': 'Jawaban hanya boleh berupa A, B, C, atau D'}), 400

    try:
        jumlah = {huruf: jawaban.count(huruf) for huruf in ['A', 'B', 'C', 'D']}
        input_angka = [map_jawaban[j] for j in jawaban]
        input_array = np.array([input_angka])

        pred_kode = int(model.predict(input_array)[0])
        kelas = map_kategori[pred_kode]

        return jsonify({
            'kelas': kelas,
            'prediksi_kode': pred_kode,
            'jumlah': jumlah,
            'deskripsi': deskripsi_kategori[kelas],
            'rekomendasi': rekomendasi_kategori[kelas]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
