**License:** [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) © 2025 Chestnut Robotics

## Submodules

- [**simulation**](https://github.com/chestnut-robotics/aero-open-sim) — Aero Hand Open simulation models
- [**mujoco_playground**](https://github.com/google-deepmind/mujoco_playground/tree/main/mujoco_playground/_src/manipulation/aero_hand) — Google DeepMind MuJoCo environments which contains buintin RL training support and examples for Aero Hand

## Install

Clone the submodules (takes a while due to mujoco_playground size):

```bash
git submodule sync && git submodule update --init --recursive
```

## Run

See the [online documentation](https://docs.tetheria.ai/docs/hand_sim/) for usage instructions.
