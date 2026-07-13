from yolo_detector import detect_people

image_path = "https://img.magnific.com/premium-photo/crowd-people-are-gathered-together-one-is-wearing-yellow-scarf_1100978-5370.jpg?semt=ais_hybrid&w=740&q=80/dataset/sample.jpg"   # Replace with your image

results = detect_people(image_path, conf=0.15)

count = 0

for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])

        # COCO class 0 = Person
        if class_id == 0:
            count += 1

print(f"People Detected: {count}")