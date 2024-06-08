from view.view import MainWindow, SecondaryWindow
from model.model import ExoplanetModel
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
import plot_logic.plot as plot
import database.data_loader as db_loader

class Controller:
    """
    Controller class to manage the interaction between the view and the model.

    This class initializes the database, sets up the main and secondary windows,
    and handles the connections between the UI elements and their respective
    functionalities.

    Methods:
        __init__: Initialize the controller and setup connections.
        setup_connections: Connect UI signals to their respective slots.
        populate_search_boxes: Populate the search boxes with distinct values from the model.
        search: Perform a search based on selected criteria and display results.
        clear: Clear the search inputs and results.
        open_secondary_window: Display the secondary window for data visualization.
        generate_plot: Generate a plot with the user-selected x and y axes.
    """
    def __init__(self):
        """
        Initialize the controller.

        This method creates the database, initializes the model and the main/secondary windows,
        sets up the connections between UI elements and their functionalities, and populates
        the search boxes with initial data.
        """
        db_loader.create_database()
        #db_loader.load_exoplanet_data()

        self.model = ExoplanetModel()
        self.main_window = MainWindow()
        self.secondary_window = SecondaryWindow()
        
        self.setup_connections()
        self.populate_search_boxes()

    def setup_connections(self):
        """
        Set up the connections between UI elements and their respective methods.

        This method connects the buttons in the main window and the secondary window
        to their respective slot functions in the controller.
        """
        self.main_window.search_button.clicked.connect(self.search)
        self.main_window.clear_button.clicked.connect(self.clear)
        self.main_window.open_button.clicked.connect(self.open_secondary_window)
        self.secondary_window.generate_plot_button.clicked.connect(self.generate_plot)
        
    def populate_search_boxes(self):
        """
        Populate the search boxes with distinct values from the model.

        This method retrieves distinct values for the search criteria from the model
        and populates the corresponding combo boxes in the main window.
        """
        self.main_window.populate_combo_box(self.main_window.name_search, self.model.get_distinct_names())
        self.main_window.populate_combo_box(self.main_window.year_search, self.model.get_distinct_years())
        self.main_window.populate_combo_box(self.main_window.method_search, self.model.get_distinct_methods())
        self.main_window.populate_combo_box(self.main_window.host_search, self.model.get_distinct_hosts())
        self.main_window.populate_combo_box(self.main_window.facility_search, self.model.get_distinct_facilities())

    def search(self):
        """
        Perform a search based on selected criteria and display results.

        This method retrieves the search criteria from the combo boxes, performs a search
        in the model, and displays the results in the output table of the main window.
        If no search criteria are selected, it shows an error message.
        """
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
        
    def clear(self):
        """
        Clear the search inputs and results.

        This method clears the contents of the output table and resets the
        search criteria combo boxes in the main window.
        """
        self.main_window.output_table.clearContents()

        self.main_window.name_search.clearEditText()
        self.main_window.year_search.clearEditText()
        self.main_window.method_search.clearEditText()
        self.main_window.host_search.clearEditText()
        self.main_window.facility_search.clearEditText()

    def open_secondary_window(self):
        """
        Display the secondary window for data visualization.

        This method shows the secondary window where users can generate plots
        based on selected data columns.
        """
        self.secondary_window.show()

    def generate_plot(self):
        """
        Generate a plot with the user-selected x and y axes.

        This method retrieves the selected x and y axis columns from the secondary window
        and calls the plot generation function to display the plot.
        """
        plot.generate_plot(self.secondary_window, self.secondary_window.column_names)
