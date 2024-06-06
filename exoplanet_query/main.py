from PyQt6.QtWidgets import QApplication
from controller.controller import Controller
import sys

def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
