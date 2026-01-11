from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from typing import Optional


class LogoOverlay(QWidget):
    def __init__(self, parent=None, logo_path: Optional[str] = None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if logo_path:
            pixmap = QPixmap(logo_path)
            self.logo.setPixmap(
                pixmap.scaled(
                    250, 250,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

        # Opacity effect
        # effect = QGraphicsOpacityEffect()
        # effect.setOpacity(0.4)
        # self.logo.setGraphicsEffect(effect)

        layout.addWidget(self.logo)
