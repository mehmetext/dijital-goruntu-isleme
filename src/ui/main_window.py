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
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction, QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dijital Görüntü İşleme")
        self.setGeometry(100, 100, 1024, 768)

        # Create status bar
        self.statusBar().showMessage("Hazır")

        self.initUI()

    def initUI(self):
        # Create menubar
        menubar = self.menuBar()

        # Create File menu
        file_menu = menubar.addMenu("&Dosya")  # Alt+D kısayolu için & eklendi

        # Add actions to File menu
        open_action = QAction("&Görüntü Aç...", self)  # Alt+G kısayolu
        open_action.setStatusTip("Bir görüntü dosyası açar")

        save_action = QAction("&Kaydet", self)  # Alt+K kısayolu
        save_action.setStatusTip("Görüntüyü kaydeder")

        exit_action = QAction("Çı&kış", self)  # Alt+K kısayolu
        exit_action.setStatusTip("Uygulamadan çıkar")

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Create Help menu
        help_menu = menubar.addMenu("&Yardım")  # Alt+Y kısayolu
        about_action = QAction("&Hakkında", self)  # Alt+H kısayolu
        about_action.setStatusTip("Uygulama hakkında bilgi gösterir")
        help_menu.addAction(about_action)

        # Create toolbar for assignments
        toolbar = QToolBar("Ödevler")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)  # Toolbar'ın ayrı pencere olarak açılmasını engelle
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # Add assignment buttons to toolbar
        assignments = [
            ("Ödev &1", "Temel İşlevsellik"),
            ("Ödev &2", "Filtre Uygulama"),
            ("Ödev &3", "Görüntü İyileştirme"),
            ("Ödev &4", "Morfolojik İşlemler"),
        ]

        for number, description in assignments:
            action = QAction(f"{number}: {description}", self)
            action.setStatusTip(f"{description} ödevini açar")
            toolbar.addAction(action)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Add top spacing for vertical centering
        main_layout.addStretch(1)

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
        main_layout.addWidget(header_widget)

        # Add bottom spacing for vertical centering
        main_layout.addStretch(1)

        # Set the main layout margins
        main_layout.setContentsMargins(20, 20, 20, 20)
