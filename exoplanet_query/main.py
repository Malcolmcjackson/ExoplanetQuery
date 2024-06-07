from PyQt6.QtWidgets import QApplication, QSplashScreen, QMessageBox
from controller.controller import Controller
import sys, PyQt6.QtCore, PyQt6.QtGui

from pyqtspinner.spinner import WaitingSpinner
from PyQt6.QtCore import QThread, pyqtSignal
from database.data_loader import load_exoplanet_data, create_database
import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtCore as QtCore
from PyQt6.QtCore import Qt as Qt

class DataLoaderThread(QThread):
    data_loaded = pyqtSignal()

    def run(self):
        create_database()
        load_exoplanet_data()
        self.data_loaded.emit()
        print("data loaded")

def show_main_window():
    controller = Controller()
    #controller.load_data_separate_thread()

    print("showing main window")
    main_window = controller.main_window
    main_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    #splash_pic = PyQt6.QtGui.QPixmap('exoplanet_query/test.jpg')
    splash_pixmap = PyQt6.QtGui.QPixmap(1200, 900)
    splash_pixmap.fill(PyQt6.QtGui.QColor(0, 0, 0))

    splash = QSplashScreen(splash_pixmap, PyQt6.QtCore.Qt.WindowType.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
    splash.setEnabled(False)

    splash.setGeometry(100, 100, 1200, 900)

    splash.show()
    splash.showMessage("<h1>Loading Exoplanet Data...</h1>", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.black)
    data_thread = DataLoaderThread()
      # Close splash screen when data is loaded
    data_thread.data_loaded.connect(splash.close)

    controller = Controller()
    main_window = controller.main_window

    # Show/activate main window when data is loaded
    data_thread.data_loaded.connect(main_window.show)
    data_thread.data_loaded.connect(main_window.activateWindow)

    data_thread.start()

    sys.exit(app.exec())