# 2212721046 Halil İbrahim Balık
# 2212721037 Eftalya Beril Şahin

from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from goruntu_isleme import GoruntuIsleyici
import base64
import os

app = Flask(__name__)
islemci = GoruntuIsleyici()

YUKLEME_KLASORU = 'static/uploads'
if not os.path.exists(YUKLEME_KLASORU):
    os.makedirs(YUKLEME_KLASORU)

app.config['UPLOAD_FOLDER'] = YUKLEME_KLASORU


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        islem = request.form.get('operation')
        c_degeri = float(request.form.get('c_value', 2))
        kalinlik = int(request.form.get('thickness', 20))
        gamma = float(request.form.get('gamma', 2))
        kernel_boyutu = int(request.form.get('kernel_size', 5))

        dosya = request.files['image']
        if not dosya:
            raise ValueError("Resim dosyası yüklenemedi")

        resim_yolu = os.path.join(app.config['UPLOAD_FOLDER'], dosya.filename)
        dosya.save(resim_yolu)

        sonuc = islemci.goruntu_isle(
            resim_yolu,
            islem,
            c_degeri,
            kalinlik,
            gamma,
            kernel_boyutu
        )

        _, buffer = cv2.imencode('.png', sonuc)
        img_str = base64.b64encode(buffer).decode()

        return jsonify({
            'status': 'success',
            'image': f'data:image/png;base64,{img_str}'
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


if __name__ == '__main__':
    app.run(debug=True)