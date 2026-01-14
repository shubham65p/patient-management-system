from PySide6.QtWidgets import (QTableWidget, QHeaderView, QAbstractItemView)
from PySide6.QtCore import Qt

class TableWidget:
    def __init__(self) -> None:
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "", "ID", "Name", "Age", "Gender", "DOB", "Phone", "Address",
            "1st Appointment", "Major Complain", "Follow-up Date", "Total Follow-ups", 
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 60) 
        self.table.setColumnWidth(2, 60)
        self.table.setColumnWidth(6, 200) 
        self.table.setColumnWidth(11, 160)  # Consultation Charges
        self.table.setColumnWidth(12, 160)  # Medicine charges
        self.table.setColumnWidth(13, 200)  # Therapy/Panchakarma charges

        self.table.verticalHeader().setDefaultSectionSize(50) # control cell length