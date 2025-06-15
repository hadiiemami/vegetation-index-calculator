# Vegetation Index Calculator

  A desktop application built with Python and Tkinter to calculate and visualize vegetation indices (e.g., NDVI, NDWI, SAVI) from GeoTIFF files. Features include band selection, index statistics, and GeoTIFF export.

  ## Features
  - Calculate 10 vegetation indices (NDVI, NDWI, SAVI, EVI, etc.).
  - Select bands dynamically based on the chosen index.
  - Display index statistics (min, max, mean, std dev).
  - Show image dimensions.
  - Save calculated indices as GeoTIFF files.
  - User-friendly GUI with modern design.

  ## Requirements
  - Python 3.8+
  - Required packages: `numpy`, `matplotlib`, `Pillow`, `rasterio`
  - GeoTIFF files (e.g., from Sentinel-2 or Landsat)

  ## Installation
  1. Clone the repository:
     ```bash
     git clone https://github.com/hadiiemami/vegetation-index-calculator.git
     ```
  2. Create and activate a virtual environment:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate  # On Windows
     ```
  3. Install dependencies:
     ```bash
     pip install numpy matplotlib Pillow rasterio
     ```
  4. Run the application:
     ```bash
     python ndvi_calculator.py
     ```

  ## Usage
  1. Launch the application.
  2. Click "Select GeoTIFF File" to load a GeoTIFF image.
  3. Choose an index from the dropdown (e.g., NDVI).
  4. Enter the appropriate band numbers (e.g., 4 for RED, 8 for NIR in Sentinel-2).
  5. Click "Calculate Index" to visualize the result.
  6. Use "Save as GeoTIFF" to export the calculated index.

  ## Building Executable
  To create a standalone `.exe` for Windows:
  ```bash
  pip install pyinstaller
  pyinstaller --onefile --windowed --collect-all=rasterio --add-data ".venv\Lib\site-packages\rasterio\gdal_data;gdal_data" --icon=favicon.ico ndvi_calculator.py
  ```

  ## License
  MIT License

  ## Contact
  Feel free to open an issue or contact me at hadiemami1995@example.com.
