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

    i = 0
    dir = 1
    while True:
        ## Stagnant thumb + Move Fingers
        finger_joint_ranges = [
            ul - ll for ul, ll in zip(hand.joint_upper_limits, hand.joint_lower_limits)
        ]
        joint_pos = [0.0] * 4 + [
            finger_joint_ranges[4 + j] * i / 100.0 for j in range(12)
        ]
        hand.set_joint_positions(joint_pos)
        if dir == 1:
            i += 1
            if i >= 100:
                dir = -1
        else:
            i -= 1
            if i <= 0:
                dir = 1
        time.sleep(0.01)
