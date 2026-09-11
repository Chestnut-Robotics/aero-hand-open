# 🤖 Aero Hand Open ROS 2 Node

The **Aero Hand Open Node** provides a ROS 2 interface for controlling Chestnut Robotics’ [Aero Hand](https://github.com/chestnut-robotics/aero-hand-open/tree/main/sdk) via the **Aero Hand SDK**.  
It allows controlling one or both hands simultaneously, exposing ROS 2 topics for both **joint-space** and **actuator-space** control.

## 🧩 Overview

This node acts as a bridge between ROS 2 and the Aero Hand hardware. It:
- Accepts commands for **joint angles** or **actuator positions**.
- Publishes real-time **actuator state feedback** (positions, speeds, currents, temperatures).
- Supports **single-hand** (right/left) or **dual-hand** operation.
- Uses parameters for serial ports, baud rate, and control mode.

## ⚙️ Running the Node

```bash
ros2 run aero_hand_open aero_hand_node
```

### Parameters

| Parameter | Type | Default | Description |
|------------|------|----------|-------------|
| `right_port` | `string` | `""` | Serial port for the right hand |
| `left_port` | `string` | `""` | Serial port for the left hand |
| `baudrate` | `int` | `921600` | Serial baud rate |
| `feedback_frequency` | `float` | `100.0` | Rate (Hz) to publish actuator feedback |
| `control_space` | `string` | `"joint"` | Control mode: `"joint"` or `"actuator"` |

Example run:
```bash
ros2 run aero_hand_open aero_hand_node --ros-args -p right_port:=/dev/ttyUSB0 -p left_port:=/dev/ttyUSB1 -p control_space:=joint
```

## 🛰️ ROS 2 Interfaces

### Subscribed Topics

| Topic | Message Type | Description |
|--------|---------------|-------------|
| `right/joint_control` | `aero_hand_open_msgs/JointControl` | Right hand joint-angle commands (radians) |
| `left/joint_control` | `aero_hand_open_msgs/JointControl` | Left hand joint-angle commands (radians) |
| `right/actuator_control` | `aero_hand_open_msgs/ActuatorControl` | Right hand actuator-space commands |
| `left/actuator_control` | `aero_hand_open_msgs/ActuatorControl` | Left hand actuator-space commands |

> Only one control mode is active at a time, based on `control_space`.

### Published Topics

| Topic | Message Type | Description |
|--------|---------------|-------------|
| `right/actuator_states` | `aero_hand_open_msgs/ActuatorStates` | Feedback for the right hand |
| `left/actuator_states` | `aero_hand_open_msgs/ActuatorStates` | Feedback for the left hand |

## 🧠 Behavior Summary

- **Initialization:**  
  Each hand is initialized if a valid serial port is provided.  
  The node throws an error if both `right_port` and `left_port` are empty.

- **Feedback:**  
  At the configured rate, the node publishes:
  - `actuations`
  - `actuator_speeds`
  - `actuator_currents`
  - `actuator_temperatures`

## 🧩 Dependencies

- **ROS 2 Humble** (or newer)
- **aero_open_sdk**
- **aero_hand_open_msgs**

Make sure the SDK is installed and accessible in your environment.

---

## ⚖️ License

This project is licensed under the **Apache License 2.0**.

---

<div align="center">
If you find this project useful, please give it a star! ⭐  

Built with ❤️ by <a href="https://chestnut.bot">Chestnut Robotics</a>
</div>
