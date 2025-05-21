from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QFileDialog,
    QSpinBox,
    QDoubleSpinBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
import numpy as np
import cv2


class Assignment31Page(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.original_image = None
        self.processed_image = None

    def initUI(self):
        layout = QVBoxLayout(self)

        # Üst kısım - Görüntü seçme ve işlem seçenekleri
        top_layout = QHBoxLayout()

        # Görüntü seçme butonu
        self.load_button = QPushButton("Görüntü Seç")
        self.load_button.clicked.connect(self.load_image)
        top_layout.addWidget(self.load_button)

        # S-curve metodu seçimi
        self.method_combo = QComboBox()
        self.method_combo.addItems(
            [
                "Standart Sigmoid",
                "Yatay Kaydırılmış Sigmoid",
                "Eğimli Sigmoid",
                "Özel Fonksiyon",
            ]
        )
        top_layout.addWidget(QLabel("S-curve Metodu:"))
        top_layout.addWidget(self.method_combo)

        # Parametre ayarları
        self.alpha_spin = QDoubleSpinBox()
        self.alpha_spin.setRange(0.1, 10.0)
        self.alpha_spin.setValue(1.0)
        self.alpha_spin.setSingleStep(0.1)
        top_layout.addWidget(QLabel("Alpha:"))
        top_layout.addWidget(self.alpha_spin)

        self.beta_spin = QDoubleSpinBox()
        self.beta_spin.setRange(-1.0, 1.0)
        self.beta_spin.setValue(0.0)
        self.beta_spin.setSingleStep(0.1)
        top_layout.addWidget(QLabel("Beta:"))
        top_layout.addWidget(self.beta_spin)

        # Uygula butonu
        self.apply_button = QPushButton("Uygula")
        self.apply_button.clicked.connect(self.apply_contrast_enhancement)
        top_layout.addWidget(self.apply_button)

        layout.addLayout(top_layout)

        # Alt kısım - Görüntü gösterimi
        bottom_layout = QHBoxLayout()

        # Orijinal görüntü
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setMinimumSize(400, 300)
        bottom_layout.addWidget(self.original_label)

        # İşlenmiş görüntü
        self.processed_label = QLabel()
        self.processed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.processed_label.setMinimumSize(400, 300)
        bottom_layout.addWidget(self.processed_label)

        layout.addLayout(bottom_layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Görüntü Seç", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            self.original_image = cv2.imread(file_name)
            self.display_image(self.original_image, self.original_label)

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

    def standard_sigmoid(self, x, alpha):
        return 1 / (1 + np.exp(-alpha * (x - 0.5)))

    def shifted_sigmoid(self, x, alpha, beta):
        return 1 / (1 + np.exp(-alpha * (x - beta)))

    def sloped_sigmoid(self, x, alpha, beta):
        return beta + (1 - beta) / (1 + np.exp(-alpha * (x - 0.5)))

    def custom_function(self, x, alpha, beta):
        # Özel fonksiyon: Yumuşak geçişli S-eğrisi
        return np.tanh(alpha * (x - beta)) * 0.5 + 0.5

    def apply_contrast_enhancement(self):
        if self.original_image is None:
            return

        # Görüntüyü normalize et (0-1 aralığına)
        img = self.original_image.astype(np.float32) / 255.0

        # Seçilen metoda göre işlem yap
        method = self.method_combo.currentText()
        alpha = self.alpha_spin.value()
        beta = self.beta_spin.value()

        if method == "Standart Sigmoid":
            enhanced = self.standard_sigmoid(img, alpha)
        elif method == "Yatay Kaydırılmış Sigmoid":
            enhanced = self.shifted_sigmoid(img, alpha, beta)
        elif method == "Eğimli Sigmoid":
            enhanced = self.sloped_sigmoid(img, alpha, beta)
        else:  # Özel Fonksiyon
            enhanced = self.custom_function(img, alpha, beta)

        # Görüntüyü 0-255 aralığına geri dönüştür
        enhanced = (enhanced * 255).astype(np.uint8)

        self.processed_image = enhanced
        self.display_image(enhanced, self.processed_label)
