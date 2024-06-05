from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox,
    QCompleter, QMessageBox
)
from PyQt6.QtCore import Qt
import sqlite3
import query.processor as query
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
)
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

class SecondaryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exoplanet Data Visualization")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        
        self.figure = plt.figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Add navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        
        self.generate_plot()

    def generate_plot(self):
        try:
            conn = sqlite3.connect('exoplanets.db')
            c = conn.cursor()
            
            # Retrieve data from the database
            # Some don't have all data fields, exclude those that are empty
            c.execute('SELECT pl_rade, pl_masse FROM exoplanets WHERE pl_rade != "" AND pl_masse != ""')                  
            data = c.fetchall()
            
            # Close the database connection
            conn.close()
            
            # Extract radius and mass data
            radii = [row[0] for row in data]
            masses = [row[1] for row in data]
            
            # Clear the previous plot
            self.figure.clear()
            
            # Create the scatter plot on the current figure
            ax = self.figure.add_subplot(111)
            ax.scatter(radii, masses, alpha=0.5)
            ax.set_title("Exoplanet Radius vs Mass")
            ax.set_xlabel("Radius (Earth radii)")
            ax.set_ylabel("Mass (Earth masses)")
            ax.grid(True)

            # Add trend line (linear regression)
            slope, intercept, r_value, p_value, std_err = stats.linregress(radii, masses)
            trend_line = f"y = {slope:.2f}x + {intercept:.2f}\nR-squared = {r_value**2:.2f}"
            ax.plot(np.array(radii), slope*np.array(radii) + intercept, color='red', label=trend_line)
            ax.legend()

            # Redraw canvas with updated plot
            self.canvas.draw() 
            
            
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", "Failed to retrieve data from the database.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NASA Exoplanet Query")
        self.setGeometry(100, 100, 1200, 900)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        
        self.setup_ui()
        self.populate_search_boxes()

        open_button = QPushButton("Open Plot")
        open_button.clicked.connect(self.open_secondary_window)
        layout.addWidget(open_button)

    def open_secondary_window(self):
        self.secondary_window = SecondaryWindow()
        self.secondary_window.show()
        
    def setup_ui(self):
        label = QLabel("Welcome to NASA Exoplanet Query")
        self.central_widget.layout().addWidget(label)
        
        # Search boxes with combo boxes and labels
        search_layout = QVBoxLayout()
        
        year_layout = QHBoxLayout()
        year_label = QLabel("Year of Discovery:")
        self.year_search = QComboBox()
        self.year_search.setEditable(True)
        self.year_search.setPlaceholderText("Select or type year")
        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_search)
        
        method_layout = QHBoxLayout()
        method_label = QLabel("Discovery Method:")
        self.method_search = QComboBox()
        self.method_search.setEditable(True)
        self.method_search.setPlaceholderText("Select or type method")
        method_layout.addWidget(method_label)
        method_layout.addWidget(self.method_search)
        
        host_layout = QHBoxLayout()
        host_label = QLabel("Host Name:")
        self.host_search = QComboBox()
        self.host_search.setEditable(True)
        self.host_search.setPlaceholderText("Select or type host")
        host_layout.addWidget(host_label)
        host_layout.addWidget(self.host_search)
        
        facility_layout = QHBoxLayout()
        facility_label = QLabel("Discovery Facility:")
        self.facility_search = QComboBox()
        self.facility_search.setEditable(True)
        self.facility_search.setPlaceholderText("Select or type facility")
        facility_layout.addWidget(facility_label)
        facility_layout.addWidget(self.facility_search)
        
        search_layout.addLayout(year_layout)
        search_layout.addLayout(method_layout)
        search_layout.addLayout(host_layout)
        search_layout.addLayout(facility_layout)
        
        self.central_widget.layout().addLayout(search_layout)
        
        # Search and Clear buttons
        button_layout = QHBoxLayout()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        button_layout.addWidget(search_button)
        
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear)
        button_layout.addWidget(clear_button)
        
        self.central_widget.layout().addLayout(button_layout)
        
        # Output
        self.output_table = QTableWidget()
        self.output_table.setColumnCount(5)  # Adjust column count as needed
        self.output_table.setHorizontalHeaderLabels(["Planet Name", "Year of Discovery", "Discovery Method", "Host Name", "Discovery Facility"])  # Adjust headers
        self.central_widget.layout().addWidget(self.output_table)
        self.output_table.setSortingEnabled(True)
        
    def populate_search_boxes(self):
        try:
            conn = sqlite3.connect('exoplanets.db')
            c = conn.cursor()
            
            # Populate year search box
            c.execute('SELECT DISTINCT disc_year FROM exoplanets ORDER BY disc_year ASC')  # Adjust query to get distinct years
            years = [str(year[0]) for year in c.fetchall()]
            self.populate_combo_box(self.year_search, years)
            
            # Populate method search box
            c.execute('SELECT DISTINCT discoverymethod FROM exoplanets ORDER BY discoverymethod ASC')
            methods = [method[0] for method in c.fetchall()]
            self.populate_combo_box(self.method_search, methods)
            
            # Populate host search box
            c.execute('SELECT DISTINCT hostname FROM exoplanets ORDER BY hostname ASC')
            hosts = [host[0] for host in c.fetchall()]
            self.populate_combo_box(self.host_search, hosts)
            
            # Populate facility search box
            c.execute('SELECT DISTINCT disc_facility FROM exoplanets ORDER BY disc_facility ASC')
            facilities = [facility[0] for facility in c.fetchall()]
            self.populate_combo_box(self.facility_search, facilities)
            
            conn.close()
        except sqlite3.Error as e:
            print("SQLite error:", e)

    def populate_combo_box(self, combobox, items):
        combobox.addItems(items)
        completer = QCompleter(items)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        combobox.setCompleter(completer)

    def search(self):
        year = self.year_search.currentText()
        method = self.method_search.currentText()
        host = self.host_search.currentText()
        facility = self.facility_search.currentText()
        
        try:
            results = query.search(year, method, host, facility)
        except query.NoFieldsSelectedError:
            QMessageBox.warning(self, "Error", "Please select at least one search field.")
            return
        
        self.output_table.setRowCount(len(results))
        
        for row_num, row_data in enumerate(results):
            for col_num, col_data in enumerate(row_data):
                self.output_table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
                    
        # Auto-size columns to fit the content
        self.output_table.resizeColumnsToContents()
        
        if not results:
            print("No matching exoplanets found.")
        
    def clear(self):
        self.output_table.clearContents()
        