from PySide6.QtWidgets import QMessageBox

def show_warning(message):
    msg = QMessageBox()
    msg.setWindowTitle("warning")
    msg.setText(message)
    msg.exec_()
