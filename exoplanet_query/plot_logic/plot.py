import sqlite3
from scipy import stats
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QMessageBox


def bin_and_aggregate_data(x_data, y_data, num_bins=200):
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

def generate_plot(secondary_window, column_names):
    try:
        conn = sqlite3.connect('exoplanets.db')
        c = conn.cursor()
        
        # Retrieve data from the database based on selected columns
        x_column_label = secondary_window.x_axis_combo.currentText()
        y_column_label = secondary_window.y_axis_combo.currentText()

        # Retrieve the actual column names using the column_names dictionary
        x_column = column_names.get(x_column_label, x_column_label)
        y_column = column_names.get(y_column_label, y_column_label)
        
        c.execute(f'SELECT {x_column}, {y_column} FROM exoplanets WHERE {x_column} != "" AND {y_column} != ""')
        data = c.fetchall()
        
        # Close the database connection
        conn.close()
        
        # Extract x and y data
        x_data = np.array([row[0] for row in data])
        y_data = np.array([row[1] for row in data])
        
        # Clear the previous plot
        secondary_window.plot_widget.clear()
        
        # Bin and aggregate data
        bin_centers, bin_values = bin_and_aggregate_data(x_data, y_data)
        
        # Create the scatter plot
        secondary_window.plot_widget.plot(bin_centers, bin_values, symbol='o', symbolSize=5, pen=None)
        secondary_window.plot_widget.setLabel('left', text=y_column_label)
        secondary_window.plot_widget.setLabel('bottom', text=x_column_label)
        secondary_window.plot_widget.showGrid(False, False)

        # Add trend line (linear regression)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_data, y_data)
        trend_line_x = np.array([np.min(x_data), np.max(x_data)])
        trend_line_y = slope * trend_line_x + intercept
        secondary_window.plot_widget.plot(trend_line_x, trend_line_y, pen=pg.mkPen('r'), name="Trend Line")
        
    except sqlite3.Error as e:
        QMessageBox.warning(secondary_window, "Error", "Failed to retrieve data from the database.")
