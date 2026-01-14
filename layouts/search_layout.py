from PySide6.QtWidgets import (QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton)
from button.custom_button import CustomButton
from config import config
class SearchLayout:
    ALLOWED_COLUMNS = config['ALLOWED_COLUMNS']

    def __init__(self) -> None:
        self.layout = QHBoxLayout()
        self.layout.addWidget(QLabel('Search by:'))

        self.search_criteria = QComboBox()
        self.search_criteria.addItems(self.ALLOWED_COLUMNS)
        self.search_criteria.setFixedHeight(38)
        
        self.layout.addWidget(self.search_criteria)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.setFixedHeight(38)
        
        self.layout.addWidget(self.search_input)

        self.search_btn = CustomButton("Search", "#5F9598")
        self.layout.addWidget(self.search_btn)

        self.clear_btn = CustomButton("Show All", "#5F9598")
        self.layout.addWidget(self.clear_btn)



