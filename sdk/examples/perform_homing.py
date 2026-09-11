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

    ## Perform homing
    ## NOTE: While performing homing, robot will not respond to any other commands.
    ## Make sure the hand is in a safe position to perform homing.
    hand.send_homing()
