import sys
import sqlite3
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTableWidget, QTableWidgetItem, 
                               QPushButton, QLineEdit, QLabel, QDialog, 
                               QFormLayout, QComboBox, QDateEdit, QTextEdit,
                               QMessageBox, QHeaderView, QSpinBox, QAbstractItemView,
                               QFrame, QButtonGroup, QStackedWidget)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from pydantic import ValidationError

from data_validation import Patient
from database_manager import DatabaseManager
from patient_dialog import PatientDialog
from config import config

from PySide6.QtGui import QFont, QPainter, QColor, QPen
from services.patient_search_service import PatientSearchService
from watermark_widget import WatermarkWidget

# from layouts.search_layout import SearchLayout
# from layouts.table_widget import TableWidget
from layouts.buttons_layout import ButtonsLayout

from pages.patient_page import PatientPage
from pages.appointment_page import AppointmentPage

from sidebar.sidebar import SideBar
from database.SQLiteDB.connection import SQLiteConnection
from database.SQLiteDB.schema import SchemaManager
from create_directory_for_database import create_dir
from repositories.patient_repository import PatientRepository
from repositories.appointment_repository import AppointmentRepository
from repositories.medicine_repository import MedicineRepository
from repositories.therapy_repository import TherapyRepository
from button.custom_button import CustomButton
from database.db_protocol import Database
from database.SQLiteDB.sqlite_database import SQLiteDatabase

class PatientManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        folder_name = create_dir()
        self.conn = SQLiteConnection(f'C:\\ProgramData\\{folder_name}\\patients.db').get_connection()
        db = SQLiteDatabase(self.conn)
        SchemaManager(db).create_tables()
        
        self.patient_repo = PatientRepository(db)
        self.appointment_repo = AppointmentRepository(db)
        self.medicine_repo = MedicineRepository(db)
        self.therapy_repo = TherapyRepository(db)
        self.search_result_count = 0
        self.setWindowTitle(config['title'])
        self.btn_layout = ButtonsLayout()
        self.sidebar = SideBar()
        self.patient_page = PatientPage(self.btn_layout)
        self.setup_ui()
        self.load_patients()
        

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.watermark.setGeometry(self.centralWidget().rect())


    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5,5,5,5)

        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                background-color: green;
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

        sidebar_layout = QVBoxLayout(sidebar)
                
        main_layout.addWidget(self.sidebar)

        self.patient_page.btn_layout.add_btn.clicked.connect(self.add_patient)
        self.patient_page.btn_layout.edit_btn.clicked.connect(self.edit_patient)
        self.patient_page.btn_layout.delete_btn.clicked.connect(self.delete_patient)

        self.patient_page.search_layout.search_btn.clicked.connect(self.search_patients)
        self.patient_page.search_layout.clear_btn.clicked.connect(self.load_patients)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.patient_page)
        self.stack.addWidget(AppointmentPage())
        
        

                
        main_layout.addWidget(self.stack)

        self.sidebar.btn_patients.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.sidebar.btn_appointments.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        self.watermark = WatermarkWidget(central_widget)
        self.watermark.setGeometry(central_widget.rect())
        self.watermark.raise_()

    def load_patients(self):
        patients = self.patient_repo.get_all()
        self.patient_page.btn_layout.row_count_lable.setText(f"Total: {len(patients)}")
        self.populate_table(patients)
    
    def view_history(self):
        print('btn clicked')
    
    def populate_table(self, patients):
        self.patient_page.table_widget.table.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            view_history_btn = CustomButton("View", '#1D546D', margin='10px')
            view_history_btn.clicked.connect(self.view_history)
            self.patient_page.table_widget.table.setCellWidget(row, 0, view_history_btn)
            for col, value in enumerate(patient, 1):
                item = QTableWidgetItem(str(value) if value else "")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.patient_page.table_widget.table.setItem(row, col, item)
    
    def add_patient(self):
        print('add button clicked')
        dialog = PatientDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            print('dataaaaaaaaaaa: ', data)

            try:
                patient = Patient(**data)
            except ValidationError as e:
                print("Data is Ivalid : {e}")
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    e.json(indent=2)
                )
                return
            
            patient_id = self.patient_repo.add(patient)

            for ap in patient.fees.data:
                appt_id = self.appointment_repo.add(
                    patient_id, 
                    ap.appointment, 
                    ap.consultation
                    )
                
                for med in ap.medicines:
                    self.medicine_repo.add(
                        appt_id, 
                        med.name,
                        med.fee
                        )
                    
                for the in ap.therapies:
                    self.therapy_repo.add(
                        appt_id, 
                        the.name,
                        the.fee
                        )
            self.load_patients()
            QMessageBox.information(self, "Success", "Patient added successfully!")
        else:
            QMessageBox.warning(self, "Error", "Patient name is required!")

    def edit_patient(self):
        current_row = self.patient_page.table_widget.table.currentRow()

        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a patient to edit!")
            return
        print('current_row: ', current_row)
        item = self.patient_page.table_widget.table.item(current_row, 1)
        print('itemmmmm: ', item)
        if item is None:
            QMessageBox.warning(self, "Error", "Invalid patient data!")
            return

        patient_id = int(item.text())
        print('paitent_id: ', patient_id)
        patient_data = [
            self.patient_page.table_widget.table.item(current_row, col).text()
            for col in range(1, self.patient_page.table_widget.table.columnCount())
        ]

        appointments = self.appointment_repo.get_appointment_by_patient_id(patient_id)

        fees_data = []

        for appt in appointments:
            ap = {
                "appointment": appt[2],     
                "consultation": appt[3],
                "medicines": [],
                "therapies": []
            }

            medicines = self.medicine_repo.get_medicine_by_appointment_id(appt[0])
            for med in medicines:
                ap["medicines"].append({
                    "name": med[2],
                    "fee": med[3]
                })

            therapies = self.therapy_repo.get_therapy_by_appointment_id(appt[0])
            for th in therapies:
                ap["therapies"].append({
                    "name": th[2],
                    "fee": th[3]
                })

            fees_data.append(ap)

        dialog = PatientDialog(self, patient_data, fees_data)

        if not dialog.exec():
            return

        raw_data = dialog.get_data()
        if not raw_data:
            QMessageBox.warning(self, "Error", "Patient name is required!")
            return
        
        try:
            patient = Patient(**raw_data)
        except ValidationError as e:
            QMessageBox.warning(
                self,
                "Validation Error",
                e.json(indent=2)
            )
            return


        self.patient_repo.update(patient_id, patient)

        # self.appointment_repo.delete_by_patient_id(patient_id)

        for appt in patient.fees.data:
            appt_id = self.appointment_repo.add(
                patient_id,
                appt.appointment,
                appt.consultation
            )

            for med in appt.medicines:
                self.medicine_repo.add(appt_id, med.name, med.fee)

            for th in appt.therapies:
                self.therapy_repo.add(appt_id, th.name, th.fee)

        self.load_patients()
        QMessageBox.information(self, "Success", "Patient updated successfully!")

    # def edit_patient(self):
    #     current_row = self.patient_page.table_widget.table.currentRow()
    #     print('current row: ', current_row)
    #     if current_row >= 0:
    #         item = self.patient_page.table_widget.table.item(current_row, 0)
    #         if item is None:
    #             QMessageBox.warning(self, "Error", "Invalid patient data!")
    #         print('item: ', item.text()) # type: ignore
    #         patient_id = int(item.text()) # type: ignore
    #         # patient_id = int(self.table.item(current_row, 0).text())
    #         patient_data = [self.patient_page.table_widget.table.item(current_row, col).text()  # type: ignore
    #                       for col in range(self.patient_page.table_widget.table.columnCount())]
    #         print('patient_data: ', patient_data)
    #         # fees data:  [{'appointment': 1, 'consultation': 500, 'medicines': [{'name': 'abc', 'fee': 100}, {'name': 'def', 'fee': 200}, {'name': 'ghi', 'fee': 300}], 'therapies': [{'name': 'Virechana', 'fee': 0}, {'name': 'Nasya', 'fee': 0}]}, {'appointment': 2, 'consultation': 250, 'medicines': [{'name': 'pqr', 'fee': 400}, {'name': 'stu', 'fee': 500}], 'therapies': [{'name': 'Vamana', 'fee': 0}, {'name': 'Virechana', 'fee': 0}, {'name': 'Basti', 'fee': 0}, {'name': 'Nasya', 'fee': 0}, {'name': 'Raktamokshana', 'fee': 0}]}]
    #         appointments = self.appointment_repo.get_appointment_by_patient_id(patient_id)
    #         print('edit appointments: ', appointments)
    #         fees_data = []
            
    #         for appt in appointments:
    #             ap = { 
    #             }
    #             ap['consultation'] = appt[3]
    #             ap['appointment'] = appt[2]
    #             ap['medicines'] = []
    #             ap['therapies'] = []
    #             print('appttt: ',appt)
    #             medicines = self.medicine_repo.get_medicine_by_appointment_id(appt[0])
    #             for med in medicines:
    #                 m = {
    #                     'name': med[2],
    #                     'fee': med[3]
    #                 }
    #                 ap['medicines'].append(m)
    #             print('medicines: ', medicines)
    #             therapies = self.therapy_repo.get_therapy_by_appointment_id(appt[0])
    #             for th in therapies:
    #                 t = {
    #                     'name': th[2],
    #                     'fee': th[3]
    #                 }
    #                 ap['therapies'].append(t)
    #             print('therapies: ', therapies)
    #             fees_data.append(ap)
    #         print('feeeee data: ', fees_data)
    #         dialog = PatientDialog(self, patient_data, fees_data)
            
    #         if dialog.exec():
    #             data = dialog.get_data()
    #             print('edited data: ', data)
    #             if data:
    #                 self.patient_repo.update(patient_id, data)
    #                 if (data['fees']['data']) != 0:
    #                     for appt in data['fees']['data']:
    #                         # appointment_data = (
    #                         #     patient_id,
    #                         #     appt['appointment'],
    #                         #     appt['consultation']
    #                         # )
    #                         appt_id = self.appointment_repo.add(patient_id, appt['appointment'], appt['consultation'])
    #                         for medicine in appt['medicines']:
    #                             self.medicine_repo.add(appt_id, medicine['name'], medicine['fee'])
                            
    #                         for therapy in appt['therapies']:
    #                             self.therapy_repo.add(appt_id, therapy['name'], therapy['fee'])
    #                 self.load_patients()
    #                 QMessageBox.information(self, "Success", "Patient updated successfully!")
    #             else:
    #                 QMessageBox.warning(self, "Error", "Patient name is required!")
    #     else:
    #         QMessageBox.warning(self, "Warning", "Please select a patient to edit!")
    
    def delete_patient(self):
        current_row = self.patient_page.table_widget.table.currentRow()
        if current_row >= 0:
            patient_id = int(self.patient_page.table_widget.table.item(current_row, 1).text()) # type: ignore
            patient_name = self.patient_page.table_widget.table.item(current_row, 2).text() # type: ignore
            
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete patient '{patient_name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.patient_repo.delete_patient(patient_id)
                self.load_patients()
                QMessageBox.information(self, "Success", "Patient deleted successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a patient to delete!")
    
    def search_patients(self):
        criteria = self.patient_page.search_layout.search_criteria.currentText()
        value = self.patient_page.search_layout.search_input.text()
        
        if value:
            search_service = PatientSearchService()
            query, params = search_service.build_query(criteria, value)
            patients = self.patient_repo.execute_query(query, params)
            # patients = self.patient_repo.search_patients(criteria, value)
            row_count = len(patients)

            self.populate_table(patients)
            self.patient_page.btn_layout.row_count_lable.setText(f"Total: {row_count}")
        else:
            self.load_patients()

def main():
    app = QApplication(sys.argv)
    window = PatientManagementSystem()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()