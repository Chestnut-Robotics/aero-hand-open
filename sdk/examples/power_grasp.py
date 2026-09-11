#!/usr/bin/env python3
# Copyright 2025 Chestnut Robotics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This example demonstrates power grasping with the AeroHand using keyboard input.
Press the SPACE key to toggle between open and close grip poses.
"""

import time
from aero_open_sdk.aero_hand import AeroHand

## This example requires the 'pynput' library.
## You can install it via pip:
##     pip install pynput
try:
    from pynput import keyboard
except ModuleNotFoundError:
    raise SystemExit(
        "\nERROR: 'pynput' is not installed.\n"
        "Install it using:\n"
        "    pip install pynput\n"
    )

class KeyboardController:
    """A simple keyboard controller for the AeroHand.
    Press SPACE to toggle between open and grip poses."""
    def __init__(self):
        self.grasped = False

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            if key == keyboard.Key.space:
                self.grasped = not self.grasped
                if self.grasped:
                    print("SPACE pressed: moving to GRIP pose")
                else:
                    print("SPACE pressed: moving to ZERO pose")
        except Exception:
            # Don't let any error in the listener kill the program
            pass

def main():
    hand = AeroHand()

    open_pose = [100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    grip_pose = [100.0, 55.0, 30.0, 60.0, 60.0, 60.0, 60.0]

    controller = KeyboardController()
    speed = 80  # from 0 to 32766
    torque = 400  # from 0 to 1000
    for i in range(7):
        # Manual setting of speed and torque is optional. 
        # When not set, the speed and torque are what was set last time.
        # When you reboot the hand (power off and on), the speed and torque are reset back to the default values.
        # The default speed is 32766 and the default torque is 1000.
        hand.set_speed(i, speed)
        time.sleep(0.01)
        hand.set_torque(i, torque)
        time.sleep(0.01)

    try:
        while True:
            if controller.grasped:
                hand.set_joint_positions(grip_pose)
            else:
                hand.set_joint_positions(open_pose)
            time.sleep(0.01)
    except KeyboardInterrupt:
        controller.listener.stop()
        # Set the joint positions to 0 when the program is interrupted.
        hand.set_joint_positions([0.0] * 16)
        hand.close()
        print("Joint positions set to 0")


if __name__ == "__main__":
    main()