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

    while True:
        actuator_current = hand.get_actuator_currents()
        print("actuator Currents:", actuator_current)
        actuator_positions = hand.get_actuations()
        print("actuator Positions:", actuator_positions)
        actuator_speeds = hand.get_actuator_speeds()
        print("actuator Speeds:", actuator_speeds)
        actuator_temperatures = hand.get_actuator_temperatures()
        print("actuator Temperatures:", actuator_temperatures)
        time.sleep(0.1)
