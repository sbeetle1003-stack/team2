#!/usr/bin/env bash
set -eo pipefail

source /opt/ros/jazzy/setup.bash
source /home/ju/kong_manipulator2026/open_manipulator_ws/install/setup.bash
source /home/ju/kong_manipulator2026/kong_ws/install/setup.bash

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ros2 launch "${script_dir}/launch/crop_active_vision.launch.py" "$@"
