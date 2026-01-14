from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel)
from PySide6.QtGui import QFont, QPainter, QColor, QPen
from PySide6.QtCore import Qt

from layouts.search_layout import SearchLayout
from layouts.table_widget import TableWidget
from layouts.buttons_layout import ButtonsLayout
from config import config

class PatientPage(QWidget):
    def __init__(self, btn_layout):
        super().__init__()
        layout = QVBoxLayout(self)
        self.btn_layout = btn_layout
        self.search_layout = SearchLayout()
        self.table_widget = TableWidget()
        
        header = QLabel(config['title'])
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
        QLabel {
            font-size: 22px;
            font-weight: 700;
            color: #111827;
            padding: 12px;
            letter-spacing: 1px;
            background-color: #f9fafb;
            border-bottom: 1px solid #e5e7eb;
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #2F6690, stop:1 #f8fafc
            );
            border-radius: 10px;
            border-bottom: 1px solid #cbd5f5;
            
            transition: all 0.9s;
        }
        QLabel:hover {
            background-color: #e0f2fe;
        }
        """)
        header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(header)

        self.search_layout.layout.addStretch()
        layout.addLayout(self.search_layout.layout)

        layout.addWidget(self.table_widget.table)

        layout.addWidget(btn_layout)
