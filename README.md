# 🖼️ Web Temelli Görüntü İşleme Uygulaması

Modern web tabanlı bir görüntü işleme uygulaması. Kenar algılama ve köşe algılama algoritmalarını kullanarak görüntüler üzerinde gelişmiş işlemler gerçekleştirir.

## ✨ Özellikler

### 🔍 Kenar Algılama Algoritmaları
- **Sobel Operatörü**: Gradient tabanlı kenar algılama
- **Prewitt Operatörü**: 3x3 konvolüsyon matrisi ile kenar algılama
- **Roberts Operatörü**: 2x2 çapraz gradient operatörü
- **Laplacian**: İkinci türev tabanlı kenar algılama
- **Canny**: Çok aşamalı optimal kenar algılama

### 📐 Köşe Algılama Algoritmaları
- **Harris Corner Detection**: Harris matrisi ile köşe algılama
- **Shi-Tomasi**: Good Features to Track algoritması

### 🎛️ Parametre Kontrolleri
- **C Değeri**: Algoritma hassasiyeti (0.1 - 10.0)
- **Kalınlık**: Kenar kalınlığı ayarı (1 - 50)
- **Gamma**: Görüntü parlaklık korreksiyonu (0.1 - 5.0)
- **Kernel Boyutu**: İşlem kernel'i boyutu (3 - 15)

### 📷 Görüntü Giriş Yöntemleri
- Dosya yükleme (JPG, PNG, JPEG formatları)
- Real-time kamera desteği
- Drag & drop dosya yükleme

### 🎨 Kullanıcı Arayüzü
- Modern ve responsive tasarım
- Bootstrap tabanlı UI
- Real-time önizleme
- Sonuç karşılaştırma paneli

## 🚀 Kurulum

### Gereksinimler
```
Python 3.7+
Flask
OpenCV (cv2)
NumPy
```

### Kurulum Adımları

1. **Repository'yi klonlayın:**
```bash
git clone <repository-url>
cd WebTemelliGoruntuIsleme
```

2. **Sanal ortam oluşturun:**
```bash
python -m venv venv
```

3. **Sanal ortamı aktifleştirin:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Gerekli paketleri yükleyin:**
```bash
pip install flask opencv-python numpy
```

5. **Uygulamayı çalıştırın:**
```bash
python app.py
```

6. **Tarayıcınızda açın:**
```
http://localhost:5000
```

## 📋 Kullanım

1. **Görüntü Yükleme:**
   - "Resim Yükle" butonuna tıklayarak dosya seçin
   - Veya drag & drop ile görüntüyü sürükleyin

2. **Kamera Kullanımı:**
   - "Kamerayı Başlat" butonuna tıklayın
   - "Fotoğraf Çek" ile anlık görüntü alın

3. **İşlem Seçimi:**
   - Dropdown menüden istediğiniz algoritmayı seçin
   - Parametreleri ihtiyacınıza göre ayarlayın

4. **İşlemi Başlatma:**
   - "İşle" butonuna tıklayın
   - Sonuç sağ panelde görüntülenecektir

## 🏗️ Proje Yapısı

```
WebTemelliGoruntuIsleme/
├── app.py                      # Ana Flask uygulaması
├── goruntu_isleme.py          # Görüntü işleme algoritmaları
├── templates/
│   └── index.html             # Ana web sayfası
├── static/
│   ├── css/
│   │   └── style.css          # Stil dosyaları
│   ├── js/
│   │   └── main.js            # JavaScript kodları
│   ├── images/                # Varsayılan görüntüler
│   ├── icons/                 # UI ikonları
│   └── uploads/               # Yüklenen dosyalar
├── venv/                      # Python sanal ortamı
└── README.md                  # Bu dosya
```

## 🔧 Teknik Detaylar

### Backend (Python/Flask)
- **Flask**: Web framework
- **OpenCV**: Görüntü işleme kütüphanesi
- **NumPy**: Sayısal hesaplamalar
- **Base64**: Görüntü encoding/decoding

### Frontend
- **HTML5**: Yapısal düzen
- **Bootstrap 5**: UI framework
- **Vanilla JavaScript**: İnteraktivite
- **CSS3**: Özel stiller

### Algoritmalar

#### Sobel Operatörü
- Gx ve Gy gradientlerinin hesaplanması
- Magnitude hesaplaması: G = √(Gx² + Gy²)
- Gamma düzeltmesi ve kalınlık ayarı

#### Canny Kenar Algılama
- Medyan tabanlı threshold hesaplaması
- L2 gradient kullanımı
- Dilatasyon ile kalınlık artırma

#### Harris Corner Detection
- Corner response matrix hesaplaması
- K parametresi ile hassasiyet ayarı
- Köşelerin kırmızı nokta ile işaretlenmesi

## 🎯 Kullanım Alanları

- **Eğitim**: Bilgisayarlı görü algoritmalarının öğretimi
- **Araştırma**: Farklı algoritmaların karşılaştırılması
- **Prototipleme**: Hızlı görüntü işleme deneyleri
- **Demo**: Algoritma gösterimleri