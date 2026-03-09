import sqlite3

from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QListView, QPushButton
import sys


class PatientSearchNewPatientWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.model = None
        self.proxy=None
        self.setWindowTitle("patient_search_new_patient")
        self.setGeometry(300, 300, 300, 300)
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        #NOTE opening DB
        self.conn=sqlite3.connect("dummy_patients.db")

        self.search_label=QLabel("Search")
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("Type Patient name here")
        self.search_line_edit.returnPressed.connect(
            lambda: self.patient_selected(self.search_list_view.currentIndex())
        )
        self.search_list_view = QListView()
        self.setup_model()
        self.load_patients()

        self.search_line_edit.textChanged.connect(self.filter_patients)
        self.search_list_view.clicked.connect(self.patient_selected)
        self.search_list_view.setCurrentIndex(self.proxy.index(0, 0))







        #NOTE place widgets inside layout
        self.main_layout.addWidget(self.search_label,0,0)
        self.main_layout.addWidget(self.search_line_edit,1,0)
        self.main_layout.addWidget(self.search_list_view,2,0)

    def setup_model(self):
        self.model=QStandardItemModel()

        self.proxy=QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.search_list_view.setModel(self.proxy)

    def load_patients(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id,name FROM patients ORDER BY name")

        for pid,name in cursor.fetchall():
            item=QStandardItem(name)
            item.setData(pid,Qt.ItemDataRole.UserRole)
            self.model.appendRow(item)
    def filter_patients(self,text):
        self.proxy.setFilterFixedString(text)

    def patient_selected(self, index):
        source_index = self.proxy.mapToSource(index)

        item = self.model.itemFromIndex(source_index)

        patient_id = item.data(Qt.ItemDataRole.UserRole)

        print("Open Patient ID:", patient_id)

        # open PatientDashboard(patient_id)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PatientSearchNewPatientWidget()
    window.show()
    sys.exit(app.exec_())


