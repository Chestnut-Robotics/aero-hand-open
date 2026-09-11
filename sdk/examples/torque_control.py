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

from aero_open_sdk.aero_hand import AeroHand

if __name__ == "__main__":
    hand = AeroHand()

    # Try to move the fingers after executing this program. 
    # The fingers will move if you apply torque to them.
    # without applying torque, the fingers move back to the half closed position.
    torque = 100  # from 0 to 1000
    torque_list = [torque] * 7
    print("Torque set to 100")
    try:
        while True:
            hand.ctrl_torque(torque_list)
    except KeyboardInterrupt:
        pass
    # Set the joint positions to 0 when the program is interrupted.
    hand.set_joint_positions([0.0] * 16)
    hand.close()
    print("Joint positions set back to 0")
