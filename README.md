# Shadow ECU Proof-of-Concept (PoC)

A prototype Shadow ECU system that integrates a camera-based AI vision module, simulated CAN data, and a microcontroller-based actuator controller to demonstrate STOP-sign detection, data fusion, and safety-critical braking behavior.

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
