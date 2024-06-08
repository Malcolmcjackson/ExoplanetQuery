<h3 align="center">NASA-Exoplanet-Query-App</h3>
  <p align="center"> An application that allows users to query NASA's exoplanet archive written in Python</p>

## Features
- Query exoplanet data by name, discovery year, method, host name, and facility.
- Display results in a searchable and sortable table.
- Generate customizable plots for data visualization.

## Screenshots

Query Window            |  Plot Window
:-------------------------:|:-------------------------:
  ![Main Window](screenshots/main_window.png)  |    ![Secondary Window](screenshots/secondary_window.png)


## Prerequisites
- Python 3.6+
- Additional dependencies listed in `requirements.txt`

## Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/exoplanet-query.git
   ```

2. Navigate to the project directory:
    ```sh
    cd exoplanet-query
    ```

3. Create a virtual environment:
    ``` sh
    python -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
        ```sh 
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh 
        source venv/bin/activate
        ```
5. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Ensure the virtual environment is activated:
    - On Windows:
        ```sh 
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh 
        source venv/bin/activate
        ```
3. Use the main window to query exoplanet data.

4. Open the secondary window to visualize data with plots.

## Potential Improvements
Potential features to be implemented in the future:

- Enable exporting query results to various file formats (CSV, JSON, etc.).
- Implement more advanced data visualization options, such as 3D plots and interactive graphs.
- Add support for filtering data by additional criteria (such as planet radius, mass, and distance from Earth).
- Implement hyperlinking to the NASA Exoplanet website when a planet name is clicked for more detailed information.
