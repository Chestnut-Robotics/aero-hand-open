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

import os
from pathlib import Path

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

_LAUNCH_ROOT = Path("src") / "launch_files"


def _find_launch_root() -> Path:
    prefix_path = os.environ.get("AMENT_PREFIX_PATH", "")
    for prefix in [p for p in prefix_path.split(os.pathsep) if p]:
        candidate = Path(prefix).parent / _LAUNCH_ROOT
        if candidate.is_dir():
            return candidate

    for parent in Path(__file__).resolve().parents:
        candidate = parent / _LAUNCH_ROOT
        if candidate.is_dir():
            return candidate

    raise RuntimeError("Unable to locate src/launch_files in this workspace.")


def generate_launch_description():
    launch_file = _find_launch_root() / "display_launch" / "display.launch.py"
    if not launch_file.is_file():
        raise RuntimeError(f"Expected launch file not found: {launch_file}")

    return LaunchDescription(
        [IncludeLaunchDescription(PythonLaunchDescriptionSource(str(launch_file)))]
    )
