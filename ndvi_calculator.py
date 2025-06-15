# ndvi_calculator.py
# Enhanced desktop app to calculate, display, and save vegetation indices with stats and dimensions

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class NDVIApp:
    def __init__(self, root):
        """Initialize the main application window."""
        self.root = root
        self.root.title("Vegetation Index Calculator")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        try:
            self.root.iconbitmap("icon.ico")  # Optional: Custom icon
        except:
            pass

        self.file_path = None
        self.band_count = 0
        self.image_dims = (0, 0)
        self.colorbar = None
        self.index_data = None
        self.profile = None
        self.canvas = None

        # Available indices and their required bands
        self.indices = {
            "NDVI": {"name": "Normalized Difference Vegetation Index", "bands": ["RED", "NIR"],
                     "formula": lambda red, nir: (nir - red) / (nir + red)},
            "NDWI": {"name": "Normalized Difference Water Index", "bands": ["GREEN", "NIR"],
                     "formula": lambda green, nir: (green - nir) / (green + nir)},
            "SAVI": {"name": "Soil-Adjusted Vegetation Index", "bands": ["RED", "NIR"],
                     "formula": lambda red, nir: ((nir - red) / (nir + red + 0.5)) * (1 + 0.5)},
            "EVI": {"name": "Enhanced Vegetation Index", "bands": ["BLUE", "RED", "NIR"],
                    "formula": lambda blue, red, nir: 2.5 * (nir - red) / (nir + 6 * red - 7.5 * blue + 1)},
            "GNDVI": {"name": "Green NDVI", "bands": ["GREEN", "NIR"],
                      "formula": lambda green, nir: (nir - green) / (nir + green)},
            "NDRE": {"name": "Normalized Difference Red Edge", "bands": ["RED_EDGE", "NIR"],
                     "formula": lambda red_edge, nir: (nir - red_edge) / (nir + red_edge)},
            "MSAVI": {"name": "Modified Soil-Adjusted Vegetation Index", "bands": ["RED", "NIR"],
                      "formula": lambda red, nir: (2 * nir + 1 - np.sqrt((2 * nir + 1) ** 2 - 8 * (nir - red))) / 2},
            "OSAVI": {"name": "Optimized Soil-Adjusted Vegetation Index", "bands": ["RED", "NIR"],
                      "formula": lambda red, nir: (nir - red) / (nir + red + 0.16)},
            "RVI": {"name": "Ratio Vegetation Index", "bands": ["RED", "NIR"],
                    "formula": lambda red, nir: nir / red},
            "DVI": {"name": "Difference Vegetation Index", "bands": ["RED", "NIR"],
                    "formula": lambda red, nir: nir - red}
        }

        # Setup GUI
        self.setup_gui()

    def setup_gui(self):
        """Set up the enhanced GUI elements."""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding=10)
        file_frame.pack(fill="x", pady=5)

        ttk.Button(file_frame, text="Select GeoTIFF File", command=self.load_file).pack(side="left", padx=5)
        self.file_label = ttk.Label(file_frame, text="No file selected", wraplength=300)
        self.file_label.pack(side="left", padx=10)
        self.band_info = ttk.Label(file_frame, text="Band info: None")
        self.band_info.pack(side="left", padx=10)
        self.dims_label = ttk.Label(file_frame, text="Dimensions: None")
        self.dims_label.pack(side="left", padx=10)

        # Index and band selection frame
        index_frame = ttk.LabelFrame(main_frame, text="Index and Band Selection", padding=10)
        index_frame.pack(fill="x", pady=5)

        ttk.Label(index_frame, text="Select Index:").pack(side="left")
        self.index_var = tk.StringVar(value="NDVI")
        self.index_combo = ttk.Combobox(index_frame, textvariable=self.index_var, values=list(self.indices.keys()),
                                        state="readonly")
        self.index_combo.pack(side="left", padx=5)
        self.index_combo.bind("<<ComboboxSelected>>", self.update_band_inputs)

        self.band_frame = ttk.Frame(index_frame)
        self.band_frame.pack(side="left", padx=10)
        self.band_entries = {}
        self.update_band_inputs(None)

        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Index Statistics", padding=10)
        stats_frame.pack(fill="x", pady=5)
        self.stats_text = tk.Text(stats_frame, height=4, width=50, state="disabled")
        self.stats_text.pack(pady=5)

        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        ttk.Button(button_frame, text="Calculate Index", command=self.calculate_index).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save as GeoTIFF", command=self.save_index).pack(side="left", padx=5)

        # Canvas for plot
        self.create_plot()

    def create_plot(self):
        """Create or recreate the matplotlib plot."""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        plt.close(self.figure) if hasattr(self, 'figure') else None

        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

    def load_file(self):
        """Load a GeoTIFF file and update info."""
        try:
            file_path = filedialog.askopenfilename(filetypes=[("GeoTIFF files", "*.tif *.tiff")])
            if file_path:
                self.file_path = file_path
                self.file_label.config(text=f"File: {file_path.split('/')[-1]}")
                with rasterio.open(file_path) as dataset:
                    self.band_count = dataset.count
                    self.image_dims = (dataset.width, dataset.height)
                    self.profile = dataset.profile
                    self.band_info.config(text=f"Band info: {self.band_count} bands available")
                    self.dims_label.config(text=f"Dimensions: {self.image_dims[0]} × {self.image_dims[1]} pixels")
            else:
                self.file_label.config(text="No file selected")
                self.band_info.config(text="Band info: None")
                self.dims_label.config(text="Dimensions: None")
                self.file_path = None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
            self.file_path = None

    def update_band_inputs(self, event):
        """Update band input fields based on selected index."""
        for widget in self.band_frame.winfo_children():
            widget.destroy()
        self.band_entries = {}

        selected_index = self.index_var.get()
        bands = self.indices[selected_index]["bands"]

        for band in bands:
            ttk.Label(self.band_frame, text=f"{band} Band:").pack(side="left", padx=5)
            entry = ttk.Entry(self.band_frame, width=5)
            entry.pack(side="left", padx=5)
            entry.insert(0, "1")
            self.band_entries[band] = entry

    def calculate_index(self):
        """Calculate and display the selected vegetation index."""
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select a GeoTIFF file first!")
            return

        try:
            selected_index = self.index_var.get()
            bands = self.indices[selected_index]["bands"]
            formula = self.indices[selected_index]["formula"]

            # Get band numbers
            band_indices = {}
            for band in bands:
                band_idx = int(self.band_entries[band].get()) - 1
                if band_idx < 0 or band_idx >= self.band_count:
                    messagebox.showerror("Error", f"Invalid {band} band number! File has {self.band_count} bands.")
                    return
                band_indices[band] = band_idx

            # Read bands
            with rasterio.open(self.file_path) as dataset:
                band_data = {band: dataset.read(idx + 1).astype(float) for band, idx in band_indices.items()}

                # Calculate index
                np.seterr(all='ignore')
                self.index_data = formula(*[band_data[band] for band in bands])
                self.index_data = np.nan_to_num(self.index_data, nan=0.0, posinf=0.0, neginf=0.0)

                # Update statistics
                stats = {
                    "Minimum": np.min(self.index_data),
                    "Maximum": np.max(self.index_data),
                    "Mean": np.mean(self.index_data),
                    "Std Dev": np.std(self.index_data)
                }
                self.stats_text.config(state="normal")
                self.stats_text.delete(1.0, tk.END)
                self.stats_text.insert(tk.END, "\n".join(f"{k}: {v:.4f}" for k, v in stats.items()))
                self.stats_text.config(state="disabled")

                # Recreate plot to avoid NoneType errors
                self.create_plot()

                # Display index
                img = self.ax.imshow(self.index_data, cmap='RdYlGn', vmin=-1, vmax=1)
                self.ax.set_title(f"{selected_index} Map")
                self.ax.axis('off')
                self.colorbar = self.figure.colorbar(img, ax=self.ax, label=selected_index)
                self.canvas.draw()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid band numbers!")
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating {selected_index}: {e}")

    def save_index(self):
        """Save the calculated index as a GeoTIFF file."""
        if not hasattr(self, 'index_data'):
            messagebox.showwarning("Warning", "Please calculate an index first!")
            return

        try:
            save_path = filedialog.asksaveasfilename(defaultextension=".tif", filetypes=[("GeoTIFF files", "*.tif")])
            if save_path:
                profile = self.profile.copy()
                profile.update(dtype=rasterio.float32, count=1)

                with rasterio.open(save_path, 'w', **profile) as dst:
                    dst.write(self.index_data.astype(np.float32), 1)
                messagebox.showinfo("Success", f"Index saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save index: {e}")


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = NDVIApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Failed to initialize GUI: {e}")