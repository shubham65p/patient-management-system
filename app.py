import sys
import sqlite3
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTableWidget, QTableWidgetItem, 
                               QPushButton, QLineEdit, QLabel, QDialog, 
                               QFormLayout, QComboBox, QDateEdit, QTextEdit,
                               QMessageBox, QHeaderView, QSpinBox, QAbstractItemView)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

from database_manager import DatabaseManager
from patient_dialog import PatientDialog
# from load_config import config

class PatientManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.search_result_count = 0
        # self.setWindowTitle(config['title'])
        self.setWindowTitle('Patient Management System')
        self.setMinimumSize(1200, 700)
        self.setup_ui()
        self.load_patients()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("Patient Management System")
        header.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        # Search section
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search by:"))
        
        self.search_criteria = QComboBox()
        self.search_criteria.addItems(["name", "phone", "major_complain", "gender"])
        search_layout.addWidget(self.search_criteria)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        search_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_patients)
        search_layout.addWidget(search_btn)
        
        clear_btn = QPushButton("Show All")
        clear_btn.clicked.connect(self.load_patients)
        search_layout.addWidget(clear_btn)
        
        search_layout.addStretch()
        main_layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Age", "Gender", "DOB", "Phone", "Address",
            "1st Appointment", "Major Complain", "Follow-up Date", "Total Follow-ups"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        main_layout.addWidget(self.table)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Patient")
        add_btn.clicked.connect(self.add_patient)
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit Patient")
        edit_btn.clicked.connect(self.edit_patient)
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete Patient")
        delete_btn.clicked.connect(self.delete_patient)
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        self.row_count_lable = QLabel("Total: 0")
        font = self.row_count_lable.font()
        font.setBold(True)
        self.row_count_lable.setFont(font)
        
        self.row_count_lable.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        btn_layout.addWidget(self.row_count_lable)
        main_layout.addLayout(btn_layout)
    
    def load_patients(self):
        patients = self.db.get_all_patients()
        # self.row_count_lable.setText()
        self.row_count_lable.setText(f"Total: {len(patients)}")
        self.populate_table(patients)
    
    def populate_table(self, patients):
        self.table.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            for col, value in enumerate(patient):
                self.table.setItem(row, col, QTableWidgetItem(str(value) if value else ""))
    
    def add_patient(self):
        dialog = PatientDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if data[0]:  # Check if name is provided
                self.db.add_patient(data)
                self.load_patients()
                QMessageBox.information(self, "Success", "Patient added successfully!")
            else:
                QMessageBox.warning(self, "Error", "Patient name is required!")
    
    def edit_patient(self):
        current_row = self.table.currentRow()
        print('current row: ', current_row)
        if current_row >= 0:
            item = self.table.item(current_row, 0)
            if item is None:
                QMessageBox.warning(self, "Error", "Invalid patient data!")
            print('item: ', item.text()) # type: ignore
            patient_id = int(item.text()) # type: ignore
            # patient_id = int(self.table.item(current_row, 0).text())
            patient_data = [self.table.item(current_row, col).text()  # type: ignore
                          for col in range(self.table.columnCount())]
            print('patient_data: ', patient_data)
            dialog = PatientDialog(self, patient_data)
            if dialog.exec():
                data = dialog.get_data()
                if data[0]:
                    self.db.update_patient(patient_id, data)
                    self.load_patients()
                    QMessageBox.information(self, "Success", "Patient updated successfully!")
                else:
                    QMessageBox.warning(self, "Error", "Patient name is required!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a patient to edit!")
    
    def delete_patient(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            patient_id = int(self.table.item(current_row, 0).text()) # type: ignore
            patient_name = self.table.item(current_row, 1).text() # type: ignore
            
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete patient '{patient_name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.db.delete_patient(patient_id)
                self.load_patients()
                QMessageBox.information(self, "Success", "Patient deleted successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a patient to delete!")
    
    def search_patients(self):
        criteria = self.search_criteria.currentText()
        value = self.search_input.text()
        
        if value:
            patients = self.db.search_patients(criteria, value)
            row_count = len(patients)

            self.populate_table(patients)
            self.row_count_lable.setText(f"Total: {row_count}")
        else:
            self.load_patients()

def main():
    app = QApplication(sys.argv)
    window = PatientManagementSystem()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()