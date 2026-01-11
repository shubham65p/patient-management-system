from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QPushButton, QCheckBox, QWidget
)

from charges.medicinal_row_widget import MedicineRowWidget


class AppointmentWidget(QGroupBox):
    def __init__(self, number):
        super().__init__(f"Appointment {number}")

        layout = QVBoxLayout(self)

        # Consultation
        consult_layout = QHBoxLayout()
        consult_layout.addWidget(QLabel("Consultation Fees"))
        self.consultation_fee = QSpinBox()
        self.consultation_fee.setMaximum(100000)
        consult_layout.addWidget(self.consultation_fee)
        consult_layout.addStretch()
        layout.addLayout(consult_layout)

        # Medicines
        self.medicine_container = QVBoxLayout()
        add_medicine_btn = QPushButton("➕ Add Medicine")
        add_medicine_btn.clicked.connect(self.add_medicine)

        layout.addWidget(QLabel("Medicines"))
        layout.addLayout(self.medicine_container)
        layout.addWidget(add_medicine_btn)

        # Panchakarma
        layout.addWidget(QLabel("Panchakarma Therapies"))
        self.therapy_container = QVBoxLayout()

        therapies = [
            "Vamana", "Virechan", "Basti", "Nasya",
            "Raktamokshan", "Abhyang",
            "Swedana", "Shirodhara", 
            "Kati Basti", "Janu Basti", "Hridya Basti", 
            "Manya Basti", "Merudand Basti", "Udvartana", 
            "Netra Tarapana", "Agnikarma", "Viddhakarma"
        ]

        self.therapy_checks = []

        for therapy in therapies:
            row = QHBoxLayout()
            cb = QCheckBox(therapy)
            fee = QSpinBox()
            fee.setMaximum(100000)
            delete_btn = QPushButton("❌")
            delete_btn.setFixedWidth(30)

            delete_btn.clicked.connect(
                lambda _, r=row: self.remove_row(r)
            )

            row.addWidget(cb)
            row.addWidget(fee)
            row.addWidget(delete_btn)

            self.therapy_container.addLayout(row)
            self.therapy_checks.append((cb, fee))

        layout.addLayout(self.therapy_container)

    def add_medicine(self):
        row = MedicineRowWidget(self.medicine_container)
        self.medicine_container.addWidget(row)

    def remove_row(self, row_layout):
        while row_layout.count():
            item = row_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def get_medicines(self):
        meds = []
        for i in range(self.medicine_container.count()):
            widget = self.medicine_container.itemAt(i).widget()
            if widget:
                meds.append({
                    "name": widget.name.text(),
                    "fee": widget.fee.value()
                })
        return meds


    def get_therapies(self):
        selected = []
        for cb, fee in self.therapy_checks:
            if cb.isChecked():
                selected.append({
                    "name": cb.text(),
                    "fee": fee.value()
                })
        return selected
