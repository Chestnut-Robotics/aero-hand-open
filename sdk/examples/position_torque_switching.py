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

import time
from aero_open_sdk.aero_hand import AeroHand

if __name__ == "__main__":
    hand = AeroHand() 

    # Note: This example combines both position and torque control modes. The hand will switch between position control and torque control every 10 seconds.
    # In position control mode, the fingers will move back and forth keeping the thumb at open position, while in torque control mode, the hand will simulate a handshake by varying torque values.
    # We recommend adjusting the time.sleep() values to change the speed of movements and torque variations as per your requirements and to observe the effects clearly.
    # We recommend to use switching only when necessary as frequent switching may lead to unexpected behavior and if the hand is not responding as expected, please restart the program and try to do homing before switching modes.

    mode = "position"  # Start in position control mode
    mode_switch_interval = 10  # seconds
    last_switch = time.time()

    # Position control variables
    i = 0
    dir_pos = 1
    # Torque control variables
    torque = 0
    dir_torque = 1

    print("Starting in POSITION control mode. Switching every 10 seconds.")
    while True:
        now = time.time()
        if now - last_switch > mode_switch_interval:
            mode = "torque" if mode == "position" else "position"
            last_switch = now
            print(f"Switched to {mode.upper()} control mode.")

        if mode == "position":
            finger_joint_ranges = [
                ul - ll for ul, ll in zip(hand.joint_upper_limits, hand.joint_lower_limits)
            ]
            joint_pos = [0.0] * 4 + [finger_joint_ranges[4 + j] * i / 100.0 for j in range(12)]
            hand.set_joint_positions(joint_pos)
            if dir_pos == 1:
                i += 1
                if i >= 100:
                    dir_pos = -1
            else:
                i -= 1
                if i <= 0:
                    dir_pos = 1
            time.sleep(0.01)
        else:
            # Sweep torque value for all 7 actuators from 0 to 1000 and back
            torque_list = [torque] * 7
            hand.ctrl_torque(torque_list)
            if dir_torque == 1:
                torque += 1
                if torque >= 700:
                    dir_torque = -1
                    time.sleep(2)  # Pause at max torque
            else:
                torque -= 1
                if torque <= 0:
                    dir_torque = 1
                    time.sleep(2)  # Pause at min torque
            time.sleep(0.002)  # 2 seconds for full sweep