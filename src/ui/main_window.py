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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dijital Görüntü İşleme")
        self.setGeometry(100, 100, 1024, 768)

        # Create status bar
        self.statusBar().showMessage("Hazır")

        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create pages
        self.assignment1_page = Assignment1Page()
        self.home_page = self.create_home_page()

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.home_page)  # index 0
        self.stacked_widget.addWidget(self.assignment1_page)  # index 1

        self.initUI()

    def create_home_page(self):
        # Create home page widget
        home_widget = QWidget()
        layout = QVBoxLayout(home_widget)

        # Add top spacing for vertical centering
        layout.addStretch(1)

        # Create header widget
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(10)

        # Course name label
        course_label = QLabel("Dijital Görüntü İşleme")
        course_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        course_font = QFont()
        course_font.setPointSize(24)
        course_font.setBold(True)
        course_label.setFont(course_font)

        # Student information label
        student_label = QLabel("231229084 - Mehmet KONUKÇU")
        student_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        student_font = QFont()
        student_font.setPointSize(16)
        student_label.setFont(student_font)

        # Add labels to header layout
        header_layout.addWidget(course_label)
        header_layout.addWidget(student_label)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Add header to main layout
        layout.addWidget(header_widget)

        # Add bottom spacing for vertical centering
        layout.addStretch(1)

        # Set the main layout margins
        layout.setContentsMargins(20, 20, 20, 20)

        return home_widget

    def initUI(self):
        # Create menubar
        menubar = self.menuBar()

        # Create File menu
        file_menu = menubar.addMenu("&Dosya")

        # Add actions to File menu
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

        # Create Help menu
        help_menu = menubar.addMenu("&Yardım")
        about_action = QAction("&Hakkında", self)
        about_action.setStatusTip("Uygulama hakkında bilgi gösterir")
        help_menu.addAction(about_action)

        # Create toolbar for assignments
        toolbar = QToolBar("Ödevler")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # Add home button
        home_action = QAction("Ana Sayfa", self)
        home_action.setStatusTip("Ana sayfaya dön")
        home_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        toolbar.addAction(home_action)

        toolbar.addSeparator()

        # Add assignment buttons to toolbar
        assignments = [
            ("Ödev &1", "Temel İşlevsellik", 1),
            ("Ödev &2", "Filtre Uygulama", None),
            ("Ödev &3", "Görüntü İyileştirme", None),
            ("Ödev &4", "Morfolojik İşlemler", None),
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
                action.setEnabled(
                    False
                )  # Henüz implement edilmemiş sayfaları devre dışı bırak
            toolbar.addAction(action)
