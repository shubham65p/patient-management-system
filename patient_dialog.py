from PySide6.QtWidgets import (
    QDialog, QLineEdit, QSpinBox, QComboBox, QDateEdit, QTextEdit,
    QPushButton, QFormLayout, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QCheckBox, QGridLayout, QWidget, QMessageBox, QToolTip
)
from PySide6.QtCore import QDate
from button.custom_button import CustomButton
from charges.fees_dialog import FeesDialog
from charges.fees_summary_widget import FeesSummaryWidget
from PySide6.QtGui import QGuiApplication

from PySide6.QtGui import QIntValidator
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression



class PatientDialog(QDialog):
    def __init__(self, parent=None, patient_data=None, previous_fee_data=None):
        super().__init__(parent)
        self.patient_data = patient_data
        self.previous_fee_data = previous_fee_data
        print('self.patientdata: ', self.patient_data)
        self.setWindowTitle("Add Patient" if not patient_data else "Edit Patient")
        self.setMinimumWidth(700)
        self.setup_ui()

        self.move_to_top()
        if patient_data:
            self.populate_data()

    
    def accept(self):
        data = self.get_data()
        phone = data["phone"]
        name = data["name"]

        if len(phone) < 10:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Phone number should be of 10 digits"
            )
            return  # 🚫 dialog stays open
        if len(name) < 1:
             QMessageBox.warning(
                self,
                "Validation Error",
                "Please enter name"
            )
             return

        super().accept() 
        
        
    
    def move_to_top(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = screen.top() + 20  # padding from top
        self.move(x, y)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # ================= Patient Info =================
        patient_group = QGroupBox("Patient Information")
        patient_layout = QGridLayout()

        self.name_input = QLineEdit()
        self.age_input = QSpinBox()
        self.age_input.setRange(1, 150)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])

        self.dob_input = QDateEdit(QDate.currentDate())
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("yyyy-MM-dd")

        self.phone_input = QLineEdit()
        regex = QRegularExpression(r"\d{0,10}")
        validator = QRegularExpressionValidator(regex, self)
        self.phone_input.setValidator(validator)
        self.phone_input.setMaxLength(10)
        self.phone_input.setPlaceholderText("Only numbers allowed")



        patient_layout.addWidget(QLabel("Name"), 0, 0)
        patient_layout.addWidget(self.name_input, 0, 1)
        patient_layout.addWidget(QLabel("Age"), 0, 2)
        patient_layout.addWidget(self.age_input, 0, 3)

        patient_layout.addWidget(QLabel("Gender"), 1, 0)
        patient_layout.addWidget(self.gender_input, 1, 1)
        patient_layout.addWidget(QLabel("Date of Birth"), 1, 2)
        patient_layout.addWidget(self.dob_input, 1, 3)

        patient_layout.addWidget(QLabel("Phone"), 2, 0)
        patient_layout.addWidget(self.phone_input, 2, 1, 1, 3)

        patient_group.setLayout(patient_layout)
        main_layout.addWidget(patient_group)

        layout = QHBoxLayout()
        # ================= Address =================
        self.address_input = QTextEdit()
        self.address_input.setFixedHeight(70)

        
        
        address_group = QGroupBox("Address")
        address_layout = QVBoxLayout()
        address_layout.addWidget(self.address_input)
        address_group.setLayout(address_layout)
        # main_layout.addWidget(address_group)
        layout.addWidget(address_group)

        # ================= Appointment =================
        appointment_group = QGroupBox("Appointment Details")
        appointment_layout = QGridLayout()

        self.first_appointment_input = QDateEdit(QDate.currentDate())
        self.first_appointment_input.setCalendarPopup(True)
        self.first_appointment_input.setDisplayFormat("yyyy-MM-dd")

        self.followup_date_input = QDateEdit(QDate.currentDate().addDays(7))
        self.followup_date_input.setCalendarPopup(True)
        self.followup_date_input.setDisplayFormat("yyyy-MM-dd")

        self.total_followups_input = QSpinBox()
        self.total_followups_input.setRange(0, 999)

        appointment_layout.addWidget(QLabel("1st Appointment"), 0, 0)
        appointment_layout.addWidget(self.first_appointment_input, 0, 1)
        appointment_layout.addWidget(QLabel("Follow-up Date"), 0, 2)
        appointment_layout.addWidget(self.followup_date_input, 0, 3)

        appointment_layout.addWidget(QLabel("Total Follow-ups"), 1, 0)
        appointment_layout.addWidget(self.total_followups_input, 1, 1)

        appointment_group.setLayout(appointment_layout)
        # main_layout.addWidget(appointment_group)
        layout.addWidget(appointment_group)

        main_layout.addLayout(layout)

        # ================= Complaint =================
        self.major_complain_input = QTextEdit()
        self.major_complain_input.setFixedHeight(90)

        complain_group = QGroupBox("Major Complaint")
        complain_layout = QVBoxLayout()
        complain_layout.addWidget(self.major_complain_input)
        complain_group.setLayout(complain_layout)
        main_layout.addWidget(complain_group)

        # ================= Charges =================
        # appt = self.appointments[0]
        # previous_appointment_group = QGroupBox(f"Appointment {appt[2]} \n {appt[3]}")
        # self.previous_fees_layout = QHBoxLayout()
        # self.previous_fees = QWidget()
        
        # self.previous_fees_layout.addWidget(QLabel(f"<b>Consultation fee: {appt[3]}</b>"))
        # self.previous_fees_layout.addWidget(QLabel(f"<b>Appointment {appt[2]} \n {appt[3]}</b>"))
        
        self.fees_summary_container = QVBoxLayout()
        self.fees_data = []
        self.previous_fee_summary = None
        if self.previous_fee_data:
            self.previous_fee_summary = FeesSummaryWidget(self.previous_fee_data)
            main_layout.addWidget(self.previous_fee_summary)
        total_appointments_till_now = 0
        if self.previous_fee_data:
            total_appointments_till_now = len(self.previous_fee_data)
        def open_fees_dialog():
            dialog = FeesDialog(total_appointments_till_now)
            if dialog.exec():
                self.fees_data = dialog.get_fees_data()
                # self.fees_data =  self.previous_fee_data + self.fees_data
                print('fees data: ', self.fees_data)
                # fees data:  [{'appointment': 1, 'consultation': 500, 'medicines': [{'name': 'abc', 'fee': 100}, {'name': 'def', 'fee': 200}, {'name': 'ghi', 'fee': 300}], 'therapies': [{'name': 'Virechana', 'fee': 0}, {'name': 'Nasya', 'fee': 0}]}, {'appointment': 2, 'consultation': 250, 'medicines': [{'name': 'pqr', 'fee': 400}, {'name': 'stu', 'fee': 500}], 'therapies': [{'name': 'Vamana', 'fee': 0}, {'name': 'Virechana', 'fee': 0}, {'name': 'Basti', 'fee': 0}, {'name': 'Nasya', 'fee': 0}, {'name': 'Raktamokshana', 'fee': 0}]}]
                # Clear old summary
                # while self.fees_summary_container.count():
                #     item = self.fees_summary_container.takeAt(0)
                #     if item.widget():
                #         item.widget().deleteLater()
                if self.previous_fee_summary:
                    main_layout.removeWidget(self.previous_fee_summary)
                    self.previous_fee_summary.deleteLater()
                    self.previous_fee_summary = None
                if self.previous_fee_data:
                    summary = FeesSummaryWidget(self.previous_fee_data + self.fees_data)
                else:
                    summary = FeesSummaryWidget(self.fees_data)
                self.fees_summary_container.addWidget(summary)
        add_fees = CustomButton("Add Fees", "#3498db")
        add_fees.clicked.connect(open_fees_dialog)
        # main_layout.addLayout(self.previous_fees_layout)
        main_layout.addLayout(self.fees_summary_container)
        main_layout.addWidget(add_fees)

        # charges_group = QGroupBox("Charges")
        # charges_layout = QGridLayout()

        # self.consultation_fee = QSpinBox()
        # self.consultation_fee.setMaximum(100000)

        # self.medicine_fee = QSpinBox()
        # self.medicine_fee.setMaximum(100000)

        # charges_layout.addWidget(QLabel("Consultation Fees"), 0, 0)
        # charges_layout.addWidget(self.consultation_fee, 0, 1)
        # charges_layout.addWidget(QLabel("Medicinal Fees"), 1, 0)
        # charges_layout.addWidget(self.medicine_fee, 1, 1)

        # # Panchakarma Therapies
        # therapy_group = QGroupBox("Panchakarma Therapies")
        # therapy_layout = QVBoxLayout()

        # self.therapy_checks = []
        # therapies = [
        #     "Vamana", "Virechana", "Basti",
        #     "Nasya", "Raktamokshana", "Shirodhara"
        # ]

        # for therapy in therapies:
        #     cb = QCheckBox(therapy)
        #     self.therapy_checks.append(cb)
        #     therapy_layout.addWidget(cb)

        # therapy_group.setLayout(therapy_layout)

        # charges_layout.addWidget(therapy_group, 0, 2, 2, 2)
        # charges_group.setLayout(charges_layout)
        # main_layout.addWidget(charges_group)

        # ================= Buttons =================
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        main_layout.addLayout(btn_layout)
    
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
        return {
            "name": self.name_input.text(),
            "age": self.age_input.value(),
            "gender": self.gender_input.currentText(),
            "dob": self.dob_input.date().toString("yyyy-MM-dd"),
            "phone": self.phone_input.text(),
            "address": self.address_input.toPlainText(),
            "first_appointment": self.first_appointment_input.date().toString("yyyy-MM-dd"),
            "followup_date": self.followup_date_input.date().toString("yyyy-MM-dd"),
            "total_followups": self.total_followups_input.value(),
            "major_complain": self.major_complain_input.toPlainText(),
            "fees": {
                "data": self.fees_data
            }
        #     "consultation_fee": self.consultation_fee.value(),
        #     "medicine_fee": self.medicine_fee.value(),
        #     "therapies": [cb.text() for cb in self.therapy_checks if cb.isChecked()]
        }





















# from PySide6.QtWidgets import (
#     QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
#     QLineEdit, QSpinBox, QComboBox, QDateEdit, QTextEdit,
#     QPushButton, QLabel
# )
# from PySide6.QtCore import QDate, Qt



# class PatientDialog(QDialog):
#     def __init__(self, parent=None, patient_data=None):
#         super().__init__(parent)
#         self.patient_data = patient_data

#         self.setWindowTitle("Add Patient" if not patient_data else "Edit Patient")
#         self.setMinimumWidth(640)

#         self.setup_ui()

#         if patient_data:
#             self.populate_data()

#     def setup_ui(self):
#         main_layout = QVBoxLayout(self)
#         main_layout.setSpacing(16)

#         # ---------------- Personal Info ----------------
#         personal_group = QGroupBox("Personal Information")
#         personal_layout = QFormLayout()
#         personal_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

#         self.name_input = QLineEdit()
#         self.name_input.setPlaceholderText("Enter full name")

#         self.age_input = QSpinBox()
#         self.age_input.setRange(0, 150)

#         self.gender_input = QComboBox()
#         self.gender_input.addItems(["Male", "Female", "Other"])

#         self.dob_input = QDateEdit()
#         self.dob_input.setCalendarPopup(True)
#         self.dob_input.setDisplayFormat("yyyy-MM-dd")
#         self.dob_input.setDate(QDate.currentDate())

#         personal_layout.addRow("Name", self.name_input)
#         personal_layout.addRow("Age", self.age_input)
#         personal_layout.addRow("Gender", self.gender_input)
#         personal_layout.addRow("Date of Birth", self.dob_input)

#         personal_group.setLayout(personal_layout)

#         # ---------------- Contact Info ----------------
#         contact_group = QGroupBox("Contact Information")
#         contact_layout = QFormLayout()

#         self.phone_input = QLineEdit()
#         self.phone_input.setPlaceholderText("Phone number")

#         self.address_input = QTextEdit()
#         self.address_input.setFixedHeight(70)

#         contact_layout.addRow("Phone", self.phone_input)
#         contact_layout.addRow("Address", self.address_input)

#         contact_group.setLayout(contact_layout)

#         # ---------------- Medical Info ----------------
#         medical_group = QGroupBox("Medical Information")
#         medical_layout = QFormLayout()

#         self.first_appointment_input = QDateEdit()
#         self.first_appointment_input.setCalendarPopup(True)
#         self.first_appointment_input.setDisplayFormat("yyyy-MM-dd")
#         self.first_appointment_input.setDate(QDate.currentDate())

#         self.major_complain_input = QTextEdit()
#         self.major_complain_input.setFixedHeight(80)

#         self.followup_date_input = QDateEdit()
#         self.followup_date_input.setCalendarPopup(True)
#         self.followup_date_input.setDisplayFormat("yyyy-MM-dd")
#         self.followup_date_input.setDate(QDate.currentDate().addDays(7))

#         self.total_followups_input = QSpinBox()
#         self.total_followups_input.setRange(0, 999)

#         medical_layout.addRow("1st Appointment", self.first_appointment_input)
#         medical_layout.addRow("Major Complain", self.major_complain_input)
#         medical_layout.addRow("Follow-up Date", self.followup_date_input)
#         medical_layout.addRow("Total Follow-ups", self.total_followups_input)

#         medical_group.setLayout(medical_layout)

#         # ---------------- Buttons ----------------
#         btn_layout = QHBoxLayout()
#         btn_layout.addStretch()

#         cancel_btn = QPushButton("Cancel")
#         save_btn = QPushButton("Save")

#         cancel_btn.clicked.connect(self.reject)
#         save_btn.clicked.connect(self.accept)

#         cancel_btn.setObjectName("secondary")
#         save_btn.setObjectName("primary")

#         btn_layout.addWidget(cancel_btn)
#         btn_layout.addWidget(save_btn)

#         # ---------------- Assemble ----------------
#         main_layout.addWidget(personal_group)
#         main_layout.addWidget(contact_group)
#         main_layout.addWidget(medical_group)
#         main_layout.addLayout(btn_layout)

#         self.setStyleSheet(self.dialog_style())

#     def dialog_style(self):
#         return """
#         QDialog {
#             background-color: #f8fafc;
#         }
#         QGroupBox {
#             font-weight: 600;
#             border: 1px solid #e5e7eb;
#             border-radius: 8px;
#             margin-top: 8px;
#             padding: 10px;
#         }
#         QGroupBox::title {
#             subcontrol-origin: margin;
#             left: 12px;
#             padding: 0 6px;
#         }
#         QLineEdit, QSpinBox, QComboBox, QDateEdit, QTextEdit {
#             padding: 6px;
#             border: 1px solid #d1d5db;
#             border-radius: 6px;
#             background: white;
#         }
#         QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {
#             border: 1px solid #2563eb;
#         }
#         QPushButton {
#             padding: 8px 18px;
#             border-radius: 6px;
#             font-weight: 600;
#         }
#         QPushButton#primary {
#             background-color: #2563eb;
#             color: white;
#         }
#         QPushButton#primary:hover {
#             background-color: #1d4ed8;
#         }
#         QPushButton#secondary {
#             background-color: #e5e7eb;
#         }
#         QPushButton#secondary:hover {
#             background-color: #d1d5db;
#         }
#         """

#     def populate_data(self):
#         # (Keep your existing populate logic)
#         pass

#     def get_data(self):
#         return (
#             self.name_input.text(),
#             self.age_input.value(),
#             self.gender_input.currentText(),
#             self.dob_input.date().toString("yyyy-MM-dd"),
#             self.phone_input.text(),
#             self.address_input.toPlainText(),
#             self.first_appointment_input.date().toString("yyyy-MM-dd"),
#             self.major_complain_input.toPlainText(),
#             self.followup_date_input.date().toString("yyyy-MM-dd"),
#             self.total_followups_input.value()
#         )








# from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
#                                QHBoxLayout, QTableWidget, QTableWidgetItem, 
#                                QPushButton, QLineEdit, QLabel, QDialog, 
#                                QFormLayout, QComboBox, QDateEdit, QTextEdit,
#                                QMessageBox, QHeaderView, QSpinBox, QAbstractItemView)
# from PySide6.QtCore import QDate


# class PatientDialog(QDialog):
#     def __init__(self, parent=None, patient_data=None):
#         super().__init__(parent)
#         self.patient_data = patient_data
#         self.setWindowTitle("Add Patient" if not patient_data else "Edit Patient")
#         self.setMinimumWidth(500)
#         self.setup_ui()
        
#         if patient_data:
#             self.populate_data()
    
#     def setup_ui(self):
#         layout = QFormLayout()
        
#         self.name_input = QLineEdit()
#         self.age_input = QSpinBox()
#         self.age_input.setRange(0, 150)
        
#         self.gender_input = QComboBox()
#         self.gender_input.addItems(["Male", "Female", "Other"])
        
#         self.dob_input = QDateEdit()
#         self.dob_input.setCalendarPopup(True)
#         self.dob_input.setDisplayFormat("yyyy-MM-dd")

#         self.dob_input.setDate(QDate.currentDate())
        
#         self.phone_input = QLineEdit()
#         self.address_input = QTextEdit()
#         self.address_input.setMaximumHeight(80)
        
#         self.first_appointment_input = QDateEdit()
#         self.first_appointment_input.setCalendarPopup(True)
#         self.first_appointment_input.setDisplayFormat("yyyy-MM-dd")
#         self.first_appointment_input.setDate(QDate.currentDate())
        
#         self.major_complain_input = QTextEdit()
#         self.major_complain_input.setMaximumHeight(100)
        
#         self.followup_date_input = QDateEdit()
#         self.followup_date_input.setCalendarPopup(True)
#         self.followup_date_input.setDisplayFormat("yyyy-MM-dd")

#         self.followup_date_input.setDate(QDate.currentDate().addDays(7))
        
#         self.total_followups_input = QSpinBox()
#         self.total_followups_input.setRange(0, 999)
        
#         layout.addRow("Name:", self.name_input)
#         layout.addRow("Age:", self.age_input)
#         layout.addRow("Gender:", self.gender_input)
#         layout.addRow("Date of Birth:", self.dob_input)
#         layout.addRow("Phone Number:", self.phone_input)
#         layout.addRow("Address:", self.address_input)
#         layout.addRow("Date of 1st Appointment:", self.first_appointment_input)
#         layout.addRow("Major Complain:", self.major_complain_input)
#         layout.addRow("Follow-up Date:", self.followup_date_input)
#         layout.addRow("Total No. of Follow-ups:", self.total_followups_input)
        
#         btn_layout = QHBoxLayout()
#         save_btn = QPushButton("Save")
#         cancel_btn = QPushButton("Cancel")
        
#         save_btn.clicked.connect(self.accept)
#         cancel_btn.clicked.connect(self.reject)
        
#         btn_layout.addWidget(save_btn)
#         btn_layout.addWidget(cancel_btn)
        
#         layout.addRow(btn_layout)
#         self.setLayout(layout)
    
    # def populate_data(self):
    #     if self.patient_data:
    #         self.name_input.setText(self.patient_data[1])
    #         self.age_input.setValue(int(self.patient_data[2]) or 0)
    #         self.gender_input.setCurrentText(self.patient_data[3] or "Male")
            
    #         if self.patient_data[4]:
    #             self.dob_input.setDate(QDate.fromString(self.patient_data[4], "yyyy-MM-dd"))
            
    #         self.phone_input.setText(self.patient_data[5] or "")
    #         self.address_input.setText(self.patient_data[6] or "")
            
    #         if self.patient_data[7]:
    #             self.first_appointment_input.setDate(QDate.fromString(self.patient_data[7], "yyyy-MM-dd"))
            
    #         self.major_complain_input.setText(self.patient_data[8] or "")
            
    #         if self.patient_data[9]:
    #             self.followup_date_input.setDate(QDate.fromString(self.patient_data[9], "yyyy-MM-dd"))
    #         if self.patient_data[10]:
    #             self.total_followups_input.setValue(int(self.patient_data[10]) or 0)
    
#     def get_data(self):
#         return (
#             self.name_input.text(),
#             self.age_input.value(),
#             self.gender_input.currentText(),
#             self.dob_input.date().toString("yyyy-MM-dd"),
#             self.phone_input.text(),
#             self.address_input.toPlainText(),
#             self.first_appointment_input.date().toString("yyyy-MM-dd"),
#             self.major_complain_input.toPlainText(),
#             self.followup_date_input.date().toString("yyyy-MM-dd"),
#             self.total_followups_input.value()
#         )




