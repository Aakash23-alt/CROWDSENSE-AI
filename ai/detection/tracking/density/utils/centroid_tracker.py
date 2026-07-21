import math


class CentroidTracker:

    def __init__(self, max_distance=50):
        self.previous_centroids = []
        self.max_distance = max_distance

    def update(self, boxes):

        current_centroids = []

        for box in boxes:

            x1, y1, x2, y2 = box.xyxy[0]

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            current_centroids.append((cx, cy))

        movements = []

        for current in current_centroids:

            nearest = None
            min_distance = float("inf")

            for previous in self.previous_centroids:

                distance = math.sqrt(
                    (current[0] - previous[0]) ** 2 +
                    (current[1] - previous[1]) ** 2
                )

                if distance < min_distance and distance < self.max_distance:
                    min_distance = distance
                    nearest = previous

            if nearest:

                dx = current[0] - nearest[0]
                dy = current[1] - nearest[1]

                movements.append((dx, dy))

        self.previous_centroids = current_centroids

        return current_centroids, movements