# 🖐️ Aero Hand Open Retargeting — ROS 2 Package

The **Aero Hand Open Retargeting** package provides a ROS 2-based interface that enables real-time control of **Chestnut Robotics’ Aero Hand** using the **Manus gloves**.

## 🧩 Overview

This package:
- Subscribes to **Manus glove data** published via `manus_ros2`.
- Retargets (maps) the human hand joint angles to Aero Hand’s robotic joint structure.
- Publishes joint-space commands to the **Aero Hand Open Node** (`aero_hand_open`).

## 🚀 Launch File

The package includes a launch file that brings up the complete teleoperation pipeline:
- Manus glove data stream (`manus_ros2`)
- Retargeting node (`aero_hand_open_retargeting`)
- Aero Hand hardware node (`aero_hand_open`)


### Running the Teleop Stack
```bash
ros2 launch aero_hand_open_retargeting aero_hand_teleop.launch.py
```

## 🧰 Dependencies

- **ROS 2 Humble** (or newer)
- **manus_ros2**
- **aero_open_sdk**
- **aero_hand_open**
- **aero_hand_open_msgs**

Ensure all packages are built in your workspace before launching.

## ⚖️ License

This project is licensed under the **Apache License 2.0**.

---

<div align="center">
If you find this project useful, please give it a star! ⭐  

Built with ❤️ by <a href="https://chestnut.bot">Chestnut Robotics</a>
</div>
