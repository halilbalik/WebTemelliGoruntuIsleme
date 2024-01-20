import cv2
import numpy as np

class GoruntuIsleyici:
    def __init__(self):
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
        resim = cv2.imread(resim_yolu)
        if resim is None:
            raise ValueError("Resim okunamadı")

        if islem in self.islemler:
            return self.islemler[islem](resim, c_degeri, kalinlik, gamma, kernel_boyutu)
        else:
            raise ValueError("Geçersiz işlem")

    def sobel_kenar(self, resim, c_degeri=2, kalinlik=20, gamma=2, kernel_boyutu=3):
        resim = np.power(resim / 255.0, gamma) * 255.0
        resim = np.uint8(resim)
        Gx = cv2.Sobel(resim, cv2.CV_64F, 1, 0, ksize=kernel_boyutu) * c_degeri
        Gy = cv2.Sobel(resim, cv2.CV_64F, 0, 1, ksize=kernel_boyutu) * c_degeri
        if kalinlik > kernel_boyutu:
            Gx = cv2.dilate(Gx, np.ones((kalinlik - kernel_boyutu, kalinlik - kernel_boyutu)))
            Gy = cv2.dilate(Gy, np.ones((kalinlik - kernel_boyutu, kalinlik - kernel_boyutu)))
        G = np.sqrt(Gx * Gx + Gy * Gy)
        return np.uint8(G)

    def prewitt_kenar(self, resim, c_degeri=2, kalinlik=20, gamma=2, kernel_boyutu=3):
        resim = np.power(resim / 255.0, gamma) * 255.0
        resim = np.uint8(resim)
        kernelX = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]) * c_degeri
        kernelY = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]]) * c_degeri
        if kalinlik > 3:
            kernelX = cv2.resize(kernelX, (kalinlik, kalinlik))
            kernelY = cv2.resize(kernelY, (kalinlik, kalinlik))
        Gx = cv2.filter2D(resim, cv2.CV_64F, kernelX)
        Gy = cv2.filter2D(resim, cv2.CV_64F, kernelY)
        G = np.sqrt(Gx * Gx + Gy * Gy)
        return np.uint8(G)

    def roberts_kenar(self, resim, c_degeri=2, kalinlik=20, gamma=2, kernel_boyutu=3):
        resim = np.power(resim / 255.0, gamma) * 255.0
        resim = np.uint8(resim)
        kernelX = np.array([[1, 0], [0, -1]]) * c_degeri
        kernelY = np.array([[0, -1], [1, 0]]) * c_degeri
        Gx = cv2.filter2D(resim, cv2.CV_16S, kernelX)
        Gy = cv2.filter2D(resim, cv2.CV_16S, kernelY)
        Gx = cv2.convertScaleAbs(Gx)
        Gy = cv2.convertScaleAbs(Gy)
        if kalinlik > 2:
            Gx = cv2.dilate(Gx, np.ones((kalinlik - 2, kalinlik - 2)))
            Gy = cv2.dilate(Gy, np.ones((kalinlik - 2, kalinlik - 2)))
        G = Gx + Gy
        return G

    def laplacian_kenar(self, resim, c_degeri=2, kalinlik=20, gamma=2, kernel_boyutu=3):
        resim = np.power(resim / 255.0, gamma) * 255.0
        resim = np.uint8(resim)
        imgBlured = cv2.GaussianBlur(resim, (kernel_boyutu, kernel_boyutu), 0)
        result = cv2.Laplacian(imgBlured, ddepth=-1, ksize=kernel_boyutu) * c_degeri
        if kalinlik > kernel_boyutu:
            result = cv2.dilate(result, np.ones((kalinlik - kernel_boyutu, kalinlik - kernel_boyutu)))
        return result

    def canny_kenar(self, resim, c_degeri=2, kalinlik=20, gamma=2, kernel_boyutu=3):
        resim = np.power(resim / 255.0, gamma) * 255.0
        resim = np.uint8(resim)
        medianValue = np.median(resim)
        lowTH = int(max(0, 0.7 * medianValue)) * c_degeri
        highTH = int(min(255, 1.3 * medianValue)) * c_degeri
        result = cv2.Canny(resim, lowTH, highTH, L2gradient=True)
        if kalinlik > 1:
            result = cv2.dilate(result, np.ones((kalinlik, kalinlik)))
        return result

    def harris_kose(self, resim, c_degeri=2, kalinlik=20, gamma=2, kernel_boyutu=3):
        resim = np.power(resim / 255.0, gamma) * 255.0
        resim = np.uint8(resim)
        resim_rgb = cv2.cvtColor(resim, cv2.COLOR_BGR2RGB)
        gri = cv2.cvtColor(resim_rgb, cv2.COLOR_RGB2GRAY)
        koseler = cv2.cornerHarris(gri, blockSize=2, ksize=kernel_boyutu, k=c_degeri * 0.01)
        koseler = cv2.dilate(koseler, None, iterations=kalinlik)
        resim_rgb[koseler > 0.01 * koseler.max()] = [255, 0, 0]
        return cv2.cvtColor(resim_rgb, cv2.COLOR_RGB2BGR)

    def shi_tomasi_kose(self, resim, c_degeri=2, kalinlik=20, gamma=2, kernel_boyutu=3):
        resim = np.power(resim / 255.0, gamma) * 255.0
        resim = np.uint8(resim)
        resim_rgb = cv2.cvtColor(resim, cv2.COLOR_BGR2RGB)
        gri = cv2.cvtColor(resim_rgb, cv2.COLOR_RGB2GRAY)
        koseler = cv2.goodFeaturesToTrack(gri, 0, c_degeri * 0.01, kalinlik)
        koseler = np.int32(koseler)
        for kose in koseler:
            x, y = kose.ravel()
            cv2.circle(resim_rgb, (x, y), 3, (255, 0, 0), -1)
        return cv2.cvtColor(resim_rgb, cv2.COLOR_RGB2BGR)