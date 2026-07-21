from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("yolov8m.pt")

# Read image
image = cv2.imread("datasets/crowd.jpg")

if image is None:
    print("Image not found!")
    exit()

# Detect ONLY persons
results = model(
    image,
    classes=[0],
    imgsz=1280,
    conf=0.20
)

# Count persons
person_count = len(results[0].boxes)

print(f"People Detected: {person_count}")

# Draw detections
annotated = results[0].plot()

# Display count
cv2.putText(
    annotated,
    f"People: {person_count}",
    (20,40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0,255,0),
    2
)

cv2.imwrite("outputs/result.jpg", annotated)

cv2.imshow("Crowd Detection", annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()