from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QGroupBox,
    QFileDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
import numpy as np
import cv2

from ..image_viewer import ImageViewer
from ...utils.image_operations import (
    resize_image,
    rotate_image,
    zoom_image,
    InterpolationMethod,
)


class Assignment2Page(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_image = None
        self.processed_image = None

    def initUI(self):
        layout = QHBoxLayout(self)

        # Sol panel - Orijinal görüntü
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.original_image_viewer = ImageViewer()
        left_layout.addWidget(QLabel("Orijinal Görüntü"))
        left_layout.addWidget(self.original_image_viewer)

        # Sağ panel - İşlenmiş görüntü
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.processed_image_viewer = ImageViewer()
        right_layout.addWidget(QLabel("İşlenmiş Görüntü"))
        right_layout.addWidget(self.processed_image_viewer)

        # Kontrol paneli
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        # Görüntü yükleme butonu
        load_button = QPushButton("Görüntü Yükle")
        load_button.clicked.connect(self.load_image)
        control_layout.addWidget(load_button)

        # Boyut değiştirme grubu
        resize_group = QGroupBox("Boyut Değiştirme")
        resize_layout = QVBoxLayout()

        # Ölçek faktörü
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Ölçek Faktörü:"))
        self.scale_factor = QDoubleSpinBox()
        self.scale_factor.setRange(0.1, 10.0)
        self.scale_factor.setValue(1.0)
        self.scale_factor.setSingleStep(0.1)
        scale_layout.addWidget(self.scale_factor)
        resize_layout.addLayout(scale_layout)

        # İnterpolasyon yöntemi
        interpolation_layout = QHBoxLayout()
        interpolation_layout.addWidget(QLabel("İnterpolasyon:"))
        self.interpolation_method = QComboBox()
        self.interpolation_method.addItems(["Bilinear", "Bicubic", "Average"])
        interpolation_layout.addWidget(self.interpolation_method)
        resize_layout.addLayout(interpolation_layout)

        resize_button = QPushButton("Boyutu Değiştir")
        resize_button.clicked.connect(self.resize_image)
        resize_layout.addWidget(resize_button)
        resize_group.setLayout(resize_layout)
        control_layout.addWidget(resize_group)

        # Döndürme grubu
        rotate_group = QGroupBox("Döndürme")
        rotate_layout = QVBoxLayout()

        angle_layout = QHBoxLayout()
        angle_layout.addWidget(QLabel("Açı:"))
        self.angle = QSpinBox()
        self.angle.setRange(-360, 360)
        self.angle.setValue(0)
        angle_layout.addWidget(self.angle)
        rotate_layout.addLayout(angle_layout)

        rotate_button = QPushButton("Döndür")
        rotate_button.clicked.connect(self.rotate_image)
        rotate_layout.addWidget(rotate_button)
        rotate_group.setLayout(rotate_layout)
        control_layout.addWidget(rotate_group)

        # Zoom grubu
        zoom_group = QGroupBox("Zoom")
        zoom_layout = QVBoxLayout()

        zoom_factor_layout = QHBoxLayout()
        zoom_factor_layout.addWidget(QLabel("Zoom Faktörü:"))
        self.zoom_factor = QDoubleSpinBox()
        self.zoom_factor.setRange(0.1, 10.0)
        self.zoom_factor.setValue(1.0)
        self.zoom_factor.setSingleStep(0.1)
        zoom_factor_layout.addWidget(self.zoom_factor)
        zoom_layout.addLayout(zoom_factor_layout)

        zoom_button = QPushButton("Zoom Uygula")
        zoom_button.clicked.connect(self.apply_zoom)
        zoom_layout.addWidget(zoom_button)
        zoom_group.setLayout(zoom_layout)
        control_layout.addWidget(zoom_group)

        # Kaydetme butonu
        save_button = QPushButton("İşlenmiş Görüntüyü Kaydet")
        save_button.clicked.connect(self.save_image)
        control_layout.addWidget(save_button)

        control_layout.addStretch()

        # Ana layout'a panelleri ekle
        layout.addWidget(left_panel, stretch=2)
        layout.addWidget(control_panel, stretch=1)
        layout.addWidget(right_panel, stretch=2)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Görüntü Seç", "", "Image Files (*.png *.jpg *.bmp)"
        )
        if file_name:
            self.current_image = cv2.imread(file_name)
            if self.current_image is not None:
                self.display_image(self.current_image, self.original_image_viewer)
                self.processed_image = self.current_image.copy()
                self.display_image(self.processed_image, self.processed_image_viewer)

    def display_image(self, image, viewer):
        if image is not None:
            height, width = image.shape[:2]
            bytes_per_line = 3 * width
            q_image = QImage(
                image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888
            )
            viewer.setPixmap(QPixmap.fromImage(q_image))

    def resize_image(self):
        if self.current_image is None:
            return

        scale = self.scale_factor.value()
        method = self.interpolation_method.currentText()

        # İnterpolasyon yöntemini seç
        interpolation = InterpolationMethod.BILINEAR
        if method == "Bicubic":
            interpolation = InterpolationMethod.BICUBIC
        elif method == "Average":
            interpolation = InterpolationMethod.AVERAGE

        self.processed_image = resize_image(self.current_image, scale, interpolation)
        self.display_image(self.processed_image, self.processed_image_viewer)

    def rotate_image(self):
        if self.current_image is None:
            return

        angle = self.angle.value()
        method = self.interpolation_method.currentText()

        # İnterpolasyon yöntemini seç
        interpolation = InterpolationMethod.BILINEAR
        if method == "Bicubic":
            interpolation = InterpolationMethod.BICUBIC
        elif method == "Average":
            interpolation = InterpolationMethod.AVERAGE

        self.processed_image = rotate_image(self.current_image, angle, interpolation)
        self.display_image(self.processed_image, self.processed_image_viewer)

    def apply_zoom(self):
        if self.current_image is None:
            return

        zoom = self.zoom_factor.value()
        method = self.interpolation_method.currentText()

        # İnterpolasyon yöntemini seç
        interpolation = InterpolationMethod.BILINEAR
        if method == "Bicubic":
            interpolation = InterpolationMethod.BICUBIC
        elif method == "Average":
            interpolation = InterpolationMethod.AVERAGE

        self.processed_image = zoom_image(self.current_image, zoom, interpolation)
        self.display_image(self.processed_image, self.processed_image_viewer)

    def save_image(self):
        if self.processed_image is None:
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self, "Görüntüyü Kaydet", "", "PNG Files (*.png);;JPEG Files (*.jpg)"
        )
        if file_name:
            cv2.imwrite(file_name, self.processed_image)
