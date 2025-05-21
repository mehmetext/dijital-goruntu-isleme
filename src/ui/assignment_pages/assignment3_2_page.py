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
    QGroupBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
import numpy as np
import cv2


class Assignment32Page(QWidget):
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

        # Tespit türü seçimi
        self.detection_combo = QComboBox()
        self.detection_combo.addItems(["Yol Çizgisi Tespiti", "Göz Tespiti"])
        self.detection_combo.currentIndexChanged.connect(self.update_parameters)
        top_layout.addWidget(QLabel("Tespit Türü:"))
        top_layout.addWidget(self.detection_combo)

        # Parametre ayarları grubu
        params_group = QGroupBox("Parametreler")
        params_layout = QVBoxLayout()

        # Çizgi tespiti parametreleri
        self.line_params = QWidget()
        line_layout = QVBoxLayout()

        # Rho parametresi
        rho_layout = QHBoxLayout()
        self.rho_spin = QSpinBox()
        self.rho_spin.setRange(1, 10)
        self.rho_spin.setValue(1)
        rho_layout.addWidget(QLabel("Rho:"))
        rho_layout.addWidget(self.rho_spin)
        line_layout.addLayout(rho_layout)

        # Theta parametresi
        theta_layout = QHBoxLayout()
        self.theta_spin = QDoubleSpinBox()
        self.theta_spin.setRange(0.1, 1.0)
        self.theta_spin.setValue(0.1)
        self.theta_spin.setSingleStep(0.1)
        theta_layout.addWidget(QLabel("Theta (π):"))
        theta_layout.addWidget(self.theta_spin)
        line_layout.addLayout(theta_layout)

        # Threshold parametresi
        threshold_layout = QHBoxLayout()
        self.threshold_spin = QSpinBox()
        self.threshold_spin.setRange(50, 300)
        self.threshold_spin.setValue(100)
        threshold_layout.addWidget(QLabel("Threshold:"))
        threshold_layout.addWidget(self.threshold_spin)
        line_layout.addLayout(threshold_layout)

        self.line_params.setLayout(line_layout)

        # Göz tespiti parametreleri
        self.eye_params = QWidget()
        eye_layout = QVBoxLayout()

        # Minimum yarıçap
        min_radius_layout = QHBoxLayout()
        self.min_radius_spin = QSpinBox()
        self.min_radius_spin.setRange(10, 100)
        self.min_radius_spin.setValue(20)
        min_radius_layout.addWidget(QLabel("Min Yarıçap:"))
        min_radius_layout.addWidget(self.min_radius_spin)
        eye_layout.addLayout(min_radius_layout)

        # Maximum yarıçap
        max_radius_layout = QHBoxLayout()
        self.max_radius_spin = QSpinBox()
        self.max_radius_spin.setRange(20, 200)
        self.max_radius_spin.setValue(50)
        max_radius_layout.addWidget(QLabel("Max Yarıçap:"))
        max_radius_layout.addWidget(self.max_radius_spin)
        eye_layout.addLayout(max_radius_layout)

        # Param1 (Canny edge detection threshold)
        param1_layout = QHBoxLayout()
        self.param1_spin = QSpinBox()
        self.param1_spin.setRange(10, 100)
        self.param1_spin.setValue(50)
        param1_layout.addWidget(QLabel("Param1:"))
        param1_layout.addWidget(self.param1_spin)
        eye_layout.addLayout(param1_layout)

        # Param2 (Accumulator threshold)
        param2_layout = QHBoxLayout()
        self.param2_spin = QSpinBox()
        self.param2_spin.setRange(10, 100)
        self.param2_spin.setValue(30)
        param2_layout.addWidget(QLabel("Param2:"))
        param2_layout.addWidget(self.param2_spin)
        eye_layout.addLayout(param2_layout)

        self.eye_params.setLayout(eye_layout)

        params_layout.addWidget(self.line_params)
        params_layout.addWidget(self.eye_params)
        params_group.setLayout(params_layout)
        top_layout.addWidget(params_group)

        # Uygula butonu
        self.apply_button = QPushButton("Uygula")
        self.apply_button.clicked.connect(self.apply_detection)
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

        # Başlangıçta göz parametrelerini gizle
        self.eye_params.hide()

    def update_parameters(self):
        if self.detection_combo.currentText() == "Yol Çizgisi Tespiti":
            self.line_params.show()
            self.eye_params.hide()
        else:
            self.line_params.hide()
            self.eye_params.show()

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

    def detect_lines(self, image):
        # Görüntüyü gri tonlamaya çevir
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Kenar tespiti
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Hough çizgi tespiti
        lines = cv2.HoughLines(
            edges,
            self.rho_spin.value(),
            self.theta_spin.value() * np.pi,
            self.threshold_spin.value(),
        )

        # Tespit edilen çizgileri çiz
        result = image.copy()
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 2)

        return result

    def detect_eyes(self, image):
        # Görüntüyü gri tonlamaya çevir
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Hough dairesi tespiti
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=50,
            param1=self.param1_spin.value(),
            param2=self.param2_spin.value(),
            minRadius=self.min_radius_spin.value(),
            maxRadius=self.max_radius_spin.value(),
        )

        # Tespit edilen daireleri çiz
        result = image.copy()
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # Daire çiz
                center = (i[0], i[1])
                radius = i[2]
                cv2.circle(result, center, radius, (0, 255, 0), 2)
                # Merkez noktası
                cv2.circle(result, center, 2, (0, 0, 255), 3)

        return result

    def apply_detection(self):
        if self.original_image is None:
            return

        if self.detection_combo.currentText() == "Yol Çizgisi Tespiti":
            self.processed_image = self.detect_lines(self.original_image)
        else:
            self.processed_image = self.detect_eyes(self.original_image)

        self.display_image(self.processed_image, self.processed_label)
