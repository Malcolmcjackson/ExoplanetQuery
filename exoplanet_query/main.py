from PyQt6.QtWidgets import QApplication, QSplashScreen
from controller.controller import Controller
import sys
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from database.data_loader import load_exoplanet_data, create_database

class DataLoaderThread(QThread):
    """
    QThread subclass to load exoplanet data in a separate thread.

    Signals:
        data_loaded: Emitted when data loading is complete.
    """
    data_loaded = pyqtSignal()

    def run(self):
        """
        Run the data loading process.

        This method creates the database, loads the exoplanet data, and emits
        the data_loaded signal upon completion.
        """
        create_database()
        load_exoplanet_data()
        self.data_loaded.emit()
        print("Data loaded")

def show_main_window(controller):
    """
    Show the main window of the application.

    Args:
        controller (Controller): The application's controller instance.
    """
    main_window = controller.main_window
    main_window.show()
    main_window.activateWindow()
    print("Showing main window")

if __name__ == "__main__":
    """
    Main entry point for the NASA Exoplanet Query application.

    This script initializes the PyQt application, displays a splash screen while
    loading data in a separate thread, and shows the main application window once
    the data is loaded.
    """
    app = QApplication(sys.argv)

    # Create splash screen
    splash_pixmap = QPixmap(1200, 900)
    splash_pixmap.fill(QColor(0, 0, 0))

    splash = QSplashScreen(splash_pixmap, Qt.WindowType.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
    splash.setEnabled(False)
    splash.setGeometry(100, 100, 1200, 900)
    splash.show()
    splash.showMessage("<h1>Loading Exoplanet Data...</h1>", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)

    # Set up data loading thread
    data_thread = DataLoaderThread()
    data_thread.data_loaded.connect(splash.close)

    controller = Controller()
    data_thread.data_loaded.connect(lambda: show_main_window(controller))

    data_thread.start()

    sys.exit(app.exec())
