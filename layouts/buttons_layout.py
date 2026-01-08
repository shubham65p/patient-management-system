from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLabel, QMessageBox, QTableWidgetItem, QWidget)
from PySide6.QtCore import Qt

from patient_dialog import PatientDialog
from database_manager import DatabaseManager
# from pages.patient_page import PatientPage
from PySide6.QtCore import Signal
from button.custom_button import CustomButton

class ButtonsLayout(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        layout = QHBoxLayout(self)
        self.db = DatabaseManager()
        # self.patient_page = PatientPage()
        self.add_btn = CustomButton("Add Patient", "#16a34a")
        # self.add_btn = QPushButton("Add Patient")
        # self.add_btn.setStyleSheet("""
        # QPushButton {
        #     background-color: #16a34a;
        #     color: white;
        #     border: none;
        #     padding: 8px 14px;
        #     border-radius: 6px;
        #     font-weight: 600;
        # }
        # QPushButton:hover {
        #     background-color: #15803d;
        # }
        # QPushButton:pressed {
        #     background-color: #166534;
        # }
        # """)
        # self.add_btn.clicked.connect(self.add_clicked.emit)
        layout.addWidget(self.add_btn)

        self.edit_btn = CustomButton("Edit Patient", "#2563eb")
        # self.edit_btn = QPushButton("Edit Patient")
        # self.edit_btn.setStyleSheet("""
        #     QPushButton {
        #         background-color: #2563eb;
        #         color: white;
        #         border: none;
        #         padding: 8px 14px;
        #         border-radius: 6px;
        #         font-weight: 600;
        #     }
        #     QPushButton:hover {
        #         background-color: #1d4ed8;
        #     }
        #     QPushButton:pressed {
        #         background-color: #1e40af;
        #     }
        #     """)
        # edit_btn.clicked.connect(self.edit_patient)
        layout.addWidget(self.edit_btn)
        self.delete_btn = CustomButton("Delete Patient", "#dc2626")
        # self.delete_btn = QPushButton("Delete Patient")
        # self.delete_btn.setStyleSheet("""
        #     QPushButton {
        #         background-color: #dc2626;
        #         color: white;
        #         border: none;
        #         padding: 8px 14px;
        #         border-radius: 6px;
        #         font-weight: 600;
        #     }
        #     QPushButton:hover {
        #         background-color: #b91c1c;
        #     }
        #     QPushButton:pressed {
        #         background-color: #991b1b;
        #     }
        #     """)
        # delete_btn.clicked.connect(self.delete_patient)
        layout.addWidget(self.delete_btn)

        # for btn in (self.add_btn, self.edit_btn, self.delete_btn):
        #     btn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addStretch()
        self.row_count_lable = QLabel("Total: 0")
        font = self.row_count_lable.font()
        font.setBold(True)
        self.row_count_lable.setFont(font)

        self.row_count_lable.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.row_count_lable)

        # self.load_buttons()

    # def load_buttons(self):
    #     self.add_btn.clicked.connect(self.add_patient)
        

    # def load_patients(self):
    #     patients = self.db.get_all_patients()
    #     # self.row_count_lable.setText()
    #     self.row_count_lable.setText(f"Total: {len(patients)}")
    #     self.populate_table(patients)

    # def populate_table(self, patients):
    #     self.patient_page.table_widget.table.setRowCount(len(patients))
    #     for row, patient in enumerate(patients):
    #         for col, value in enumerate(patient):
    #             self.patient_page.table_widget.table.setItem(row, col, QTableWidgetItem(str(value) if value else ""))


    # def add_patient(self):
    #     dialog = PatientDialog(self)
    #     if dialog.exec():
    #         data = dialog.get_data()
    #         if data[0]:  # Check if name is provided
    #             self.db.add_patient(data)
    #             self.load_patients()
    #             QMessageBox.information(self, "Success", "Patient added successfully!")
    #         else:
    #             QMessageBox.warning(self, "Error", "Patient name is required!")
        