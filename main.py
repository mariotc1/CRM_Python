import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from welcome_window import WelcomeWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyle("Fusion")

    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec_())