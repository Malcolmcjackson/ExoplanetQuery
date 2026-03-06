<h1 align="center">🔭 NASA Exoplanet Query App</h1>
<p align="center"> A Streamlit-powered web application for exploring NASA’s Exoplanet Archive through interactive queries and engaging visualizations. </p>

<p align="center"> 🚀 Live Demo: <a href="https://nasaexoplanetquery.streamlit.app/">nasaexoplanetquery.streamlit.app</a> </p>

# 🌟 Features

### 🔍 Interactive Querying
#### Filter planets by:
- Name
- Discovery Year
- Discovery Method
- Host Star
- Discovery Facility
- And more!

Results appear in a clean, sortable table with friendly labels.

### 📊 Curated Scientific Visualizations
#### All charts are built with Plotly and tuned for mobile:
- **Planet Radius vs Planet Mass** (with trendline + R² annotation)
- **Orbital Distance vs Temperature** (log-binned smoothing option)
- **Cumulative Exoplanet Discoveries Over Time** (animated!)
- **Distance From Earth Histogram** (log-distance scaling)
- **Discovery Method Radius Distributions** (zoomed + full-range boxplots)

### 🌍 Fully Web-Based
#### No installation required; runs directly in your browser.

## 📸 Visualization Gallery

| Planet Radius vs Mass | Temperature vs Orbital Distance |
|----------------------|----------------------------------|
| ![](screenshots/radius_mass.png) | ![](screenshots/temp_distance.png) |

| Cumulative Discoveries (Animated) | Distance From Earth Histogram |
|-----------------------------------|-------------------------------|
| ![](screenshots/discovery_year.png) | ![](screenshots/distance_hist.png) |

| Discovery Method Radius Boxplots (Zoomed) | Full Range Boxplots |
|-------------------------------------------|----------------------|
| ![](screenshots/method_zoom.png) | ![](screenshots/method_full.png) |

## Local Setup
### Prerequisites
- Python 3.9+
- pip

### Setup
 ```
git clone https://github.com/Malcolmcjackson/NASA-Exoplanet-Query-App.git
cd NASA-Exoplanet-Query-App
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
 ```

### Run the Streamlit App
```
streamlit run exoplanet_query/app.py
```

# 📦 Project Structure
```
exoplanet_query/
│
├── app.py                 # Streamlit UI
├── controller/            # Query filtering logic
├── database/              # Data loading / caching
├── plot/                  # Plot construction functions
├── screenshots/           # Demo screenshots
└── requirements.txt
```

## 💡Future Improvements
- Add more curated scientific plots (density maps, 3D scatter, HR-diagram overlays)
- Save user queries to downloadable CSV/JSON
- Clickable planet names linking to NASA’s Exoplanet Archive pages
- Faster data caching / optional local SQLite sync
- More mobile optimizations (collapsible sections, sticky nav)

## 🧡 Acknowledgments
- Data provided by the **NASA Exoplanet Archive**:  https://exoplanetarchive.ipac.caltech.edu/
