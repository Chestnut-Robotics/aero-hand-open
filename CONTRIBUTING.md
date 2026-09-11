# Contributing to Aero Hand Open

Thanks for helping us push affordable, tendon-driven manipulation forward. This repository combines hardware, firmware, ROS 2, SDK, and documentation assets, so we ask contributors to follow the guidelines below to keep changes focused, testable, and easy to review.

## Community Expectations
- Be respectful, welcoming, and safety minded. Engineering discussions can be direct, but they must remain considerate.
- Default to transparency: document decisions, list trade-offs, and share limitations so others can build on your work.
- Mind safety-critical changes. If a modification can affect actuators, wiring, or user safety, call it out explicitly in the pull request (PR).

## Before You Start
- Review the `README.md`, published documentation (https://docs.tetheria.ai/), and existing issues/discussions to confirm the idea has not already been addressed.
- For substantial features, open a GitHub issue or discussion to align on scope before you invest heavy effort.
- By contributing, you agree that your work will be released under the same licenses as the rest of the project:
  - Software (SDK, firmware, ROS 2 code): Apache 2.0
  - Hardware designs, CAD, BOMs, assembly docs: CC BY-NC-SA 4.0

## Repository Tour
- `sdk/` – Python SDK and CLI for controlling the hand.
- `firmware/` – ESP32-S3 Arduino sketch, headers, and assets.
- `ros2/` – ROS 2 packages for messages, teleoperation, and RL experiments.
- `hardware/` – CAD files, printable STLs, BOM, and assembly resources.

## Contribution Workflow
1. Fork the repository and work in a feature branch (`feature/topic-short-description`).
2. Keep commits cohesive and well-described; rebase on the latest `main` before opening a PR.
3. Document any behavioral changes and note follow-on work you intentionally leave out.
4. Run the relevant checks (see sections below) and include the command output or a short summary in the PR description.
5. Draft releases (version bumps, firmware images, SDK publishes) are coordinated with maintainers—please do not push tags or publish packages on your own.


## Testing Expectations
- Mention in the PR description what you tested and how.

## Pull Request Checklist
- The PR has a clear title and links to the related issue/discussion.
- Scope is minimal—unrelated refactors should be split into a separate PR.
- Tests and linting pass locally.
- Documentation, examples, and BOM entries reflect the change.
- Include migration notes or upgrade steps when you impact existing users.

## Getting Help

**GitHub Issues** – Bugs + feature requests only.
- [Open an issue](https://github.com/chestnut-robotics/aero-hand-open/issues)

**GitHub Discussions** –
- Build / electronics / mechanical help
- SDK / ROS2 / sim/RL "how do I…"
- Design proposals and feedback
- [Join discussions](https://github.com/chestnut-robotics/aero-hand-open/discussions)

**Discord** –
- Quick questions, live debugging, voice/screen‑share
- Social chat, lab intros, "I printed my first hand!"
- Live events and office hours
- [Join Discord](http://discord.gg/ZQKWK7NebQ)

**Email** – For sensitive issues (security, safety, licensing), reach out via support@chestnut.bot or the maintainer emails listed in the SDK metadata.

We are excited to collaborate. Thanks for making Aero Hand Open better!
