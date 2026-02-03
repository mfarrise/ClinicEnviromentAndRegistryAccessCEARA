import os
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QFileDialog


class Patient_Dash_Board(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Dashboard")
        Layout = QGridLayout(self)
        self.setLayout(Layout)

        fetch_path_btn = QPushButton(self)
        fetch_path_btn.setText("Fetch Path")
        Layout.addWidget(fetch_path_btn,1,1)
        fetch_path_btn.clicked.connect(self.open_path_dialog)


    def open_path_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            parent=None,
            caption="Select file",
            dir="",
            filter="All Files (*.*);;Word Files (*.docx);;PDF Files (*.pdf)"
        )