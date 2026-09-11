<p align="center">
  <img alt="Aero Hand Open by Chestnut Robotics" src="https://raw.githubusercontent.com/chestnut-robotics/aero-hand-open/main/sdk/assets/logo.png" width="30%">
  <br/><br/>
</p>
 
<div align="center">

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Chestnut Robotics](https://img.shields.io/badge/Developed%20by-Chestnut%20Robotics-0A66C2)](https://chestnut.bot)

</div>

<h2 align="center">
  <p>Aero Hand Open ROS2 — ROS 2 packages for Chestnut Robotics’ Aero Hand Open</p>
</h2>

<div align="center">
  <img src="https://raw.githubusercontent.com/chestnut-robotics/aero-hand-open/main/sdk/assets/banner.jpg" alt="Aero Hand Demo" title="Aero Hand in action" width="70%"/>
  <p><strong>Aero Hand Open</strong> is a 7-DoF tendon-driven robotic hand for dexterous manipulation and research.</p>
</div>

---

## ⚙️ Installation

We currently have tested the ROS2 package on **Ubuntu 22.04** with **ROS2 Humble Hawksbill**.

Follow the instructions in [INSTALL.md](INSTALL.md).

---

## 🚀 Next steps

- Start here: [Launch files overview](src/launch_files/readme.md)
- URDF/RViz visualization: `ros2 launch src/launch_files/display_launch/display.launch.py`
- Teleop launches:
  - Webcam: `src/launch_files/webcam_teleop_launch/readme.md`
  - Apple Vision Pro: `src/launch_files/vision_pro_teleop_launch/readme.md`
  - Manus glove: `src/launch_files/manus_teleop_launch/readme.md`

## 🧰 Troubleshooting
If something isn’t working, check:

- `INSTALL.md` for dependency setup
- `src/launch_files/*/readme.md` for per-launch requirements and arguments

## 💬 Support

If you encounter issues or have feature requests:
- Open a [GitHub Issue](https://github.com/chestnut-robotics/aero-open-ros2/issues)
- Contact us at **support@chestnut.bot**

---

## 🤝 Contribution

We welcome community contributions!

If you'd like to improve the SDK, fix bugs, or add new features:

1. Fork this repository.
2. Create a new branch for your changes.
    ```bash
    git checkout -b feature/your-feature-name
    ```

3. Commit your changes with clear messages.

4. Push your branch to your fork.

5. Open a Pull Request (PR) describing your updates.


---

## ⚖️ License

This project is licensed under the **Apache License 2.0**.


<div align="center">
If you find this project useful, please give it a star! ⭐

Built with ❤️ by Chestnut Robotics
</div>