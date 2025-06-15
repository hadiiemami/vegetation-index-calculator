Vegetation Index Calculator
  A desktop application built with Python and Tkinter to calculate and visualize vegetation indices (e.g., NDVI, NDWI, SAVI) from GeoTIFF files. Features include band selection, index statistics, and GeoTIFF export.
Features

Calculate 10 vegetation indices (NDVI, NDWI, SAVI, EVI, etc.).
Select bands dynamically based on the chosen index.
Display index statistics (min, max, mean, std dev).
Show image dimensions.
Save calculated indices as GeoTIFF files.
User-friendly GUI with modern design.

Requirements

Python 3.8+
Required packages: numpy, matplotlib, Pillow, rasterio
GeoTIFF files (e.g., from Sentinel-2 or Landsat)

Installation

Clone the repository:git clone https://github.com/your-username/vegetation-index-calculator.git


Create and activate a virtual environment:python -m venv .venv
.venv\Scripts\activate  # On Windows


Install dependencies:pip install numpy matplotlib Pillow rasterio


Run the application:python ndvi_calculator.py



Usage

Launch the application.
Click "Select GeoTIFF File" to load a GeoTIFF image.
Choose an index from the dropdown (e.g., NDVI).
Enter the appropriate band numbers (e.g., 4 for RED, 8 for NIR in Sentinel-2).
Click "Calculate Index" to visualize the result.
Use "Save as GeoTIFF" to export the calculated index.

Building Executable
  To create a standalone .exe for Windows:
pip install pyinstaller
pyinstaller --onefile --windowed --collect-all=rasterio --add-data ".venv\Lib\site-packages\rasterio\gdal_data;gdal_data" --icon=favicon.ico ndvi_calculator.py

License
  MIT License
Contact
  Feel free to open an issue or contact me at your-email@example.com.
