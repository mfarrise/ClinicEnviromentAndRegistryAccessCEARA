                                                ################################################
                                                #      setting things for CIN RISK Window      #
                                                ################################################


from nephrology_equations_module import calculate_eGFR
from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QLabel, QComboBox, QWidget, QPushButton

class ContrastRiskSubWindow(QWidget):
    def __init__(self):
        super().__init__()

        CINLayout = QGridLayout(self)
        self.setLayout(CINLayout)
