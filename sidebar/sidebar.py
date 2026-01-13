from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QButtonGroup, QSizePolicy)
from PySide6.QtCore import Qt

from logo_overlay import LogoOverlay
from config import config

class SideBar(QWidget):
    def __init__(self):
        super().__init__()
        self.logo = LogoOverlay(logo_path=config['logo_path'])
        
        # self.sidebar = QWidget()
        self.setFixedWidth(250)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("""
            QWidget {
                background-color: #061E29;
                
                border-radius: 5px;
            }
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 0;
                padding: 15px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:checked {
                background-color: #2980b9;
            }
        """)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(10, 20, 10, 20)
        content_layout.addWidget(self.logo)

        self.btn_patients = QPushButton("Patient Details")
        self.btn_appointments = QPushButton("Appointments")
        self.btn_invoices = QPushButton("Invoice Generation")
        self.btn_suvarnaprashn = QPushButton("Suvarnaprashn")
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        

        for btn in (self.btn_patients, self.btn_appointments, self.btn_invoices, self.btn_suvarnaprashn):
            btn.setCheckable(True)
            self.nav_group.addButton(btn)
            content_layout.addWidget(btn)

        self.btn_patients.setChecked(True)

        content_layout.addStretch()
        outer_layout.addWidget(content)
        # outer_layout.addStretch() 
