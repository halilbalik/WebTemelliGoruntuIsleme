# -*- coding: utf-8 -*-
# Proje Sahipleri:
# 2212721046 Halil İbrahim Balık
# 2212721037 Eftalya Beril Şahin

from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from goruntu_isleme import GoruntuIsleyici
import base64
import os

# Flask uygulamasının başlatılması
app = Flask(__name__)
# Görüntü işleme operasyonları için GoruntuIsleyici sınıfından bir örnek (instance) oluşturulur.
islemci = GoruntuIsleyici()

# Yüklenen dosyaların kaydedileceği klasör yolu
YUKLEME_KLASORU = 'static/uploads'
# Eğer belirtilen klasör mevcut değilse, oluşturulur.
if not os.path.exists(YUKLEME_KLASORU):
    os.makedirs(YUKLEME_KLASORU)

# Flask konfigürasyonuna yükleme klasörünün yolu eklenir.
app.config['UPLOAD_FOLDER'] = YUKLEME_KLASORU


@app.route('/')
def index():
    """
    Uygulamanın ana sayfasını render eder.
    """
    return render_template('index.html')


@app.route('/process_image', methods=['POST'])
def process_image():
    """
    Kullanıcı tarafından yüklenen görüntü üzerinde, seçilen görüntü işleme operasyonunu uygular.
    İşlem sonucunda elde edilen görüntüyü JSON formatında geri döner.
    """
    try:
        # Form üzerinden gelen operasyon ve parametrelerin alınması
        islem = request.form.get('operation')
        c_degeri = float(request.form.get('c_value', 2))
        kalinlik = int(request.form.get('thickness', 20))
        gamma = float(request.form.get('gamma', 2))
        kernel_boyutu = int(request.form.get('kernel_size', 5))

        # Görüntü dosyasının request'ten alınması
        dosya = request.files.get('image')
        if not dosya:
            raise ValueError("Görüntü dosyası bulunamadı.")

        # Görüntünün sunucuda geçici bir yola kaydedilmesi
        resim_yolu = os.path.join(app.config['UPLOAD_FOLDER'], dosya.filename)
        dosya.save(resim_yolu)

        # GoruntuIsleyici sınıfı üzerinden ilgili işlemin gerçekleştirilmesi
        sonuc = islemci.goruntu_isle(
            resim_yolu,
            islem,
            c_degeri,
            kalinlik,
            gamma,
            kernel_boyutu
        )

        # İşlenen görüntünün base64 formatına çevrilerek web arayüzünde gösterime hazırlanması
        _, buffer = cv2.imencode('.png', sonuc)
        img_str = base64.b64encode(buffer).decode()

        # Başarılı işlem sonucunun JSON olarak döndürülmesi
        return jsonify({
            'status': 'success',
            'image': f'data:image/png;base64,{img_str}'
        })

    except Exception as e:
        # Hata durumunda hatanın mesajını JSON olarak döndürür.
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


if __name__ == '__main__':
    # Flask uygulamasının geliştirme sunucusunda çalıştırılması
    app.run(debug=True)
