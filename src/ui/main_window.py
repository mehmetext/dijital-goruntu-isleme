from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QMenuBar,
    QMenu,
    QToolBar,
    QToolButton,
    QStatusBar,
    QStackedWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction, QIcon

from .assignment_pages.assignment1_page import Assignment1Page
from .assignment_pages.assignment2_page import Assignment2Page
from .assignment_pages.assignment3_1_page import Assignment31Page
from .assignment_pages.assignment3_2_page import Assignment32Page
from .assignment_pages.assignment3_3_page import Assignment33Page
from .assignment_pages.assignment3_4_page import Assignment34Page


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dijital Görüntü İşleme")
        self.setGeometry(100, 100, 1024, 768)

        self.statusBar().showMessage("Hazır")

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.assignment1_page = Assignment1Page()
        self.assignment2_page = Assignment2Page()
        self.assignment3_1_page = Assignment31Page()
        self.assignment3_2_page = Assignment32Page()
        self.assignment3_3_page = Assignment33Page()
        self.assignment3_4_page = Assignment34Page()
        self.home_page = self.create_home_page()

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.assignment1_page)
        self.stacked_widget.addWidget(self.assignment2_page)
        self.stacked_widget.addWidget(self.assignment3_1_page)
        self.stacked_widget.addWidget(self.assignment3_2_page)
        self.stacked_widget.addWidget(self.assignment3_3_page)
        self.stacked_widget.addWidget(self.assignment3_4_page)

        self.initUI()

    def create_home_page(self):
        home_widget = QWidget()
        layout = QVBoxLayout(home_widget)

        layout.addStretch(1)

        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(10)

        course_label = QLabel("Dijital Görüntü İşleme")
        course_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        course_font = QFont()
        course_font.setPointSize(24)
        course_font.setBold(True)
        course_label.setFont(course_font)

        student_label = QLabel("231229084 - Mehmet KONUKÇU")
        student_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        student_font = QFont()
        student_font.setPointSize(16)
        student_label.setFont(student_font)

        header_layout.addWidget(course_label)
        header_layout.addWidget(student_label)
        header_layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(header_widget)

        layout.addStretch(1)

        layout.setContentsMargins(20, 20, 20, 20)

        return home_widget

    def initUI(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&Dosya")

        open_action = QAction("&Görüntü Aç...", self)
        open_action.setStatusTip("Bir görüntü dosyası açar")

        save_action = QAction("&Kaydet", self)
        save_action.setStatusTip("Görüntüyü kaydeder")

        exit_action = QAction("Çı&kış", self)
        exit_action.setStatusTip("Uygulamadan çıkar")

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("&Yardım")
        about_action = QAction("&Hakkında", self)
        about_action.setStatusTip("Uygulama hakkında bilgi gösterir")
        help_menu.addAction(about_action)

        toolbar = QToolBar("Ödevler")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        home_action = QAction("Ana Sayfa", self)
        home_action.setStatusTip("Ana sayfaya dön")
        home_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        toolbar.addAction(home_action)

        toolbar.addSeparator()

        assignments = [
            ("Ödev &1", "Temel İşlevsellik", 1),
            ("Ödev &2", "Temel Görüntü Operasyonları", 2),
            ("Ödev &3.1", "S-curve Kontrast Güçlendirme", 3),
            ("Ödev &3.2", "Hough Transform ile Nesne Tespiti", 4),
            ("Ödev &3.3", "Deblurring Algoritması", 5),
            ("Ödev &3.4", "Nesne Sayma ve Özellik Çıkarma", 6),
        ]

        for number, description, page_index in assignments:
            action = QAction(f"{number}: {description}", self)
            action.setStatusTip(f"{description} ödevini açar")
            if page_index is not None:
                action.triggered.connect(
                    lambda checked, index=page_index: self.stacked_widget.setCurrentIndex(
                        index
                    )
                )
            else:
                action.setEnabled(False)
            toolbar.addAction(action)
