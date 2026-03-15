from PySide6.QtWidgets import QWidget, QGridLayout, QTextEdit


class OldHistoryViewer(QWidget):
    def __init__(self, name,html):
        super().__init__()
        self.setStyleSheet("""
                
                QTextEdit {
                    font-size: 12pt;
                }
                """)
        self.name=name
        self.html=html
        self.setWindowTitle(self.name+" Previous History")
        self.layout=QGridLayout()
        self.setLayout(self.layout)
        self.setGeometry(600,600,800,800)
        self.viewer=QTextEdit()
        self.layout.addWidget(self.viewer)
        self.viewer.setReadOnly(True)
        self.viewer.setHtml(self.html)


