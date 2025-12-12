# Shadow ECU Proof-of-Concept (PoC)

A prototype Shadow ECU system simulating a vehicle safety-critical module. This project demonstrates **actuator control, vision-based STOP sign detection, and data fusion** using Arduino and Python.

---

## System Overview

The Shadow ECU system consists of three main components:

1. **Arduino-based Shadow ECU**
   - Controls a **servo motor** simulating a brake actuator.
   - Uses an **LED** as a visual safety indicator.
   - Receives `STOP` or `CLEAR` commands via serial communication.
   - Implements a **safety fallback**: releases the brake if no command is received within 2 seconds.

2. **Python Data Fusion (`logger.py`)**
   - Generates simulated **CAN-like data** (speed & brake status).
   - Reads **vision decisions** (`STOP` / `CLEAR`) from `vision.py`.
   - Applies **fusion logic** to decide commands for the Arduino.
   - Sends commands via serial and logs system state.

3. **Vision System (`vision.py`)**
   - Uses OpenCV to detect **STOP signs** via:
     - Red color HSV thresholding
     - Contour extraction
     - Octagonal shape approximation
     - Area filtering
   - Outputs `STOP` or `CLEAR` decisions to `decision.txt`.
   - In this PoC, the **laptop camera simulates a vehicle-mounted camera**.

---

## Requirements

- **Hardware**: Arduino Uno, servo motor, LED, connecting wires
- **Software**:
  - Python 3.12+
  - Arduino IDE
  - Libraries: OpenCV, NumPy, PySerial
- **Optional**: Webcam (laptop camera suffices)

Install Python dependencies:

```bash
pip install opencv-python numpy pyserial
