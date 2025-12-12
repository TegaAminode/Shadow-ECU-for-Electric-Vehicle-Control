import cv2
import numpy as np
import time

DECISION_FILE = "decision.txt"

def write_decision(decision):
    with open(DECISION_FILE, "w") as f:
        f.write(decision)

def detect_stop_sign(frame):
    """
    Simple STOP sign detection using red color + octagon approximation
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Red color range
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.04*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        if len(approx) == 8 and area > 500:  # Octagon + minimum area
            return True
    return False

# Initialize camera
cap = cv2.VideoCapture(0)
time.sleep(2)

print("Vision AI Started (Stop Sign Detection)")

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    stop_detected = detect_stop_sign(frame)
    
    decision = "STOP" if stop_detected else "CLEAR"
    
    write_decision(decision)
    print(f"Decision: {decision}")
    
    # Optional display
    if stop_detected:
        cv2.putText(frame, "STOP SIGN DETECTED", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()