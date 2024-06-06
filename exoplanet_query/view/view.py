from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton,
    QTableWidget, QHBoxLayout, QComboBox, QCompleter, QMessageBox, QHeaderView )
import sqlite3

from PyQt6.QtCore import Qt
import pyqtgraph as pg

class MainWindow(QMainWindow):
    """
    Main window for the NASA Exoplanet Query application.

    This window provides the user interface for querying exoplanet data. It allows users
    to search for exoplanets based on various criteria, such as planet name, year of discovery,
    discovery method, host name, and discovery facility. Additionally, users can visualize
    the data using the provided plot functionality.

    Public Methods:
        - __init__: Initialize the main window.
        - setup_ui: Set up the user interface of the main window.
        - create_search_box: Create a search box using a QLabel and QComboBox.
        - populate_combo_box: Populate the provided combobox with the provided items.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NASA Exoplanet Query")
        self.setGeometry(100, 100, 1200, 900)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        
        self.setup_ui()

        # add "open plot" button to bottom of window
        open_button = QPushButton("Open Plot")
        layout.addWidget(open_button)
        self.open_button = open_button

    def setup_ui(self):
        """
        setup_ui initializes the user interface of the main window
        """
        search_layout = QVBoxLayout()

        self.name_search, name_layout = self.create_search_box("Planet Name:")
        self.year_search, year_layout = self.create_search_box("Year of Discovery:")
        self.method_search, method_layout = self.create_search_box("Discovery Method:")
        self.host_search, host_layout = self.create_search_box("Host Name:")
        self.facility_search, facility_layout = self.create_search_box("Discovery Facility:")
        
        search_layout.addLayout(name_layout)
        search_layout.addLayout(year_layout)
        search_layout.addLayout(method_layout)
        search_layout.addLayout(host_layout)
        search_layout.addLayout(facility_layout)
        
        self.central_widget.layout().addLayout(search_layout)
        
        button_layout = QHBoxLayout()
        search_button = QPushButton("Search")
        clear_button = QPushButton("Clear")

        button_layout.addWidget(search_button)
        button_layout.addWidget(clear_button)
        
        self.central_widget.layout().addLayout(button_layout)
        
        self.output_table = QTableWidget()
        self.output_table.setColumnCount(5)
        self.output_table.setHorizontalHeaderLabels(["Planet Name", "Year of Discovery", "Discovery Method", "Host Name", "Discovery Facility"])
        
        header = self.output_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.central_widget.layout().addWidget(self.output_table)
        self.output_table.setSortingEnabled(True)
        
        self.output_table.resizeColumnsToContents()
        
        self.search_button = search_button
        self.clear_button = clear_button

    def create_search_box(self, label_text):
        """
        create_search_box creates a search box using a QLabel and QComboBox.

        Args:
            label_text - The text to display in the QLabel.

        Returns:
            tuple: A tuple containing the created QComboBox and its layout (QHBoxLayout).
        """
        layout = QHBoxLayout()
        label = QLabel(label_text)
        combo_box = QComboBox()
        combo_box.setEditable(True)
        combo_box.setPlaceholderText(f"Select or type {label_text.lower()}")
        layout.addWidget(label)
        layout.addWidget(combo_box)
        return combo_box, layout

    def populate_combo_box(self, combobox, items):
        """
        Populate the provided combobox with the provided items.

        Args:
            combobox (QComboBox): The search combobox to populate.
            items (list): Items to populate the search box with.
        """
        combobox.addItems(items)
        completer = QCompleter(items)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        combobox.setCompleter(completer)

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
        """
        Set up the user interface of the main window
        """
        axis_layout = QHBoxLayout()
        
        self.x_axis_label = QLabel("X-Axis:")
        self.x_axis_combo = QComboBox()
        axis_layout.addWidget(self.x_axis_label)
        axis_layout.addWidget(self.x_axis_combo)
        
        self.y_axis_label = QLabel("Y-Axis:")
        self.y_axis_combo = QComboBox()
        axis_layout.addWidget(self.y_axis_label)
        axis_layout.addWidget(self.y_axis_combo)
        
        self.central_widget.layout().addLayout(axis_layout)
        
        generate_plot_button = QPushButton("Generate Plot")
        self.central_widget.layout().addWidget(generate_plot_button)
        
        self.generate_plot_button = generate_plot_button

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
