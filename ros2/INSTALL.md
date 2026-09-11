# Installation Guide (All Packages)

This repo is a ROS 2 workspace that contains multiple packages. Follow the base
setup once, then install any optional dependencies for the packages you plan to
use.

## Base prerequisites

- Ubuntu 22.04
- ROS 2 Humble ([Ubuntu install instructions](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html))
- `colcon` build tools:
  ```bash
  sudo apt install python3-colcon-common-extensions
  ```
- `rosdep`:
  ```bash
  sudo apt install python3-rosdep
  sudo rosdep init || true
  rosdep update
  ```

## Clone the workspace

If you haven't already:

```bash
git clone https://github.com/chestnut-robotics/aero-hand-open
cd aero-hand-open
cd ros2
```

## Build (all packages)

```bash
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

If you only need a subset of packages, you can build selectively, for example:
```bash
colcon build --packages-select aero_hand_open_msgs aero_hand_open
```

## Python Dependencies (Optional)

Only install these if you need the corresponding packages.

### Teleop + Retargeting (Manus/Mediapipe/Apple Vision Pro)

```bash
python3 -m pip install -r requirements.txt
```

Notes:
- `torch`/`torchvision` are large and may require a matching CUDA build.
- `dex_retargeting` is pulled via pip by the requirements above.

### Aero Hand SDK (Required for Hardware Control)

The hardware node (`aero_hand_open`) and the RL package require the Aero Hand SDK.
Follow the SDK install guide:
[Aero Hand SDK installation guide](https://github.com/chestnut-robotics/aero-hand-open/tree/main/sdk)

## Package-Specific Extras

- `manus_ros2` / `manus_ros2_msgs`
  - Follow `src/manus_glove_pkg/README.md` for the Manus SDK and udev rules.
- `aero_hand_open_retargeting`
  - Manus teleop requires the Manus SDK.
  - Apple Vision Pro teleop uses the `avp-stream` Python package (installed by `requirements.txt`).
  - Dex retargeting requires `dex_retargeting` (pip) and `aero_open_sdk`.
- `aero_hand_open_rl`
  - Requires external repos listed in `src/aero_hand_open_rl/README.md`.

## Quick Package Map

- `aero_hand_open_msgs`: ROS 2 message definitions.
- `aero_hand_open`: Hardware interface node (requires Aero Hand SDK).
- `aero_hand_open_description`: URDF + RViz assets.
- `aero_hand_open_retargeting`: Teleoperation + retargeting nodes.
- `manus_glove_pkg/*`: Manus glove ROS 2 packages.
- `aero_hand_open_rl`: RL policy deployment.
