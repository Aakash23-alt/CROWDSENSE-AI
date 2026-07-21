from ultralytics import YOLO
from utils.centroid_tracker import CentroidTracker
import cv2
import time

# ============================================
# Load Model
# ============================================

model = YOLO("yolov8m.pt")
tracker = CentroidTracker()

# ============================================
# Video
# ============================================

video_path = "datasets/crowd.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Cannot open video.")
    exit()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Resolution : {width}x{height}")
print(f"FPS : {fps}")

# ============================================
# Output Video
# ============================================

out = cv2.VideoWriter(
    "outputs/output_video.mp4",
    cv2.VideoWriter_fourcc(*'mp4v'),
    fps,
    (width, height)
)

prev_time = time.time()

# ============================================
# Main Loop
# ============================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # ========================================
    # YOLO Detection
    # ========================================

    results = model.predict(
        source=frame,
        classes=[0],
        conf=0.25,
        imgsz=960,
        device=0,
        verbose=False
    )

    boxes = results[0].boxes

    person_count = len(boxes)

    annotated = results[0].plot()

    # ========================================
    # Tracker
    # ========================================

    centers, movements = tracker.update(boxes)

    for center in centers:

        cv2.circle(
            annotated,
            center,
            5,
            (0,255,255),
            -1
        )

    # ========================================
    # Draw Grid
    # ========================================

    cv2.line(
        annotated,
        (width//2,0),
        (width//2,height),
        (255,255,0),
        2
    )

    cv2.line(
        annotated,
        (0,height//2),
        (width,height//2),
        (255,255,0),
        2
    )

    # ========================================
    # Grid Counters
    # ========================================

    top_left = 0
    top_right = 0
    bottom_left = 0
    bottom_right = 0

    # ========================================
    # Count People
    # ========================================

    for box in boxes:

        x1,y1,x2,y2 = box.xyxy[0]

        cx = int((x1+x2)/2)
        cy = int((y1+y2)/2)

        if cx < width//2 and cy < height//2:

            top_left += 1

        elif cx >= width//2 and cy < height//2:

            top_right += 1

        elif cx < width//2 and cy >= height//2:

            bottom_left += 1

        else:

            bottom_right += 1

    # ========================================
    # Most Crowded Zone
    # ========================================

    grid_counts = {

        "Top Left": top_left,
        "Top Right": top_right,
        "Bottom Left": bottom_left,
        "Bottom Right": bottom_right

    }

    most_crowded = max(
        grid_counts,
        key=grid_counts.get
    )

    max_people = grid_counts[most_crowded]

    # ========================================
    # Crowd Density
    # ========================================

    if person_count < 10:

        density = "LOW"

    elif person_count < 20:

        density = "MEDIUM"

    else:

        density = "HIGH"
        # ========================================
    # Crowd Flow Detection
    # ========================================

    flow = "STATIONARY"

    if len(movements) > 5:

        avg_dx = sum(m[0] for m in movements) / len(movements)
        avg_dy = sum(m[1] for m in movements) / len(movements)

        threshold = 2

        if abs(avg_dx) > abs(avg_dy):

            if avg_dx > threshold:
                flow = "RIGHT ➜"

            elif avg_dx < -threshold:
                flow = "LEFT ⬅"

        else:

            if avg_dy > threshold:
                flow = "DOWN ⬇"

            elif avg_dy < -threshold:
                flow = "UP ⬆"

    # ========================================
    # FPS
    # ========================================

    current_time = time.time()

    fps_display = 1 / (current_time - prev_time)

    prev_time = current_time

    # ========================================
    # Information Panel
    # ========================================

    panel_x = 20
    y = 40
    gap = 30

    cv2.putText(
        annotated,
        f"People : {person_count}",
        (panel_x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0,255,0),
        2
    )

    y += gap

    cv2.putText(
        annotated,
        f"Density : {density}",
        (panel_x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0,255,255),
        2
    )

    y += gap

    cv2.putText(
        annotated,
        f"Flow : {flow}",
        (panel_x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255,255,0),
        2
    )

    y += gap

    cv2.putText(
        annotated,
        f"FPS : {fps_display:.2f}",
        (panel_x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255,255,255),
        2
    )

    y += 40

    cv2.putText(
        annotated,
        f"Top Left : {top_left}",
        (panel_x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,255,255),
        2
    )

    y += gap

    cv2.putText(
        annotated,
        f"Top Right : {top_right}",
        (panel_x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,255,255),
        2
    )

    y += gap

    cv2.putText(
        annotated,
        f"Bottom Left : {bottom_left}",
        (panel_x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,255,255),
        2
    )

    y += gap

    cv2.putText(
        annotated,
        f"Bottom Right : {bottom_right}",
        (panel_x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,255,255),
        2
    )

    y += 40

    cv2.putText(
        annotated,
        f"Most Crowded : {most_crowded} ({max_people})",
        (panel_x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0,0,255),
        2
    )

    # ========================================
    # Save Video
    # ========================================

    out.write(annotated)

    # ========================================
    # Resize for Display
    # ========================================

    display = cv2.resize(
        annotated,
        (1280,720)
    )

    cv2.imshow(
        "ResQAI Crowd Management",
        display
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ============================================
# Cleanup
# ============================================

cap.release()

out.release()

cv2.destroyAllWindows()

print("Output video saved in outputs folder.")