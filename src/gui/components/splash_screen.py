from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QProgressBar, QApplication
from PyQt5.QtCore import Qt, QTimer

class SplashScreen(QWidget):
    """Modern splash screen with loading animation."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dream.OS Cell Phone - Loading...")
        self.setFixedSize(600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
        self.start_loading_animation()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        container = QFrame()
        container.setObjectName("splashContainer")
        container.setStyleSheet("""
            #splashContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2C3E50, stop:1 #3498DB);
                border-radius: 20px;
                border: 2px solid #34495E;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        logo_label = QLabel("📱")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("""
            QLabel {
                font-size: 80px;
                color: white;
                margin: 20px;
            }
        """)
        container_layout.addWidget(logo_label)
        title_label = QLabel("Dream.OS Cell Phone")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: white;
                margin: 10px;
            }
        """)
        container_layout.addWidget(title_label)
        subtitle_label = QLabel("Autonomous Agent Communication System")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #BDC3C7;
                margin: 5px;
            }
        """)
        container_layout.addWidget(subtitle_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #34495E;
                border-radius: 10px;
                text-align: center;
                background-color: #2C3E50;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E74C3C, stop:0.5 #F39C12, stop:1 #27AE60);
                border-radius: 8px;
            }
        """)
        self.progress_bar.setFixedHeight(20)
        container_layout.addWidget(self.progress_bar)
        self.loading_label = QLabel("Initializing system...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #BDC3C7;
                margin: 5px;
            }
        """)
        container_layout.addWidget(self.loading_label)
        version_label = QLabel("v2.0 - Modern Interface")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #7F8C8D;
                margin: 5px;
            }
        """)
        container_layout.addWidget(version_label)
        layout.addWidget(container)
        self.center_on_screen()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def start_loading_animation(self):
        self.progress = 0
        self.loading_steps = [
            "Initializing system...",
            "Loading agent coordinates...",
            "Establishing communication...",
            "Preparing interface...",
            "Ready!"
        ]
        self.current_step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loading)
        self.timer.start(200)

    def update_loading(self):
        self.progress += 2
        self.progress_bar.setValue(self.progress)
        step_index = min(self.progress // 20, len(self.loading_steps) - 1)
        self.loading_label.setText(self.loading_steps[step_index])
        if self.progress >= 100:
            self.timer.stop()
            self.close()
            self.main_window.show() 