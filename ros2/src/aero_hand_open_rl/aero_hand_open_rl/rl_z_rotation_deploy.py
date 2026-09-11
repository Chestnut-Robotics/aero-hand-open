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

#!/usr/bin/env python3
"""
Minimal ROS 2 node: rl_z_rotation_deploy.py

Usage:
  ros2 run <your_package_name> rl_z_rotation_deploy
"""

import rclpy
from rclpy.node import Node

import time
import jax.numpy as jp
from aero_hand_open_msgs.msg import ActuatorStates, ActuatorControl
from aero_hand_open_rl.utils.sim_to_real_mappings import (
    actuation_array_to_sim_array,
    sim_array_to_actuation_array,
)
import jax.numpy as jp
import numpy as np

import jax
from brax.io import model
from brax.training.agents.ppo.train import train as ppo_train
from brax.training.agents.ppo import networks as ppo_networks

from mujoco_playground import registry, wrapper
from mujoco_playground.config import manipulation_params

import functools

OPEN_PALM = [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
]


class RLZRotationDeploy(Node):
    """Empty template node for RL Z-axis rotation deployment."""

    def __init__(self):
        super().__init__("rl_z_rotation_deploy")
        self.get_logger().info("rl_z_rotation_deploy node started.")
        self.declare_parameter("start_duration", 1.5)
        self.declare_parameter("dt", 0.05)

        self.declare_parameter(
            "action_scale", [0.026, 0.026, 0.026, 0.024, 0.7, 0.003, 0.012]
        )
        self.declare_parameter(
            "DEFAULT_CTRL", [0.083, 0.082, 0.082, 0.086, 0.75, 0.035, 0.1]
        )
        self.declare_parameter(
            "model_path",
            "src/aero_hand_open_rl/aero_hand_open_rl/ppo_TetheriaCubeRotateZAxisTendon_20250926_152920",
        )
        self.declare_parameter("env_name", "AeroCubeRotateZAxis")

        start_duration = self.get_parameter("start_duration").value
        self.dt = self.get_parameter("dt").value
        self.action_scale = jp.array(
            self.get_parameter("action_scale").value, dtype=jp.float32
        )

        self.DEFAULT_CTRL = jp.array(
            self.get_parameter("DEFAULT_CTRL").value, dtype=jp.float32
        )

        self.model_path = self.get_parameter("model_path").value
        self.env_name = self.get_parameter("env_name").value

        env = registry.load(self.env_name)
        ppo_params = manipulation_params.brax_ppo_config(self.env_name)
        network_factory_config = ppo_params.get("network_factory", {})

        del ppo_params["network_factory"]

        network_factory = functools.partial(
            ppo_networks.make_ppo_networks, **network_factory_config
        )

        if "num_timesteps" in ppo_params:
            del ppo_params["num_timesteps"]

        make_inference_fn, _, _ = ppo_train(
            environment=env,
            wrap_env_fn=wrapper.wrap_for_brax_training,
            network_factory=network_factory,
            num_timesteps=0,
            seed=1,
            **ppo_params,
        )

        params = model.load_params(self.model_path)
        self.jit_inference_fn = jax.jit(make_inference_fn(params, deterministic=True))

        self.rng = jax.random.PRNGKey(14)

        self.latest_actuation_commanded = sim_array_to_actuation_array(
            self.DEFAULT_CTRL
        )
        self.latest_actuation_readed = self.latest_actuation_commanded

        self.last_action = jp.zeros(
            len(self.latest_actuation_commanded), dtype=jp.float32
        )

        # === Publisher: right/actuator_control ===
        self.pub = self.create_publisher(ActuatorControl, "right/actuator_control", 10)

        # === Subscriber: right/actuator_states ===
        self.sub = self.create_subscription(
            ActuatorStates,
            "right/actuator_states",
            self.actuator_states_callback,
            10,
        )

        self.timer = self.create_timer(self.dt, self.timer_callback)

        self.publish_actuation_positions(self.latest_actuation_commanded)
        self.get_logger().info(
            f"Set initial actuations and wait for {start_duration} seconds to put the cube in the center"
        )
        time.sleep(start_duration)

    def timer_callback(self):

        if self.latest_actuation_commanded is None:
            self.get_logger().info("No latest actuations")
            return

        self.publish_actuation_positions(self.latest_actuation_commanded)

        latest_tendon_readed = actuation_array_to_sim_array(
            self.latest_actuation_readed
        )

        tendon_lengths_obs = jp.zeros((len(latest_tendon_readed),), dtype=jp.float32)
        for idx, v in enumerate(latest_tendon_readed):
            tendon_lengths_obs = tendon_lengths_obs.at[idx].set(v)
        obs = get_obs(tendon_lengths_obs, self.last_action)
        act_rng, self.rng = jax.random.split(self.rng)
        action = np.array(self.jit_inference_fn(obs, act_rng)[0])

        latest_tendon_commanded = self.DEFAULT_CTRL + action * self.action_scale
        latest_actuation_commanded = sim_array_to_actuation_array(
            latest_tendon_commanded
        )
        self.latest_actuation_commanded = latest_actuation_commanded
        self.last_action = action

    def actuator_states_callback(self, msg: ActuatorStates):
        self.get_logger().info(
            f"Latest actuation readed: {self.latest_actuation_readed}"
        )

        self.latest_actuation_readed = msg.actuations

    def publish_actuation_positions(self, actuation_positions: list):

        actuation_positions_np = np.asarray(
            jax.device_get(actuation_positions), dtype=np.float32
        ).ravel()

        actuation_position_list = actuation_positions_np.tolist()

        self.get_logger().info(f"Latest actuation commanded: {actuation_positions_np}")
        actuation_msg = ActuatorControl()
        actuation_msg.header.stamp = self.get_clock().now().to_msg()
        actuation_msg.actuation_positions = actuation_position_list
        self.pub.publish(actuation_msg)


def get_obs(sim, last_action):

    sensor_data = jp.zeros(len(sim), dtype=jp.float32)

    for idx in range(len(sim)):
        v = jp.ravel(sim[idx])[0]
        sensor_data = sensor_data.at[idx].set(v)

    idx_reorder = jp.array([0, 1, 2, 3, 5, 6, 4])  # reorder
    sensor_data_reordered = sensor_data[idx_reorder]

    last_action_sim7 = jp.asarray(last_action, dtype=jp.float32)

    obs = {"state": np.concatenate([sensor_data_reordered, last_action_sim7])}
    return obs


def main(args=None):
    rclpy.init(args=args)
    node = RLZRotationDeploy()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.hand.set_actuations(OPEN_PALM)
    finally:
        node.hand.set_actuations(OPEN_PALM)
        node.get_logger().info("Shutting down rl_z_rotation_deploy node.")
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
