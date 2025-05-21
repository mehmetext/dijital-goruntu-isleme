from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QSpinBox,
    QDoubleSpinBox,
    QGroupBox,
    QSlider,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
import numpy as np
import cv2


class Assignment33Page(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.original_image = None
        self.processed_image = None
        self.blurred_image = None

    def initUI(self):
        layout = QVBoxLayout(self)

        # Üst kısım - Görüntü seçme ve işlem seçenekleri
        top_layout = QHBoxLayout()

        # Görüntü seçme butonu
        self.load_button = QPushButton("Görüntü Seç")
        self.load_button.clicked.connect(self.load_image)
        top_layout.addWidget(self.load_button)

        # Parametre ayarları grubu
        params_group = QGroupBox("Deblurring Parametreleri")
        params_layout = QVBoxLayout()

        # Bulanıklık parametreleri
        blur_group = QGroupBox("Bulanıklık Parametreleri")
        blur_layout = QVBoxLayout()

        # Kernel boyutu
        kernel_layout = QHBoxLayout()
        self.kernel_spin = QSpinBox()
        self.kernel_spin.setRange(3, 31)
        self.kernel_spin.setValue(5)
        self.kernel_spin.setSingleStep(2)
        kernel_layout.addWidget(QLabel("Kernel Boyutu:"))
        kernel_layout.addWidget(self.kernel_spin)
        blur_layout.addLayout(kernel_layout)

        # Bulanıklık açısı
        angle_layout = QHBoxLayout()
        self.angle_spin = QSpinBox()
        self.angle_spin.setRange(0, 180)
        self.angle_spin.setValue(45)
        angle_layout.addWidget(QLabel("Bulanıklık Açısı:"))
        angle_layout.addWidget(self.angle_spin)
        blur_layout.addLayout(angle_layout)

        # Bulanıklık miktarı
        length_layout = QHBoxLayout()
        self.length_spin = QSpinBox()
        self.length_spin.setRange(1, 50)
        self.length_spin.setValue(10)
        length_layout.addWidget(QLabel("Bulanıklık Miktarı:"))
        length_layout.addWidget(self.length_spin)
        blur_layout.addLayout(length_layout)

        blur_group.setLayout(blur_layout)
        params_layout.addWidget(blur_group)

        # Deblurring parametreleri
        deblur_group = QGroupBox("Deblurring Parametreleri")
        deblur_layout = QVBoxLayout()

        # Wiener filtresi parametresi
        k_layout = QHBoxLayout()
        self.k_spin = QDoubleSpinBox()
        self.k_spin.setRange(0.001, 0.1)
        self.k_spin.setValue(0.01)
        self.k_spin.setSingleStep(0.001)
        k_layout.addWidget(QLabel("Wiener K:"))
        k_layout.addWidget(self.k_spin)
        deblur_layout.addLayout(k_layout)

        # İterasyon sayısı
        iter_layout = QHBoxLayout()
        self.iter_spin = QSpinBox()
        self.iter_spin.setRange(1, 50)
        self.iter_spin.setValue(10)
        iter_layout.addWidget(QLabel("İterasyon Sayısı:"))
        iter_layout.addWidget(self.iter_spin)
        deblur_layout.addLayout(iter_layout)

        deblur_group.setLayout(deblur_layout)
        params_layout.addWidget(deblur_group)

        params_group.setLayout(params_layout)
        top_layout.addWidget(params_group)

        # Butonlar
        buttons_layout = QVBoxLayout()

        # Bulanıklaştır butonu
        self.blur_button = QPushButton("Bulanıklaştır")
        self.blur_button.clicked.connect(self.apply_blur)
        buttons_layout.addWidget(self.blur_button)

        # Deblur butonu
        self.deblur_button = QPushButton("Deblur Uygula")
        self.deblur_button.clicked.connect(self.apply_deblur)
        buttons_layout.addWidget(self.deblur_button)

        top_layout.addLayout(buttons_layout)
        layout.addLayout(top_layout)

        # Alt kısım - Görüntü gösterimi
        bottom_layout = QHBoxLayout()

        # Orijinal görüntü
        original_group = QGroupBox("Orijinal Görüntü")
        original_layout = QVBoxLayout()
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setMinimumSize(300, 300)
        original_layout.addWidget(self.original_label)
        original_group.setLayout(original_layout)
        bottom_layout.addWidget(original_group)

        # Bulanık görüntü
        blurred_group = QGroupBox("Bulanık Görüntü")
        blurred_layout = QVBoxLayout()
        self.blurred_label = QLabel()
        self.blurred_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blurred_label.setMinimumSize(300, 300)
        blurred_layout.addWidget(self.blurred_label)
        blurred_group.setLayout(blurred_layout)
        bottom_layout.addWidget(blurred_group)

        # Deblur edilmiş görüntü
        deblurred_group = QGroupBox("Deblur Edilmiş Görüntü")
        deblurred_layout = QVBoxLayout()
        self.deblurred_label = QLabel()
        self.deblurred_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.deblurred_label.setMinimumSize(300, 300)
        deblurred_layout.addWidget(self.deblurred_label)
        deblurred_group.setLayout(deblurred_layout)
        bottom_layout.addWidget(deblurred_group)

        layout.addLayout(bottom_layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Görüntü Seç", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            self.original_image = cv2.imread(file_name)
            self.display_image(self.original_image, self.original_label)
            self.blurred_image = None
            self.processed_image = None
            self.display_image(None, self.blurred_label)
            self.display_image(None, self.deblurred_label)

    def display_image(self, image, label):
        if image is not None:
            height, width = image.shape[:2]
            bytes_per_line = 3 * width
            q_image = QImage(
                image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888
            ).rgbSwapped()
            pixmap = QPixmap.fromImage(q_image)
            label.setPixmap(
                pixmap.scaled(
                    label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            label.clear()

    def create_motion_blur_kernel(self, size, angle, length):
        # Hareket bulanıklığı kernel'i oluştur
        kernel = np.zeros((size, size))
        center = size // 2

        # Açıyı radyana çevir
        angle_rad = np.deg2rad(angle)

        # Kernel'in merkezinden geçen çizgiyi çiz
        for i in range(length):
            x = int(center + i * np.cos(angle_rad))
            y = int(center + i * np.sin(angle_rad))
            if 0 <= x < size and 0 <= y < size:
                kernel[y, x] = 1.0

        # Kernel'i normalize et
        kernel = kernel / np.sum(kernel)
        return kernel

    def apply_blur(self):
        if self.original_image is None:
            return

        # Hareket bulanıklığı kernel'i oluştur
        kernel = self.create_motion_blur_kernel(
            self.kernel_spin.value(), self.angle_spin.value(), self.length_spin.value()
        )

        # Bulanıklığı uygula
        self.blurred_image = cv2.filter2D(self.original_image, -1, kernel)
        self.display_image(self.blurred_image, self.blurred_label)

    def apply_deblur(self):
        if self.blurred_image is None:
            return

        # Görüntüyü gri tonlamaya çevir
        gray = cv2.cvtColor(self.blurred_image, cv2.COLOR_BGR2GRAY)

        # Hareket bulanıklığı kernel'i oluştur
        kernel = self.create_motion_blur_kernel(
            self.kernel_spin.value(), self.angle_spin.value(), self.length_spin.value()
        )

        # Wiener filtresi ile deblur
        deblurred = self.wiener_deblur(gray, kernel, self.k_spin.value())

        # İteratif deblur
        for _ in range(self.iter_spin.value()):
            deblurred = self.iterative_deblur(deblurred, kernel)

        # Görüntüyü BGR'ye geri dönüştür
        self.processed_image = cv2.cvtColor(deblurred, cv2.COLOR_GRAY2BGR)
        self.display_image(self.processed_image, self.deblurred_label)

    def wiener_deblur(self, image, kernel, k):
        # Wiener filtresi ile deblur
        kernel_fft = np.fft.fft2(kernel, s=image.shape)
        image_fft = np.fft.fft2(image)

        # Wiener filtresi
        kernel_fft_conj = np.conj(kernel_fft)
        wiener_filter = kernel_fft_conj / (np.abs(kernel_fft) ** 2 + k)

        # Filtreyi uygula
        deblurred_fft = image_fft * wiener_filter
        deblurred = np.real(np.fft.ifft2(deblurred_fft))

        # Değerleri 0-255 aralığına normalize et
        deblurred = np.clip(deblurred, 0, 255).astype(np.uint8)

        return deblurred

    def iterative_deblur(self, image, kernel):
        # İteratif deblur
        # Lucy-Richardson algoritması benzeri bir yaklaşım
        blurred = cv2.filter2D(image, -1, kernel)
        ratio = image.astype(float) / (blurred.astype(float) + 1e-10)
        correction = cv2.filter2D(ratio, -1, kernel)
        deblurred = image * correction

        # Değerleri 0-255 aralığına normalize et
        deblurred = np.clip(deblurred, 0, 255).astype(np.uint8)

        return deblurred
