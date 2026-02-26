# PCD Viewer

A simple Python utility for visualizing point cloud data (PCD files) with semantic annotations.
It loads a `.pcd` file, optionally downsamples the points, applies axis-based colorization, aligns the cloud to gravity,
and overlays semantic objects defined in a CSV file. Interaction keys allow switching the color axis during visualization.

---

## 🔧 Requirements

* Python 3.12 (Don't use >=3.13 until updating of `open3d`)
* [open3d](http://www.open3d.org/) (>=0.19.0)
* [numpy](https://numpy.org/)
* [pandas](https://pandas.pydata.org/)
* [matplotlib](https://matplotlib.org/) (for color maps)

Dependencies are listed in `pyproject.toml`.


## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone <repo-url> pcd_viewer
   cd pcd_viewer
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows use `venv\Scripts\activate`
   pip install -r requirements.txt      # installs dependencies listed in this file
   # or, to install the package itself (editable install):
   pip install -e .
   ```

   *(Note: installing the package via `pip install .` or `pip install -e .` will create a
   `pcd-viewer` distribution entry.)*

   > If you prefer using `uv` to manage your environment you can run:
   > ```bash
   > uv sync
   > ```



## 🗂️ Project Structure

```
pcd_viewer/
├── main.py                   # entry point
├── pyproject.toml            # project metadata & dependencies
├── README.md                 # this file
└── data/                     # example data
    ├── laser_map.pcd         # sample point cloud
    └── semantic_objects.csv  # semantic annotations
```


## 📁 Semantic CSV Format

The CSV file should contain at least the following columns:

| Column | Description                              |
|--------|------------------------------------------|
| x,y,z  | 3D coordinates of the semantic object    |
| label  | Semantic class (e.g. `chair`, `desk`)    |

Additional rotation fields (`rx, ry, rz`) are ignored by the viewer but may be present.

Colors for known labels are defined in `PCDViewer.color_map`; unknown labels default to white.


## 🧠 Features

* **Load PCD file:** reads point cloud from disk using Open3D.
* **Downsample:** random subsampling to limit the number of rendered points.
* **Gravity alignment:** rotate the scene about an axis by a specified angle.
* **Colorization:** assign colors to points based on x/y/z axis value using the `turbo` colormap.
* **Semantic overlay:** display spheres at annotated object positions with label-specific colors.
* **Interactive controls:**
  * Press `1` to colorize by X-axis
  * Press `2` to colorize by Y-axis
  * Press `3` to colorize by Z-axis


## ▶️ Usage

Run the main script from the project root:

```bash
python main.py
```

By default it looks for `./data/laser_map.pcd` and
`./data/semantic_objects.csv`. You can modify `main()` to point to other files or integrate
`PCDViewer` into your own application.


## ✅ Example

```python
from main import PCDViewer, csv_reader

csv = csv_reader("data/semantic_objects.csv")
pcdv = PCDViewer("data/laser_map.pcd")
pcdv.load_point_cloud_to_geometories()
pcdv.downsample_point_cloud(max_points=150000)
pcdv.add_semantic_dataframe(csv)
pcdv.align_gravity(angle_deg=45, axis="y")
pcdv.colorize_by_axis(axis="z")
pcdv.darken_point_cloud(factor=0.5)
pcdv.visualize()
```


## 🤝 Contributing

Feel free to open issues or pull requests. Suggestions for additional
visualization features (e.g. bounding boxes, point cloud filtering, etc.)
are welcome.


## 📄 License

Specify your license here (e.g. MIT).