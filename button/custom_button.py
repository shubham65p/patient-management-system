from PySide6.QtWidgets import (QPushButton)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class CustomButton(QPushButton):
    def __init__(self, text, color, margin = '2px') -> None:
        super().__init__(text)
        # self = QPushButton(text)
        def darken(color: str, factor: int) -> str:
            c = QColor(color)
            return c.darker(factor).name()

        hover = darken(color, 110)
        pressed = darken(color, 120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 8px 14px;
                border-radius: 6px;
                font-weight: 600;
                margin: {margin};
                font-size: 10px
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
        """)

    