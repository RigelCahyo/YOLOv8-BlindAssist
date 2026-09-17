import torch
print(torch.cuda.is_available())  # Harus mencetak True
print(torch.cuda.get_device_name(0))  # Menampilkan nama GPU

#Mendownload dataset
from roboflow import Roboflow
rf = Roboflow(api_key="rhsP9SmIGx5ZaMyUMWbf")
project = rf.workspace("miii").project("dataset-ss2ki")
version = project.version(1)
dataset = version.download("yolov8")

#Melatih model
from ultralytics import YOLO

# Path ke file data.yaml
data_yaml_path = "D:\Kuliah\Semester 5\Capstone\coba aja\Dataset-1\data.yaml"

# Inisialisasi model YOLOv8
model = YOLO("yolov8s.pt")  # Menggunakan YOLOv8 pre-trained (versi n = nano, s = small, m = medium)

# Melatih model
if __name__ == '__main__':
    model.train(data=data_yaml_path, epochs=100, imgsz=640, batch=8, device=0,
                name="custom_yolov8s", workers=0 
                )
