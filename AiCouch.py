import cv2
import cvzone
from cvzone.PoseModule import PoseDetector
import numpy as np

cap = cv2.VideoCapture(0)
detector = PoseDetector(detectionCon=0.69)
dir = 0
curl_count = 0
color = (0, 0, 255)

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)  # Flip horizontally for mirror effect
    img = detector.findPose(img)
    lmlst, bbox = detector.findPosition(img, draw=False)

    if lmlst:
        angle = detector.findAngle(img, 12, 14, 16)
        bar_val = np.interp(angle, (40, 155), (60, 360))  # Adjusted to fit within the bounds
        bar_val = min(max(int(bar_val), 60), 360)  # Ensure the value is within the bounds
        per_val = np.interp(angle, (40, 155), (100, 0))

        # Draw a filled rectangle background
        cv2.rectangle(img, (560, 60), (600, 360), (0, 0, 0), -1)
        # Draw a filled rectangle for the bar
        cv2.rectangle(img, (560, int(bar_val)), (600, 360), color, -1)
        # Display percentage
        cvzone.putTextRect(img, f"{int(per_val)}%", (540, 40), 1.6, 2, (255, 255, 255), color, border=4)

        if per_val == 100:
            if dir == 0:
                curl_count += 0.5
                dir = 1
                color = (0, 255, 0)
        elif per_val == 0:
            if dir == 1:
                curl_count += 0.5
                dir = 0
                color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        # Debugging print statement
        print(f"Angle: {angle}, Bar Value: {bar_val}, Percentage: {per_val}, Curl Count: {curl_count}")

    # Display the title and curl count
    cvzone.putTextRect(img, 'Bicep Curl Counter', (30, 40), 2, 3, (255, 255, 255), (255, 0, 0), border=6)
    cvzone.putTextRect(img, f'Curl Count: {int(curl_count)}', (50, 120), 2, 3, (255, 255, 255), (0, 100, 0), border=6)

    cv2.imshow('Bicep Curl Counter', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
