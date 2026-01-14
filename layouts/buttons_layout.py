from PySide6.QtWidgets import (QHBoxLayout, QLabel, QMessageBox, QTableWidgetItem, QWidget)
from PySide6.QtCore import Qt

from button.custom_button import CustomButton

class ButtonsLayout(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        layout = QHBoxLayout(self)
        self.add_btn = CustomButton("Add Patient", "#2F6690")
        layout.addWidget(self.add_btn)

        self.edit_btn = CustomButton("Edit Patient", "#2F6690")
        layout.addWidget(self.edit_btn)

        self.delete_btn = CustomButton("Delete Patient", "#2F6690")
        layout.addWidget(self.delete_btn)

        layout.addStretch()
        self.row_count_lable = QLabel("Total: 0")
        font = self.row_count_lable.font()
        font.setBold(True)
        self.row_count_lable.setFont(font)

        self.row_count_lable.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.row_count_lable)