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


# utils/sim_to_real_mappings.py
"""
Actuator mapping utilities:
- Convert actuator range of aero hand open <-> MuJoCo tendon length range
- Array-based API (fixed order), avoids dict overhead
"""
from aero_open_sdk.joints_to_actuations import JointsToActuationsModel
from aero_open_sdk.aero_hand_constants import AeroHandConstants

# Index: [index, middle, ring, pinky, thumb_abd, th1, th2]
SIM_RANGE = [
    (0.0617776, 0.107723),  # right_index_A_pip in sim
    (0.0621875, 0.1084),  # right_middle_A_pip in sim
    (0.0616733, 0.10775),  # right_ring_A_pip in sim
    (0.0637823, 0.109504),  # right_pinky_A_pip in sim
    (-0.0254462, 1.77858),  # right_thumb_A_mcp_abd in sim
    (0.026941, 0.0382787),  # right_th1_A_pip in sim
    (0.0839985, 0.110133),  # right_th2_A_pip in sim
]

ACTUATIONS_LOWER_LIMITS = AeroHandConstants.actuation_lower_limits
ACTUATIONS_UPPER_LIMITS = AeroHandConstants.actuation_upper_limits


ACTUATION_RANGE = [
    (
        ACTUATIONS_LOWER_LIMITS[0],
        ACTUATIONS_UPPER_LIMITS[0],
    ),  # right_thumb_A_abd in servo
    (
        ACTUATIONS_LOWER_LIMITS[1],
        ACTUATIONS_UPPER_LIMITS[1],
    ),  # right_thumb_A_flex in servo
    (
        ACTUATIONS_LOWER_LIMITS[2],
        ACTUATIONS_UPPER_LIMITS[2],
    ),  # right_thumb_A_mcp in servo
    (ACTUATIONS_LOWER_LIMITS[3], ACTUATIONS_UPPER_LIMITS[3]),  # right_index in servo
    (ACTUATIONS_LOWER_LIMITS[4], ACTUATIONS_UPPER_LIMITS[4]),  # right_middle in servo
    (ACTUATIONS_LOWER_LIMITS[5], ACTUATIONS_UPPER_LIMITS[5]),  # right_ring in servo
    (ACTUATIONS_LOWER_LIMITS[6], ACTUATIONS_UPPER_LIMITS[6]),  # right_pinky in servo
]

THUMB_ABD_ACTUATION = 0
THUMB_FLEX_ACTUATION = 1
THUMB_MCP_ACTUATION = 2
FINGER_IDX_ACTUATION = 3
FINGER_MIDDLE_ACTUATION = 4
FINGER_RING_ACTUATION = 5
FINGER_PINKY_ACTUATION = 6

THUMB_ABD_SIM = 4
THUMB_FLEX_SIM = 5
THUMB_MCP_SIM = 6
FINGER_IDX_SIM = 0
FINGER_MIDDLE_SIM = 1
FINGER_RING_SIM = 2
FINGER_PINKY_SIM = 3

PI = 3.141592653589793
MOTOR_PULLEY_RADIUS = 9.000  # mm


#### sim to actuation ####


def sim_to_actuation_forward(
    x: float,
    lo: float,
    hi: float,
    min_u: int = ACTUATIONS_LOWER_LIMITS[0],
    max_u: int = ACTUATIONS_UPPER_LIMITS[0],
) -> float:
    """
    ctrl forward mapping: lo -> min_u, hi -> max_u
    """
    if x < lo:
        x = lo
    if x > hi:
        x = hi
    t = (x - lo) / (hi - lo)
    return min_u + t * (max_u - min_u)


def sim_to_actuation_reverse(
    x: float,
    lo: float,
    hi: float,
    min_u: int = ACTUATIONS_LOWER_LIMITS[0],
    max_u: int = ACTUATIONS_UPPER_LIMITS[0],
) -> float:
    """
    ctrl reverse mapping: lo -> max_u, hi -> min_u
    """
    if x < lo:
        x = lo
    if x > hi:
        x = hi
    t = (hi - x) / (hi - lo)
    return min_u + t * (max_u - min_u)


def sim_to_actuation_thumb_mcp(
    sim_abd_joint: float, sim_flex_tendon: float, sim_mcp_tendon: float
) -> float:

    joint_abd = sim_abd_joint

    joint_flex = (
        0.000344 * sim_abd_joint
        - 78.088995 * sim_flex_tendon
        + 0.188440 * sim_mcp_tendon
        + 2.977490
    )
    joint_mcp = (
        0.004162 * sim_abd_joint
        - 11.373921 * sim_flex_tendon
        - 56.722756 * sim_mcp_tendon
        + 6.666491
    )

    joint_ip = (
        0.004528469071365329 * sim_abd_joint
        - 11.422035184164583 * sim_flex_tendon
        - 56.887542891723974 * sim_mcp_tendon
        + 6.687096101625219
    )

    JTA = JointsToActuationsModel()
    JTA_abd, JTA_flex, JTA_mcp = JTA.thumb_actuations(
        joint_abd, joint_flex, joint_mcp, joint_ip
    )

    return JTA_abd / PI * 180, JTA_flex / PI * 180, JTA_mcp / PI * 180


def sim_array_to_actuation_array(sim_arr):

    actuation_arr = [0.0] * len(sim_arr)

    actuation_arr[THUMB_ABD_ACTUATION] = sim_to_actuation_forward(
        sim_arr[THUMB_ABD_SIM],
        SIM_RANGE[THUMB_ABD_SIM][0],
        SIM_RANGE[THUMB_ABD_SIM][1],
        ACTUATION_RANGE[THUMB_ABD_ACTUATION][0],
        ACTUATION_RANGE[THUMB_ABD_ACTUATION][1],
    )  # in degrees

    (
        actuation_arr[THUMB_ABD_ACTUATION],
        actuation_arr[THUMB_FLEX_ACTUATION],
        actuation_arr[THUMB_MCP_ACTUATION],
    ) = sim_to_actuation_thumb_mcp(
        sim_arr[THUMB_ABD_SIM],
        sim_arr[THUMB_FLEX_SIM],
        sim_arr[THUMB_MCP_SIM],
    )

    actuation_arr[FINGER_IDX_ACTUATION] = sim_to_actuation_reverse(
        sim_arr[FINGER_IDX_SIM],
        SIM_RANGE[FINGER_IDX_SIM][0],
        SIM_RANGE[FINGER_IDX_SIM][1],
        ACTUATION_RANGE[FINGER_IDX_ACTUATION][0],
        ACTUATION_RANGE[FINGER_IDX_ACTUATION][1],
    )
    actuation_arr[FINGER_MIDDLE_ACTUATION] = sim_to_actuation_reverse(
        sim_arr[FINGER_MIDDLE_SIM],
        SIM_RANGE[FINGER_MIDDLE_SIM][0],
        SIM_RANGE[FINGER_MIDDLE_SIM][1],
        ACTUATION_RANGE[FINGER_MIDDLE_ACTUATION][0],
        ACTUATION_RANGE[FINGER_MIDDLE_ACTUATION][1],
    )

    actuation_arr[FINGER_RING_ACTUATION] = sim_to_actuation_reverse(
        sim_arr[FINGER_RING_SIM],
        SIM_RANGE[FINGER_RING_SIM][0],
        SIM_RANGE[FINGER_RING_SIM][1],
        ACTUATION_RANGE[FINGER_RING_ACTUATION][0],
        ACTUATION_RANGE[FINGER_RING_ACTUATION][1],
    )
    actuation_arr[FINGER_PINKY_ACTUATION] = sim_to_actuation_reverse(
        sim_arr[FINGER_PINKY_SIM],
        SIM_RANGE[FINGER_PINKY_SIM][0],
        SIM_RANGE[FINGER_PINKY_SIM][1],
        ACTUATION_RANGE[FINGER_PINKY_ACTUATION][0],
        ACTUATION_RANGE[FINGER_PINKY_ACTUATION][1],
    )
    return actuation_arr


#### actuation to sim ####


def actuation_to_sim_forward(
    u: int,
    lo: float,
    hi: float,
    min_u: int = ACTUATIONS_LOWER_LIMITS[0],
    max_u: int = ACTUATIONS_UPPER_LIMITS[0],
) -> float:
    """
    forward mapping:
    - min_u -> lo
    - max_u -> hi
    """
    u = max(min_u, min(max_u, int(u)))
    return lo + (u - min_u) / (max_u - min_u) * (hi - lo)


def actuation_to_sim_reverse(
    u: int,
    lo: float,
    hi: float,
    min_u: int = ACTUATIONS_LOWER_LIMITS[0],
    max_u: int = ACTUATIONS_UPPER_LIMITS[0],
) -> float:
    """
    reverse mapping:
    - min_u -> hi
    - max_u -> lo
    """
    u = max(min_u, min(max_u, int(u)))
    return hi - (u - min_u) / (max_u - min_u) * (hi - lo)


# fitting result: Actuation (cable length) ≈ -977.220399 * flex + 37.517992 + 2.5000 * abd
# fitting result: Actuation (cable length) ≈ -1241.571958 * flex + 136.590025 + 2.5000 * abd


def actuation_to_sim_thumb_cmc_flex(
    actuation_cmc_flex: float, actuation_abd: float
) -> float:

    cable = actuation_cmc_flex / 180 * PI * MOTOR_PULLEY_RADIUS

    res = ((cable - 2.5000 * actuation_abd) - 37.517992) / (-977.220399)

    return res


def actuation_to_sim_thumb_tendon(
    actuation_thumb_tendon: float, actuation_abd: float
) -> float:

    cable = actuation_thumb_tendon / 180 * PI * MOTOR_PULLEY_RADIUS

    res = ((cable - 2.5000 * actuation_abd) - 136.590025) / (-1241.571958)

    return res


def actuation_array_to_sim_array(actuation_arr):
    """
    input: [u0..u6] uint16
    output: [ctrl0..ctrl6] float
    """
    sim_arr = [0.0] * len(actuation_arr)

    sim_arr[THUMB_ABD_SIM] = actuation_to_sim_forward(
        actuation_arr[THUMB_ABD_ACTUATION],
        SIM_RANGE[THUMB_ABD_SIM][0],
        SIM_RANGE[THUMB_ABD_SIM][1],
        ACTUATION_RANGE[THUMB_ABD_ACTUATION][0],
        ACTUATION_RANGE[THUMB_ABD_ACTUATION][1],
    )

    sim_arr[THUMB_FLEX_SIM] = actuation_to_sim_thumb_cmc_flex(
        actuation_arr[THUMB_FLEX_ACTUATION],
        sim_arr[THUMB_ABD_SIM],
    )

    sim_arr[THUMB_MCP_SIM] = actuation_to_sim_thumb_tendon(
        actuation_arr[THUMB_MCP_ACTUATION],
        sim_arr[THUMB_ABD_SIM],
    )

    sim_arr[FINGER_IDX_SIM] = actuation_to_sim_reverse(
        actuation_arr[FINGER_IDX_ACTUATION],
        SIM_RANGE[FINGER_IDX_SIM][0],
        SIM_RANGE[FINGER_IDX_SIM][1],
        ACTUATION_RANGE[FINGER_IDX_ACTUATION][0],
        ACTUATION_RANGE[FINGER_IDX_ACTUATION][1],
    )
    sim_arr[FINGER_MIDDLE_SIM] = actuation_to_sim_reverse(
        actuation_arr[FINGER_MIDDLE_ACTUATION],
        SIM_RANGE[FINGER_MIDDLE_SIM][0],
        SIM_RANGE[FINGER_MIDDLE_SIM][1],
        ACTUATION_RANGE[FINGER_MIDDLE_ACTUATION][0],
        ACTUATION_RANGE[FINGER_MIDDLE_ACTUATION][1],
    )
    sim_arr[FINGER_RING_SIM] = actuation_to_sim_reverse(
        actuation_arr[FINGER_RING_ACTUATION],
        SIM_RANGE[FINGER_RING_SIM][0],
        SIM_RANGE[FINGER_RING_SIM][1],
        ACTUATION_RANGE[FINGER_RING_ACTUATION][0],
        ACTUATION_RANGE[FINGER_RING_ACTUATION][1],
    )
    sim_arr[FINGER_PINKY_SIM] = actuation_to_sim_reverse(
        actuation_arr[FINGER_PINKY_ACTUATION],
        SIM_RANGE[FINGER_PINKY_SIM][0],
        SIM_RANGE[FINGER_PINKY_SIM][1],
        ACTUATION_RANGE[FINGER_PINKY_ACTUATION][0],
        ACTUATION_RANGE[FINGER_PINKY_ACTUATION][1],
    )
    return sim_arr
