import cv2
import numpy as np

class GoruntuIsleyici:
    """
    Görüntü işleme algoritmalarını içeren ve uygulayan sınıf.
    Kenar ve köşe bulma gibi çeşitli operasyonları barındırır.
    """
    def __init__(self):
        """
        Sınıf başlatıldığında, desteklenen işlemler ve karşılık gelen
        metotları bir sözlük yapısında saklar.
        """
        self.islemler = {
            'sobel': self.sobel_kenar,
            'prewitt': self.prewitt_kenar,
            'roberts': self.roberts_kenar,
            'laplacian': self.laplacian_kenar,
            'canny': self.canny_kenar,
            'harris': self.harris_kose,
            'shi_tomasi': self.shi_tomasi_kose
        }

    def goruntu_isle(self, resim_yolu, islem, c_degeri=2, kalinlik=20, gamma=2, kernel_boyutu=5):
        """
        Belirtilen yoldaki görüntüyü okur ve istenen işlemi uygular.
        """
        resim = cv2.imread(resim_yolu)
        if resim is None:
            raise ValueError("Görüntü okunamadı veya dosya yolu geçersiz.")

        if islem in self.islemler:
            return self.islemler[islem](resim, c_degeri, kalinlik, gamma, kernel_boyutu)
        else:
            raise ValueError(f"'{islem}' adında bir işlem bulunamadı.")

    def sobel_kenar(self, resim, c_degeri, kalinlik, gamma, kernel_boyutu):
        """Sobel operatörü kullanarak kenarları tespit eder."""
        resim = self._gamma_duzeltme(resim, gamma)
        Gx = cv2.Sobel(resim, cv2.CV_64F, 1, 0, ksize=kernel_boyutu) * c_degeri
        Gy = cv2.Sobel(resim, cv2.CV_64F, 0, 1, ksize=kernel_boyutu) * c_degeri
        Gx, Gy = self._kenar_kalinlastir_morfolojik(Gx, Gy, kalinlik, kernel_boyutu)
        G = np.sqrt(Gx**2 + Gy**2)
        return np.uint8(G)

    def prewitt_kenar(self, resim, c_degeri, kalinlik, gamma, kernel_boyutu):
        """Prewitt operatörü kullanarak kenarları tespit eder."""
        resim = self._gamma_duzeltme(resim, gamma)
        kernelX = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]) * c_degeri
        kernelY = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]]) * c_degeri
        kernelX, kernelY = self._kenar_kalinlastir_resize(kernelX, kernelY, kalinlik, 3)
        Gx = cv2.filter2D(resim, cv2.CV_64F, kernelX)
        Gy = cv2.filter2D(resim, cv2.CV_64F, kernelY)
        G = np.sqrt(Gx**2 + Gy**2)
        return np.uint8(G)

    def roberts_kenar(self, resim, c_degeri, kalinlik, gamma, kernel_boyutu):
        """Roberts Cross operatörü kullanarak kenarları tespit eder."""
        resim = self._gamma_duzeltme(resim, gamma)
        kernelX = np.array([[1, 0], [0, -1]]) * c_degeri
        kernelY = np.array([[0, -1], [1, 0]]) * c_degeri
        Gx = cv2.filter2D(resim, cv2.CV_16S, kernelX)
        Gy = cv2.filter2D(resim, cv2.CV_16S, kernelY)
        Gx = cv2.convertScaleAbs(Gx)
        Gy = cv2.convertScaleAbs(Gy)
        Gx, Gy = self._kenar_kalinlastir_morfolojik(Gx, Gy, kalinlik, 2)
        return cv2.add(Gx, Gy)

    def laplacian_kenar(self, resim, c_degeri, kalinlik, gamma, kernel_boyutu):
        """Laplacian operatörü kullanarak kenarları tespit eder."""
        resim = self._gamma_duzeltme(resim, gamma)
        imgBlured = cv2.GaussianBlur(resim, (kernel_boyutu, kernel_boyutu), 0)
        result = cv2.Laplacian(imgBlured, ddepth=-1, ksize=kernel_boyutu) * c_degeri
        if kalinlik > kernel_boyutu:
            kernel = np.ones((kalinlik - kernel_boyutu, kalinlik - kernel_boyutu))
            result = cv2.dilate(result, kernel)
        return result

    def canny_kenar(self, resim, c_degeri, kalinlik, gamma, kernel_boyutu):
        """Canny kenar tespit algoritmasını uygular."""
        resim = self._gamma_duzeltme(resim, gamma)
        medianValue = np.median(resim)
        lowTH = int(max(0, 0.7 * medianValue) * c_degeri)
        highTH = int(min(255, 1.3 * medianValue) * c_degeri)
        result = cv2.Canny(resim, lowTH, highTH, L2gradient=True)
        if kalinlik > 1:
            result = cv2.dilate(result, np.ones((kalinlik, kalinlik)))
        return result

    def harris_kose(self, resim, c_degeri, kalinlik, gamma, kernel_boyutu):
        """Harris köşe tespit algoritmasını uygular."""
        resim = self._gamma_duzeltme(resim, gamma)
        gri = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)
        koseler = cv2.cornerHarris(gri, blockSize=2, ksize=kernel_boyutu, k=c_degeri * 0.01)
        koseler = cv2.dilate(koseler, None, iterations=kalinlik)
        resim[koseler > 0.01 * koseler.max()] = [0, 0, 255] # Köşeleri kırmızıya boya
        return resim

    def shi_tomasi_kose(self, resim, c_degeri, kalinlik, gamma, kernel_boyutu):
        """Shi-Tomasi köşe tespit algoritmasını uygular."""
        resim = self._gamma_duzeltme(resim, gamma)
        gri = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)
        koseler = cv2.goodFeaturesToTrack(gri, maxCorners=0, qualityLevel=c_degeri * 0.01, minDistance=kalinlik)
        if koseler is not None:
            koseler = np.int0(koseler)
            for kose in koseler:
                x, y = kose.ravel()
                cv2.circle(resim, (x, y), 3, (0, 0, 255), -1) # Köşelere daire çiz
        return resim

    # --- Yardımcı Metotlar ---

    def _gamma_duzeltme(self, resim, gamma):
        """Görüntüye gamma düzeltmesi uygular."""
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(resim, table)

    def _kenar_kalinlastir_morfolojik(self, Gx, Gy, kalinlik, kernel_boyutu):
        """Morfolojik genişletme ile kenarları kalınlaştırır."""
        if kalinlik > kernel_boyutu:
            kernel = np.ones((kalinlik - kernel_boyutu, kalinlik - kernel_boyutu))
            Gx = cv2.dilate(Gx, kernel)
            Gy = cv2.dilate(Gy, kernel)
        return Gx, Gy

    def _kenar_kalinlastir_resize(self, kernelX, kernelY, kalinlik, base_size):
        """Kernel'i yeniden boyutlandırarak kenarları kalınlaştırır."""
        if kalinlik > base_size:
            kernelX = cv2.resize(kernelX, (kalinlik, kalinlik), interpolation=cv2.INTER_NEAREST)
            kernelY = cv2.resize(kernelY, (kalinlik, kalinlik), interpolation=cv2.INTER_NEAREST)
        return kernelX, kernelY
