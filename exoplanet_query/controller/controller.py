from view.view import MainWindow, SecondaryWindow
from model.model import ExoplanetModel
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
import plot_logic.plot as plot
import database.data_loader as db_loader

class Controller:
    def __init__(self):
        db_loader.create_database()
        db_loader.load_exoplanet_data()

        self.model = ExoplanetModel()
        self.main_window = MainWindow()
        self.secondary_window = SecondaryWindow()
        
        self.setup_connections()
        self.populate_search_boxes()

    def setup_connections(self):
        self.main_window.search_button.clicked.connect(self.search)
        self.main_window.clear_button.clicked.connect(self.clear)
        self.main_window.open_button.clicked.connect(self.open_secondary_window)
        self.secondary_window.generate_plot_button.clicked.connect(self.generate_plot)
        
    def populate_search_boxes(self):
        self.main_window.populate_combo_box(self.main_window.name_search, self.model.get_distinct_names())
        self.main_window.populate_combo_box(self.main_window.year_search, self.model.get_distinct_years())
        self.main_window.populate_combo_box(self.main_window.method_search, self.model.get_distinct_methods())
        self.main_window.populate_combo_box(self.main_window.host_search, self.model.get_distinct_hosts())
        self.main_window.populate_combo_box(self.main_window.facility_search, self.model.get_distinct_facilities())

    def search(self):
        name = self.main_window.name_search.currentText()
        year = self.main_window.year_search.currentText()
        method = self.main_window.method_search.currentText()
        host = self.main_window.host_search.currentText()
        facility = self.main_window.facility_search.currentText()

        # Check if any search parameters are provided
        if not any([name, year, method, host, facility]):
            #raise NoFieldsSelectedError("No search fields selected")
            QMessageBox.warning(self.main_window, "Error", "Please select at least one search field.")
            return
        
        try:
            results = self.model.search_exoplanets(name, year, method, host, facility)
            self.main_window.output_table.setRowCount(len(results))
            for row_num, row_data in enumerate(results):
                for col_num, col_data in enumerate(row_data):
                    self.main_window.output_table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
            self.main_window.output_table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self.main_window, "Error", str(e))
        
    # clear table/selected queries
    def clear(self):
        self.main_window.output_table.clearContents()

        self.main_window.name_search.clearEditText()
        self.main_window.year_search.clearEditText()
        self.main_window.method_search.clearEditText()
        self.main_window.host_search.clearEditText()
        self.main_window.facility_search.clearEditText()

    def open_secondary_window(self):
        self.secondary_window.show()

    def generate_plot(self):
        plot.generate_plot(self.secondary_window, self.secondary_window.column_names)