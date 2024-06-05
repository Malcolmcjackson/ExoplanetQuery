import data.loader as loader
import sys
from PyQt6.QtWidgets import QApplication
from ui.interface import MainWindow

# Create SQLite database and table
loader.create_database()

# Load exoplanet data into SQLite database
loader.load_exoplanet_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())