from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
import cv2
import numpy as np


class Assignment1Page(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Ana layout
        layout = QVBoxLayout(self)

        # Başlık
        title = QLabel("Ödev 1: Temel İşlevsellik")
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Açıklama
        description = QLabel(
            "Bu ödevde görüntü yükleme ve temel işlevler gösterilmektedir.\n"
            "Aşağıdaki butonu kullanarak bir görüntü seçebilirsiniz."
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)

        # Görüntü yükleme butonu
        self.load_button = QPushButton("Görüntü Yükle")
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        # Görüntü gösterme alanı
        self.image_container = QWidget()
        self.image_layout = QHBoxLayout(self.image_container)

        # Orijinal görüntü
        self.original_image_label = QLabel("Orijinal Görüntü")
        self.original_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_image_label.setMinimumSize(300, 300)
        self.original_image_label.setStyleSheet("border: 1px solid #ccc;")

        # İşlenmiş görüntü
        self.processed_image_label = QLabel("İşlenmiş Görüntü")
        self.processed_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.processed_image_label.setMinimumSize(300, 300)
        self.processed_image_label.setStyleSheet("border: 1px solid #ccc;")

        self.image_layout.addWidget(self.original_image_label)
        self.image_layout.addWidget(self.processed_image_label)

        layout.addWidget(self.image_container)

        # İşlem butonları
        self.process_buttons = QHBoxLayout()

        self.grayscale_button = QPushButton("Gri Tonlama")
        self.grayscale_button.setEnabled(False)
        self.grayscale_button.clicked.connect(self.convert_to_grayscale)

        self.invert_button = QPushButton("Negatif")
        self.invert_button.setEnabled(False)
        self.invert_button.clicked.connect(self.invert_image)

        self.process_buttons.addWidget(self.grayscale_button)
        self.process_buttons.addWidget(self.invert_button)

        layout.addLayout(self.process_buttons)

        # Alt boşluk
        layout.addStretch()

        self.setLayout(layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Görüntü Seç",
            "",
            "Görüntü Dosyaları (*.png *.jpg *.jpeg *.bmp *.gif);;Tüm Dosyalar (*)",
        )

        if file_name:
            # Görüntüyü yükle ve göster
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(
                300,
                300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.original_image_label.setPixmap(scaled_pixmap)

            # Orijinal görüntüyü sınıf değişkeni olarak sakla
            self.original_pixmap = pixmap

            # İşlem butonlarını aktif et
            self.grayscale_button.setEnabled(True)
            self.invert_button.setEnabled(True)

    def convert_to_grayscale(self):
        """
        Orijinal görüntüyü gri tonlamalı hale dönüştürür.
        """
        if hasattr(self, "original_pixmap") and not self.original_pixmap.isNull():
            # QPixmap'i QImage'e dönüştür
            image = self.original_pixmap.toImage()

            # QImage'i numpy dizisine dönüştür
            width = image.width()
            height = image.height()
            ptr = image.constBits()
            ptr.setsize(height * width * 4)  # 4 kanal (RGBA)
            arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))

            # BGR formatına dönüştür (OpenCV için)
            bgr_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

            # Gri tonlamaya dönüştür
            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

            # Gri tonlamalı görüntüyü tekrar QImage'e dönüştür
            h, w = gray_image.shape
            bytes_per_line = w
            q_image = QImage(
                gray_image.data, w, h, bytes_per_line, QImage.Format.Format_Grayscale8
            )

            # QImage'i QPixmap'e dönüştür ve göster
            processed_pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = processed_pixmap.scaled(
                300,
                300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.processed_image_label.setPixmap(scaled_pixmap)

    def invert_image(self):
        """
        Orijinal görüntünün negatifini alır.
        """
        if hasattr(self, "original_pixmap") and not self.original_pixmap.isNull():
            # QPixmap'i QImage'e dönüştür
            image = self.original_pixmap.toImage()

            # QImage'i numpy dizisine dönüştür
            width = image.width()
            height = image.height()
            ptr = image.constBits()
            ptr.setsize(height * width * 4)  # 4 kanal (RGBA)
            arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))

            # BGR formatına dönüştür (OpenCV için)
            bgr_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

            # Görüntüyü negatife çevir (255 - piksel değeri)
            inverted_image = cv2.bitwise_not(bgr_image)

            # Negatif görüntüyü tekrar QImage'e dönüştür
            inverted_rgb = cv2.cvtColor(inverted_image, cv2.COLOR_BGR2RGB)
            h, w, c = inverted_rgb.shape
            bytes_per_line = c * w
            q_image = QImage(
                inverted_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888
            )

            # QImage'i QPixmap'e dönüştür ve göster
            processed_pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = processed_pixmap.scaled(
                300,
                300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.processed_image_label.setPixmap(scaled_pixmap)
