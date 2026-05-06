#!/usr/bin/env python3
"""Minimal ROS 2 LaserScan front-obstacle observer.

Run this inside the ROS 2 / CyberDog simulation container after Gazebo,
visual, and control are already up:

    python3 scripts/scan_front_obstacle.py

Optional parameters:

    python3 scripts/scan_front_obstacle.py --ros-args \
      -p scan_topic:=/scan \
      -p front_angle_deg:=15.0 \
      -p obstacle_threshold:=1.0 \
      -p print_period:=0.5
"""

import math
from typing import List

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data


class FrontObstacleObserver(Node):
    def __init__(self) -> None:
        super().__init__("front_obstacle_observer")

        self.declare_parameter("scan_topic", "/scan")
        self.declare_parameter("front_angle_deg", 15.0)
        self.declare_parameter("obstacle_threshold", 1.0)
        self.declare_parameter("print_period", 0.5)

        self.scan_topic = (
            self.get_parameter("scan_topic").get_parameter_value().string_value
        )
        self.front_angle_rad = math.radians(
            self.get_parameter("front_angle_deg").get_parameter_value().double_value
        )
        self.obstacle_threshold = (
            self.get_parameter("obstacle_threshold").get_parameter_value().double_value
        )
        self.print_period = (
            self.get_parameter("print_period").get_parameter_value().double_value
        )

        self.latest_front_distance = math.inf
        self.latest_valid_count = 0
        self.latest_total_count = 0
        self.received_scan = False

        self.create_subscription(
            LaserScan, self.scan_topic, self.on_scan, qos_profile_sensor_data
        )

        self.create_timer(self.print_period, self.print_status)

        self.get_logger().info(
            "Listening to %s, front window +/- %.1f deg, obstacle threshold %.2f m"
            % (
                self.scan_topic,
                math.degrees(self.front_angle_rad),
                self.obstacle_threshold,
            )
        )

    def on_scan(self, msg: LaserScan) -> None:
        self.received_scan = True

        if msg.angle_increment == 0.0 or not msg.ranges:
            self.latest_front_distance = math.inf
            self.latest_valid_count = 0
            self.latest_total_count = 0
            return

        start_index = self.angle_to_index(-self.front_angle_rad, msg)
        end_index = self.angle_to_index(self.front_angle_rad, msg)

        start_index = max(0, min(start_index, len(msg.ranges) - 1))
        end_index = max(0, min(end_index, len(msg.ranges) - 1))
        if start_index > end_index:
            start_index, end_index = end_index, start_index

        front_ranges = list(msg.ranges[start_index : end_index + 1])
        valid_ranges = self.filter_valid_ranges(front_ranges, msg)

        self.latest_total_count = len(front_ranges)
        self.latest_valid_count = len(valid_ranges)
        self.latest_front_distance = min(valid_ranges) if valid_ranges else math.inf

    @staticmethod
    def angle_to_index(angle: float, msg: LaserScan) -> int:
        return int(round((angle - msg.angle_min) / msg.angle_increment))

    @staticmethod
    def filter_valid_ranges(ranges: List[float], msg: LaserScan) -> List[float]:
        valid = []
        for distance in ranges:
            if not math.isfinite(distance):
                continue
            if distance < msg.range_min or distance > msg.range_max:
                continue
            valid.append(distance)
        return valid

    def print_status(self) -> None:
        if not self.received_scan:
            self.get_logger().info("Waiting for LaserScan data on %s ..." % self.scan_topic)
            return

        if self.latest_valid_count == 0:
            self.get_logger().info(
                "Front nearest: no valid return | obstacle: no | valid points: 0/%d"
                % self.latest_total_count
            )
            return

        obstacle_detected = self.latest_front_distance <= self.obstacle_threshold
        self.get_logger().info(
            "Front nearest: %.3f m | obstacle: %s | valid points: %d/%d"
            % (
                self.latest_front_distance,
                "yes" if obstacle_detected else "no",
                self.latest_valid_count,
                self.latest_total_count,
            )
        )


def main() -> None:
    rclpy.init()
    node = FrontObstacleObserver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
