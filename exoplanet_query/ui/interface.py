from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox,
    QCompleter, QMessageBox
)
from PyQt6.QtCore import Qt
import sqlite3
import query.processor as query
import numpy as np
from scipy import stats
import pyqtgraph as pg

class SecondaryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exoplanet Data Visualization")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        
        self.setup_ui()

    def setup_ui(self):
        # Layout for dropdowns
        axis_layout = QHBoxLayout()
        
        # Dropdown for X-axis
        self.x_axis_label = QLabel("X-Axis:")
        self.x_axis_combo = QComboBox()
        axis_layout.addWidget(self.x_axis_label)
        axis_layout.addWidget(self.x_axis_combo)
        
        # Dropdown for Y-axis
        self.y_axis_label = QLabel("Y-Axis:")
        self.y_axis_combo = QComboBox()
        axis_layout.addWidget(self.y_axis_label)
        axis_layout.addWidget(self.y_axis_combo)
        
        # Add layout for dropdowns
        self.central_widget.layout().addLayout(axis_layout)
        
        # Button to generate plot
        generate_plot_button = QPushButton("Generate Plot")
        generate_plot_button.clicked.connect(self.generate_plot)
        self.central_widget.layout().addWidget(generate_plot_button)

        # Populate dropdowns
        self.populate_dropdowns()

    def populate_dropdowns(self):
        # Define a mapping of column names to user-friendly labels
        column_labels = {
            "pl_name": "Planet Name",
            "disc_year": "Discovery Year",
            "discoverymethod": "Discovery Method",
            "hostname": "Host Name",
            "disc_facility": "Discovery Facility",
            "sy_dist": "Distance from Earth",
            "pl_rade": "Radius (in R🜨)",
            "pl_masse": "Mass (in M🜨)",
            "pl_orbper": "Orbital Period (in days)",
            "st_rad": "Star Radius (in R☉)" ,
            "pl_eqt": "Temperature (in K)"
        }

        # Create a reverse mapping dictionary to map user-friendly labels back to column names
        self.column_names = {v: k for k, v in column_labels.items()}

        try:
            conn = sqlite3.connect('exoplanets.db')
            c = conn.cursor()
            
            # Get the list of columns from the exoplanets table
            c.execute("PRAGMA table_info(exoplanets)")
            columns = [column[1] for column in c.fetchall()]
            
            # Map column names to user-friendly labels
            user_friendly_columns = [column_labels.get(column, column) for column in columns]
            
            # Add user-friendly labels to dropdowns
            self.x_axis_combo.addItems(user_friendly_columns)
            self.y_axis_combo.addItems(user_friendly_columns)
            
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"SQLite error: {e}")

    def generate_plot(self):
        try:
            conn = sqlite3.connect('exoplanets.db')
            c = conn.cursor()
            
            # Retrieve data from the database based on selected columns
            x_column_label = self.x_axis_combo.currentText()
            y_column_label = self.y_axis_combo.currentText()
            
            # Retrieve the actual column names using the column_names dictionary
            x_column = self.column_names.get(x_column_label, x_column_label)
            y_column = self.column_names.get(y_column_label, y_column_label)
            
            c.execute(f'SELECT {x_column}, {y_column} FROM exoplanets WHERE {x_column} != "" AND {y_column} != ""')
            data = c.fetchall()
            
            # Close the database connection
            conn.close()
            
            # Extract x and y data
            x_data = np.array([row[0] for row in data])
            y_data = np.array([row[1] for row in data])
            
            # Clear the previous plot
            self.plot_widget.clear()
            
            # Bin and aggregate data
            bin_centers, bin_values = self.bin_and_aggregate_data(x_data, y_data)
            
            # Create the scatter plot
            self.plot_widget.plot(bin_centers, bin_values, symbol='o', symbolSize=5, pen=None)
            #self.plot_widget.setTitle("Exoplanet Data Visualization")
            self.plot_widget.setLabel('left', text=y_column_label)
            self.plot_widget.setLabel('bottom', text=x_column_label)
            self.plot_widget.showGrid(False, False)

            # Set minimum values for axes to zero
            #self.plot_widget.setXRange(0, np.max(x_data))
            #self.plot_widget.setYRange(0, np.max(y_data))

            # Add trend line (linear regression)
            slope, intercept, r_value, p_value, std_err = stats.linregress(x_data, y_data)
            trend_line_x = np.array([np.min(x_data), np.max(x_data)])
            trend_line_y = slope * trend_line_x + intercept
            self.plot_widget.plot(trend_line_x, trend_line_y, pen=pg.mkPen('r'), name="Trend Line")
            
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", "Failed to retrieve data from the database.")

    def bin_and_aggregate_data(self, x_data, y_data, num_bins=200):
        # Calculate bin edges
        bin_edges = np.linspace(np.min(x_data) - 1e-6, np.max(x_data) + 1e-6, num_bins + 1)
        bin_centers = (bin_edges[1:] + bin_edges[:-1]) / 2
        
        # Initialize arrays to store aggregated values
        bin_values = np.zeros_like(bin_centers)
        bin_counts = np.zeros_like(bin_centers)
        
        # Iterate over data points and assign them to bins
        for x, y in zip(x_data, y_data):
            bin_index = np.digitize(x, bin_edges) - 1
            bin_values[bin_index] += y
            bin_counts[bin_index] += 1
        
        # Calculate mean value for each bin
        bin_values = np.divide(bin_values, np.maximum(bin_counts, 1), out=np.zeros_like(bin_values), where=bin_counts!=0)
        
        return bin_centers, bin_values



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
        # Search boxes with combo boxes and labels
        search_layout = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_label = QLabel("Planet Name:")
        self.name_search = QComboBox()
        self.name_search.setEditable(True)
        self.name_search.setPlaceholderText("Select or type name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_search)
        
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
        
        search_layout.addLayout(name_layout)
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
        self.output_table.setColumnCount(5)
        self.output_table.setHorizontalHeaderLabels(["Planet Name", "Year of Discovery", "Discovery Method", "Host Name", "Discovery Facility"])
        self.central_widget.layout().addWidget(self.output_table)
        self.output_table.setSortingEnabled(True)

        # Auto-size columns to fit the content initially
        self.output_table.resizeColumnsToContents()

        
    def populate_search_boxes(self):
        try:
            conn = sqlite3.connect('exoplanets.db')
            c = conn.cursor()
            
            # Populate name search box
            c.execute('SELECT DISTINCT pl_name FROM exoplanets ORDER BY pl_name ASC')
            names = [names[0] for names in c.fetchall()]
            self.populate_combo_box(self.name_search, names)

            # Populate year search box
            c.execute('SELECT DISTINCT disc_year FROM exoplanets ORDER BY disc_year ASC')
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
        name = self.name_search.currentText()
        year = self.year_search.currentText()
        method = self.method_search.currentText()
        host = self.host_search.currentText()
        facility = self.facility_search.currentText()
        
        try:
            results = query.search(name, year, method, host, facility)
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