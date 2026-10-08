import matplotlib
import numpy as np
import open3d as o3d
import pandas as pd

class PCDViewer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.geometries = None
        self.color_map = {
            "chair": [1, 0, 0],                # 赤
            "desk": [0, 0, 1],                 # 青
            "fire extinguisher": [1, 0.5, 0],  # オレンジ
            "chair desk": [0.5, 0, 0.5],       # 紫
            "aruco id=17": [0, 1, 0],          # 緑
        }

    def load_point_cloud_to_geometories(self):
        try:
            self.geometries = [o3d.io.read_point_cloud(self.file_path)]
            print(f"Successfully loaded point cloud from {self.file_path}")
        except Exception as e:
            print(f"Error loading point cloud: {e}")

    import numpy as np

    def align_gravity(self, angle_deg=45, axis="x"):
        if self.geometries is None:
            print("No geometries loaded.")
            return

        angle_rad = np.deg2rad(angle_deg)

        if axis == "x":
            R = o3d.geometry.get_rotation_matrix_from_xyz((angle_rad, 0, 0))
        elif axis == "y":
            R = o3d.geometry.get_rotation_matrix_from_xyz((0, angle_rad, 0))
        elif axis == "z":
            R = o3d.geometry.get_rotation_matrix_from_xyz((0, 0, angle_rad))
        else:
            return

        for g in self.geometries:
            g.rotate(R, center=(0, 0, 0))

    def add_semantic_dataframe(self, df):
        if self.geometries is None:
            print("No point cloud loaded. Cannot add semantic data.")
            return
        
        for _, row in df.iterrows():
            x, y, z = row["x"], row["y"], row["z"]
            label = row["label"]

            # 球を作成
            sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.07)
            sphere.translate((x, y, z))

            # 色設定（未定義は白）
            color = self.color_map.get(label, [1, 1, 1])
            sphere.paint_uniform_color(color)
            sphere.compute_vertex_normals()

            self.geometries.append(sphere)

    def colorize_by_axis(self, axis="z"):
        if self.geometries is None:
            return

        pcd = self.geometries[0]
        points = np.asarray(pcd.points)

        axis_dict = {"x": 0, "y": 1, "z": 2}
        idx = axis_dict.get(axis, 2)

        values = points[:, idx]

        low = np.percentile(values, 5)
        high = np.percentile(values, 95)

        clipped = np.clip(values, low, high)
        normalized = (clipped - low) / (high - low)

        colormap = matplotlib.colormaps["turbo"]
        colors = colormap(normalized)[:, :3]

        pcd.colors = o3d.utility.Vector3dVector(colors)

    def downsample_point_cloud(self, max_points=150000):
        if self.geometries is None:
            return

        pcd = self.geometries[0]
        points = np.asarray(pcd.points)

        if len(points) <= max_points:
            return

        idx = np.random.choice(len(points), max_points, replace=False)
        downsampled = pcd.select_by_index(idx)

        self.geometries[0] = downsampled

    def darken_point_cloud(self, factor=0.5):
        """
        factor=0.5 → 50%暗く
        """
        pcd = self.geometries[0]
        colors = np.asarray(pcd.colors)

        colors = colors * factor
        pcd.colors = o3d.utility.Vector3dVector(colors)

    def visualize(self):
        if self.geometries is None:
            print("No point cloud to visualize.")
            return

        vis = o3d.visualization.VisualizerWithKeyCallback()
        vis.create_window()
        opt = vis.get_render_option()
        opt.background_color = np.asarray([0, 0, 0])
        
        for g in self.geometries:
            vis.add_geometry(g)

        def update_x(vis):
            self.colorize_by_axis("x")
            vis.update_geometry(self.geometries[0])
            print("Colorized by X")
            return False

        def update_y(vis):
            self.colorize_by_axis("y")
            vis.update_geometry(self.geometries[0])
            print("Colorized by Y")
            return False

        def update_z(vis):
            self.colorize_by_axis("z")
            vis.update_geometry(self.geometries[0])
            print("Colorized by Z")
            return False

        vis.register_key_callback(ord("1"), update_x)
        vis.register_key_callback(ord("2"), update_y)
        vis.register_key_callback(ord("3"), update_z)

        print("Press 1=X, 2=Y, 3=Z to change color axis")

        vis.run()
        vis.destroy_window()


def csv_reader(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def main():
    csv_file_path = "./data/semantic_objects.csv"
    pcd_file_path = "./data/laser_map.pcd"

    # read csv file a df
    data = csv_reader(csv_file_path)
    if data is None:
        print("Failed to read the CSV file.")
        return

    # visualize pcd file
    pcdv = PCDViewer(pcd_file_path)
    pcdv.load_point_cloud_to_geometories()
    pcdv.downsample_point_cloud(max_points=150000)
    pcdv.add_semantic_dataframe(data)
    pcdv.align_gravity(angle_deg=45, axis="y")
    pcdv.colorize_by_axis(axis="z")
    pcdv.darken_point_cloud(factor=0.8)
    pcdv.visualize()

if __name__ == "__main__":
    main()
