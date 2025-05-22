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
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
import numpy as np
import cv2
import pandas as pd
from scipy.stats import entropy


class Assignment34Page(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.original_image = None
        self.processed_image = None
        self.objects = []

    def initUI(self):
        layout = QVBoxLayout(self)

        # Üst kısım - Görüntü seçme ve işlem seçenekleri
        top_layout = QHBoxLayout()

        # Görüntü seçme butonu
        self.load_button = QPushButton("Görüntü Seç")
        self.load_button.clicked.connect(self.load_image)
        top_layout.addWidget(self.load_button)

        # Parametre ayarları grubu
        params_group = QGroupBox("Nesne Tespiti Parametreleri")
        params_layout = QVBoxLayout()

        # HSV renk aralığı parametreleri
        hsv_group = QGroupBox("HSV Renk Aralığı")
        hsv_layout = QVBoxLayout()

        # H değeri aralığı
        h_layout = QHBoxLayout()
        self.h_min_spin = QSpinBox()
        self.h_min_spin.setRange(0, 179)
        self.h_min_spin.setValue(35)
        self.h_max_spin = QSpinBox()
        self.h_max_spin.setRange(0, 179)
        self.h_max_spin.setValue(85)
        h_layout.addWidget(QLabel("H:"))
        h_layout.addWidget(self.h_min_spin)
        h_layout.addWidget(QLabel("-"))
        h_layout.addWidget(self.h_max_spin)
        hsv_layout.addLayout(h_layout)

        # S değeri aralığı
        s_layout = QHBoxLayout()
        self.s_min_spin = QSpinBox()
        self.s_min_spin.setRange(0, 255)
        self.s_min_spin.setValue(50)
        self.s_max_spin = QSpinBox()
        self.s_max_spin.setRange(0, 255)
        self.s_max_spin.setValue(255)
        s_layout.addWidget(QLabel("S:"))
        s_layout.addWidget(self.s_min_spin)
        s_layout.addWidget(QLabel("-"))
        s_layout.addWidget(self.s_max_spin)
        hsv_layout.addLayout(s_layout)

        # V değeri aralığı
        v_layout = QHBoxLayout()
        self.v_min_spin = QSpinBox()
        self.v_min_spin.setRange(0, 255)
        self.v_min_spin.setValue(50)
        self.v_max_spin = QSpinBox()
        self.v_max_spin.setRange(0, 255)
        self.v_max_spin.setValue(255)
        v_layout.addWidget(QLabel("V:"))
        v_layout.addWidget(self.v_min_spin)
        v_layout.addWidget(QLabel("-"))
        v_layout.addWidget(self.v_max_spin)
        hsv_layout.addLayout(v_layout)

        hsv_group.setLayout(hsv_layout)
        params_layout.addWidget(hsv_group)

        # Morfolojik işlem parametreleri
        morph_group = QGroupBox("Morfolojik İşlemler")
        morph_layout = QVBoxLayout()

        # Kernel boyutu
        kernel_layout = QHBoxLayout()
        self.kernel_spin = QSpinBox()
        self.kernel_spin.setRange(1, 21)
        self.kernel_spin.setValue(3)
        self.kernel_spin.setSingleStep(2)
        kernel_layout.addWidget(QLabel("Kernel Boyutu:"))
        kernel_layout.addWidget(self.kernel_spin)
        morph_layout.addLayout(kernel_layout)

        # Minimum nesne alanı
        min_area_layout = QHBoxLayout()
        self.min_area_spin = QSpinBox()
        self.min_area_spin.setRange(10, 1000)
        self.min_area_spin.setValue(100)
        min_area_layout.addWidget(QLabel("Min Alan:"))
        min_area_layout.addWidget(self.min_area_spin)
        morph_layout.addLayout(min_area_layout)

        morph_group.setLayout(morph_layout)
        params_layout.addWidget(morph_group)

        params_group.setLayout(params_layout)
        top_layout.addWidget(params_group)

        # İşlem butonları
        buttons_layout = QVBoxLayout()

        # Nesne tespiti butonu
        self.detect_button = QPushButton("Nesneleri Tespit Et")
        self.detect_button.clicked.connect(self.detect_objects)
        buttons_layout.addWidget(self.detect_button)

        # Excel'e kaydet butonu
        self.save_button = QPushButton("Excel'e Kaydet")
        self.save_button.clicked.connect(self.save_to_excel)
        buttons_layout.addWidget(self.save_button)

        top_layout.addLayout(buttons_layout)
        layout.addLayout(top_layout)

        # Alt kısım - Görüntü gösterimi ve tablo
        bottom_layout = QHBoxLayout()

        # Sol taraf - Görüntüler
        images_layout = QVBoxLayout()

        # Orijinal görüntü
        original_group = QGroupBox("Orijinal Görüntü")
        original_layout = QVBoxLayout()
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setMinimumSize(300, 300)
        original_layout.addWidget(self.original_label)
        original_group.setLayout(original_layout)
        images_layout.addWidget(original_group)

        # İşlenmiş görüntü
        processed_group = QGroupBox("Tespit Edilen Nesneler")
        processed_layout = QVBoxLayout()
        self.processed_label = QLabel()
        self.processed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.processed_label.setMinimumSize(300, 300)
        processed_layout.addWidget(self.processed_label)
        processed_group.setLayout(processed_layout)
        images_layout.addWidget(processed_group)

        bottom_layout.addLayout(images_layout)

        # Sağ taraf - Özellik tablosu
        table_group = QGroupBox("Nesne Özellikleri")
        table_layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            [
                "No",
                "Center",
                "Length",
                "Width",
                "Diagonal",
                "Energy",
                "Entropy",
                "Mean",
                "Median",
            ]
        )
        header = self.table.horizontalHeader()
        for i in range(9):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)
        bottom_layout.addWidget(table_group)

        layout.addLayout(bottom_layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Görüntü Seç", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            self.original_image = cv2.imread(file_name)
            self.display_image(self.original_image, self.original_label)
            self.processed_image = None
            self.display_image(None, self.processed_label)
            self.table.setRowCount(0)
            self.objects = []

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

    def detect_objects(self):
        if self.original_image is None:
            return

        # Görüntüyü HSV'ye çevir
        hsv = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)

        # Koyu yeşil renk aralığını belirle
        lower = np.array(
            [self.h_min_spin.value(), self.s_min_spin.value(), self.v_min_spin.value()]
        )
        upper = np.array(
            [self.h_max_spin.value(), self.s_max_spin.value(), self.v_max_spin.value()]
        )

        # Renk maskesi oluştur
        mask = cv2.inRange(hsv, lower, upper)

        # Morfolojik işlemler
        kernel = np.ones((self.kernel_spin.value(), self.kernel_spin.value()), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Konturları bul
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Sonuç görüntüsünü hazırla
        result = self.original_image.copy()
        self.objects = []

        # Her kontur için özellikleri hesapla
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area < self.min_area_spin.value():
                continue

            # Kontur özellikleri
            x, y, w, h = cv2.boundingRect(contour)
            center = (x + w // 2, y + h // 2)
            diagonal = np.sqrt(w**2 + h**2)

            # Nesne bölgesini al
            roi = mask[y : y + h, x : x + w]

            # Enerji ve entropi hesapla
            energy = np.sum(roi**2) / (w * h)
            hist = cv2.calcHist([roi], [0], None, [256], [0, 256])
            hist = hist / np.sum(hist)
            entropy_val = float(entropy(hist.flatten()))

            # Ortalama ve medyan hesapla
            mean_val = np.mean(roi)
            median_val = np.median(roi)

            # Nesne bilgilerini kaydet
            self.objects.append(
                {
                    "no": i + 1,
                    "center": f"{center[0]},{center[1]}",
                    "length": h,
                    "width": w,
                    "diagonal": diagonal,
                    "energy": energy,
                    "entropy": entropy_val,
                    "mean": mean_val,
                    "median": median_val,
                }
            )

            # Konturu çiz
            cv2.drawContours(result, [contour], -1, (0, 255, 0), 2)
            cv2.putText(
                result, str(i + 1), center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
            )

        # Sonuç görüntüsünü göster
        self.processed_image = result
        self.display_image(result, self.processed_label)

        # Tabloyu güncelle
        self.update_table()

    def update_table(self):
        self.table.setRowCount(len(self.objects))
        for i, obj in enumerate(self.objects):
            self.table.setItem(i, 0, QTableWidgetItem(str(obj["no"])))
            self.table.setItem(i, 1, QTableWidgetItem(obj["center"]))
            self.table.setItem(i, 2, QTableWidgetItem(f"{obj['length']} px"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{obj['width']} px"))
            self.table.setItem(i, 4, QTableWidgetItem(f"{obj['diagonal']:.1f} px"))
            self.table.setItem(i, 5, QTableWidgetItem(f"{obj['energy']:.3f}"))
            self.table.setItem(i, 6, QTableWidgetItem(f"{obj['entropy']:.2f}"))
            self.table.setItem(i, 7, QTableWidgetItem(f"{obj['mean']:.1f}"))
            self.table.setItem(i, 8, QTableWidgetItem(f"{obj['median']:.1f}"))

    def save_to_excel(self):
        if not self.objects:
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self, "Excel Dosyasını Kaydet", "", "Excel Files (*.xlsx)"
        )
        if file_name:
            # DataFrame oluştur
            df = pd.DataFrame(self.objects)

            # Excel'e kaydet
            df.to_excel(file_name, index=False)
