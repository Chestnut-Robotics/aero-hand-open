<p align="center">
  <img alt="Aero Hand Open by Chestnut Robotics" src="assets/logo.png" width="30%">
  <br/><br/>
</p>

<div align="center">

[![Python Version](https://img.shields.io/pypi/pyversions/aero-open-sdk)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/aero-open-sdk)](https://pypi.org/project/aero-open-sdk/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/pypi/status/aero-open-sdk)](https://pypi.org/project/aero-open-sdk/)
[![Build](https://img.shields.io/github/actions/workflow/status/chestnut-robotics/aero-open-sdk/test.yml?branch=main)](https://github.com/chestnut-robotics/aero-open-sdk/actions)
[![Chestnut Robotics](https://img.shields.io/badge/Developed%20by-Chestnut%20Robotics-0A66C2)](https://chestnut.bot)

</div>

<h2 align="center">
  <p>Aero Open SDK — Python interface for Chestnut Robotics’ Aero Hand Open</p>
</h2>

<div align="center">
  <img src="assets/banner.jpg" alt="Aero Hand Demo" title="Aero Hand in action" width="70%"/>
  <p><strong>Aero Open Hand</strong> is a 7-DoF tendon-driven robotic hand for dexterous manipulation and research.</p>
  <p>The SDK enables full control via Python. Perform homing, calibration, and precise motion control with ease.</p>
</div>

---

## ⚙️ Installation

The SDK is currently tested for Python 3.10 and above.

### 📦 Install via pip

```bash
pip install aero-open-sdk
```

### 🧩 Install from source (editable mode)

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/chestnut-robotics/aero-hand-open.git
   ```

2. Navigate to the cloned repository directory:
   ```bash
   cd sdk
   ```

3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

---

## 🖥️ One-Time Setup

When setting up your hand for the first time, our setup GUI helps you configure motor IDs and test motor connections.

After installation, launch the Setup GUI with:

```bash
aero-open-gui
```

This provides an interactive interface to configure your hand.

---

## 🔌 Serial Port Setup

Aero Hand connects to the host PC via a serial (USB) interface.
To operate the SDK, you must specify the correct serial port for your device.

### 🐧 Linux

Most Linux systems assign the device path as `/dev/ttyACM0` or `/dev/ttyUSB0`. You can list connected serial devices with:

```bash
ls /dev/ttyACM* /dev/ttyUSB*
```

**💡 Persistent Device Path (Recommended)**

Device names like `/dev/ttyUSB0` can change each time you reconnect.

To get a persistent name, use the by-id symlink instead:

```bash
ls -l /dev/serial/by-id/
```

This will show you a list of connected serial devices with more descriptive names. Look for the one that corresponds to your Aero Hand. Which will look something like:
```bash
usb-Espressif_USB_JTAG_serial_debug_unit_D8:3B:DA:45:C8:1C-if00
```
Then initialize your hand using that path:
```python
from aero_open_sdk.aero_hand import AeroHand

aero_hand = AeroHand(
  port="/dev/serial/by-id/usb-Espressif_USB_JTAG_serial_debug_unit_D8:3B:DA:45:C8:1C-if00"
)
```
✅ This ensures your connection always points to the correct device, even if you unplug and replug the hand or change the USB port.

### 🪟 Windows
On Windows, the device will appear as a COM port like `COM3` or `COM4`. You can find the correct COM port by checking the Device Manager under "Ports (COM & LPT)".

You can then Initialize your hand with the detected COM port:
```python
from aero_open_sdk.aero_hand import AeroHand
aero_hand = AeroHand(port="COM3")
```
**💡 Making the COM Port Persistent**

Windows does not have a /by-id/ system like Linux, so the COM number can change if you plug the device into a different USB port.

To make it permanent, you can assign a fixed COM number:
1. Plug in the Aero Hand and open Device Manager.
2. Find it under Ports (COM & LPT).
3. Right-click → Properties → Port Settings → Advanced.
4. In COM Port Number, select an unused port (e.g., COM5).
5. Click OK to save.

You can now always use this COM port when initializing the SDK.

---


## 💡 Examples

To integrate the SDK into your own code, refer to the `examples` folder for sample files demonstrating basic usage.

---

## 🧰 Troubleshooting

### 1. Installation Fails (`pip install` error)

If installation fails, try the following steps:

- Check your Python version:

    Make sure you have Python 3.10 or higher installed.

- 🔧 Upgrade pip to the latest version:

    Our package requires an up-to-date version of pip.

    You can upgrade pip with:
    ```bash
    pip install --upgrade pip
    ```

On Windows, if you see error like "pip is not recognized", use the `py` launcher command instead:

    ```bash
    py -m pip install --upgrade pip
    ```

### 2. Path Mismatch on Windows

- You may not have the Python Scripts path added to your system PATH environment variable.

- To fix this, you can either:

  1. Add the Python Scripts directory (e.g., `C:\Users\<YourName>\AppData\Local\Programs\Python\Python310\Scripts`) to your system PATH.
  2. Or use the `py` launcher command to launch the GUI after installation:
      ```bash
      py -m aero_open_sdk
      ```
  3. Create a virtual environment and install the package there.
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      pip install aero-open-sdk
      aero-open-gui
      ```

### 3. Linux Troubleshooting: Serial Port Permission

If you see a permission error when connecting to the serial port (e.g., `/dev/ttyACM0`), do the following:

1. Find your username:
   ```sh
   whoami
   ```
2. Add your user to the `dialout` group (replace `yourusername` with the output from `whoami`):
   ```sh
   sudo usermod -a -G dialout yourusername
   ```
3. **Restart your system** (or log out and log back in).
4. After restart, open a terminal and run:
   ```sh
   groups
   ```
   You should see your username and `dialout` listed.
5. Try connecting to the serial port again in the GUI.

If you still see permission errors, check device permissions with:
```sh
ls -l /dev/ttyACM0
```
You may need to temporarily set permissions:
```sh
sudo chmod 666 /dev/ttyACM0
```

## 💬 Support

If you encounter issues or have feature requests:
- Open a [GitHub Issue](https://github.com/chestnut-robotics/aero-hand-open/tree/main/sdk/issues)
- Contact us at **contact@chestnut.bot**

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