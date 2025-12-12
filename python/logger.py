import serial
import time
import random

COM_PORT = 'COM4'       # Replace with your Arduino COM port
BAUD_RATE = 9600

DECISION_FILE = "decision.txt"

# Simulate CAN data
def get_can_data():
    speed = random.randint(0, 50)  # 0–50 km/h
    brake = random.randint(0, 1)
    return {"speed": speed, "brake": brake}

def read_decision():
    try:
        with open(DECISION_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "CLEAR"

if __name__ == "__main__":
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print("Logger connected to Arduino")
    except Exception as e:
        print(f"Error connecting to Arduino: {e}")
        exit(1)

    while True:
        can = get_can_data()
        speed = can["speed"]
        brake_state = can["brake"]

        vision_decision = read_decision()

        # Simple fusion logic
        command = "CLEAR"
        if vision_decision == "STOP" and speed > 5:
            command = "STOP"
        elif vision_decision == "STOP" and speed <= 5:
            command = "STOP"
        elif vision_decision == "CLEAR":
            command = "CLEAR"

        try:
            ser.write((command + "\n").encode())
        except Exception as e:
            print(f"Error sending to Arduino: {e}")

        print(f"Speed: {speed} | Brake: {brake_state} | Vision: {vision_decision} | Command: {command}")

        time.sleep(1)