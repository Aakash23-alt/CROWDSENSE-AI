from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_people(image_path, conf=0.25):
    results = model(image_path, conf=conf)
    return results