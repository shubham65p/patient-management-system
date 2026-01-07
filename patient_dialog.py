from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTableWidget, QTableWidgetItem, 
                               QPushButton, QLineEdit, QLabel, QDialog, 
                               QFormLayout, QComboBox, QDateEdit, QTextEdit,
                               QMessageBox, QHeaderView, QSpinBox, QAbstractItemView)
from PySide6.QtCore import QDate


class PatientDialog(QDialog):
    def __init__(self, parent=None, patient_data=None):
        super().__init__(parent)
        self.patient_data = patient_data
        self.setWindowTitle("Add Patient" if not patient_data else "Edit Patient")
        self.setMinimumWidth(500)
        self.setup_ui()
        
        if patient_data:
            self.populate_data()
    
    def setup_ui(self):
        layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.age_input = QSpinBox()
        self.age_input.setRange(0, 150)
        
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("yyyy-MM-dd")

        self.dob_input.setDate(QDate.currentDate())
        
        self.phone_input = QLineEdit()
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        
        self.first_appointment_input = QDateEdit()
        self.first_appointment_input.setCalendarPopup(True)
        self.first_appointment_input.setDisplayFormat("yyyy-MM-dd")
        self.first_appointment_input.setDate(QDate.currentDate())
        
        self.major_complain_input = QTextEdit()
        self.major_complain_input.setMaximumHeight(100)
        
        self.followup_date_input = QDateEdit()
        self.followup_date_input.setCalendarPopup(True)
        self.followup_date_input.setDisplayFormat("yyyy-MM-dd")

        self.followup_date_input.setDate(QDate.currentDate().addDays(7))
        
        self.total_followups_input = QSpinBox()
        self.total_followups_input.setRange(0, 999)
        
        layout.addRow("Name:", self.name_input)
        layout.addRow("Age:", self.age_input)
        layout.addRow("Gender:", self.gender_input)
        layout.addRow("Date of Birth:", self.dob_input)
        layout.addRow("Phone Number:", self.phone_input)
        layout.addRow("Address:", self.address_input)
        layout.addRow("Date of 1st Appointment:", self.first_appointment_input)
        layout.addRow("Major Complain:", self.major_complain_input)
        layout.addRow("Follow-up Date:", self.followup_date_input)
        layout.addRow("Total No. of Follow-ups:", self.total_followups_input)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addRow(btn_layout)
        self.setLayout(layout)
    
    def populate_data(self):
        if self.patient_data:
            self.name_input.setText(self.patient_data[1])
            self.age_input.setValue(int(self.patient_data[2]) or 0)
            self.gender_input.setCurrentText(self.patient_data[3] or "Male")
            
            if self.patient_data[4]:
                self.dob_input.setDate(QDate.fromString(self.patient_data[4], "yyyy-MM-dd"))
            
            self.phone_input.setText(self.patient_data[5] or "")
            self.address_input.setText(self.patient_data[6] or "")
            
            if self.patient_data[7]:
                self.first_appointment_input.setDate(QDate.fromString(self.patient_data[7], "yyyy-MM-dd"))
            
            self.major_complain_input.setText(self.patient_data[8] or "")
            
            if self.patient_data[9]:
                self.followup_date_input.setDate(QDate.fromString(self.patient_data[9], "yyyy-MM-dd"))
            if self.patient_data[10]:
                self.total_followups_input.setValue(int(self.patient_data[10]) or 0)
    
    def get_data(self):
        return (
            self.name_input.text(),
            self.age_input.value(),
            self.gender_input.currentText(),
            self.dob_input.date().toString("yyyy-MM-dd"),
            self.phone_input.text(),
            self.address_input.toPlainText(),
            self.first_appointment_input.date().toString("yyyy-MM-dd"),
            self.major_complain_input.toPlainText(),
            self.followup_date_input.date().toString("yyyy-MM-dd"),
            self.total_followups_input.value()
        )




