下面是可直接保存为 `README_rockroad.md` 的精简版 Markdown。

```markdown
# CyberDog 石板路通过脚本说明

本文说明 `cross_rockroad2.py` 运行前必须完成的环境准备、验证步骤和主要参数。

## 1. 运行目标

`cross_rockroad2.py` 用于让 CyberDog 在 Gazebo 仿真中自动通过第一关石板路。

脚本主要依赖：

- Gazebo 真实位姿 `/gazebo/model_states`
- LCM 高层运动控制
- 机器人模型名 `robot`

当前脚本不强制依赖相机或激光雷达。

---

## 2. 必须启动的系统

运行脚本前，需要完整启动仿真和控制链：

- Gazebo
- control
- motion manager / 运动控制相关节点

只启动 Gazebo 时，机器人可能不会响应运动命令。

---

## 3. 添加 Gazebo State 插件

在实际使用的 world 文件中，例如：

```bash
/home/cyberdog_sim/src/cyberdog_simulator/cyberdog_gazebo/world/race_new.world
```

在：

```xml
<world name="earth">
```

下面加入：

```xml
<plugin name="gazebo_ros_state" filename="libgazebo_ros_state.so">
    <ros>
        <namespace>/gazebo</namespace>
    </ros>
    <update_rate>50.0</update_rate>
</plugin>
```

修改前建议备份：

```bash
cp race_new.world race_new.world.backup_state_plugin
```

确认插件存在：

```bash
ls /opt/ros/galactic/lib/libgazebo_ros_state.so
```

---

## 4. 验证 Gazebo 位姿服务和话题

重启 Gazebo 后执行：

```bash
source /opt/ros/galactic/setup.bash
source /home/cyberdog_sim/install/setup.bash
source /home/cyberdog_ws/install/setup.bash
```

检查服务：

```bash
ros2 service list | grep get_entity_state
```

应看到：

```bash
/gazebo/get_entity_state
```

检查话题：

```bash
ros2 topic list | grep model_states
```

应看到：

```bash
/gazebo/model_states
```

确认机器人模型名为 `robot`：

```bash
ros2 service call /gazebo/get_entity_state gazebo_msgs/srv/GetEntityState "{name: 'robot', reference_frame: 'world'}"
```

返回中应包含：

```text
success=True
```

---

## 5. LCM Python 路径要求

脚本内部已经加入：

```python
/home/lcm/build/python
/home/loco_example/loco_hl_example/sequential_motion
```

因此一般不需要手动 export。

但需要确保以下文件存在：

```bash
/home/lcm/build/python
/home/loco_example/loco_hl_example/sequential_motion/robot_control_cmd_lcmt.py
```

---

## 6. 运行脚本

脚本路径：

```bash
/home/loco_example/loco_hl_example/scripts/cross_rockroad2.py
```

语法检查：

```bash
python3 -m py_compile /home/loco_example/loco_hl_example/scripts/cross_rockroad2.py
```

推荐运行命令：

```bash
python3 /home/loco_example/loco_hl_example/scripts/cross_rockroad2.py --ros-args \
  -p forward_speed:=0.20 \
  -p step_height:=0.16 \
  -p target_x:=3.00 \
  -p max_time:=50.0
```

---

## 7. 主要参数说明

### `forward_speed`

前进速度。

推荐范围：

```text
0.16 ~ 0.25
```

### `step_height`

抬腿高度。

石板高度约 5cm，建议不要设置过大。

推荐范围：

```text
0.12 ~ 0.18
```

### `target_x`

终点世界坐标 x。

想让机器人通过石板后多走一段，就增大该值。

常用值：

```text
2.85
3.00
3.20
```

### `max_time`

最大运行时间，防止脚本无限运行。

推荐范围：

```text
40 ~ 60 秒
```

### `yaw_deadband`

允许的朝向误差。

推荐范围：

```text
0.05 ~ 0.08
```

### `turn_speed`

摆正朝向时的转向速度。

推荐范围：

```text
0.08 ~ 0.12
```

---

## 8. 调试建议

如果前脚蹭石板：

```text
适当提高 forward_speed
适当调整 step_height
```

如果机器人晃动明显：

```text
降低 forward_speed
降低 step_height
```

如果机器人走歪：

```text
减小 yaw_deadband
适当提高 turn_speed
```

如果通过后停得太早：

```text
增大 target_x
增大 max_time
```

---

## 9. 当前结论

`cross_rockroad2.py` 的核心依赖不是相机或激光，而是：

```text
Gazebo state 插件
/gazebo/model_states
模型名 robot
LCM 控制命令
```

相机和激光可作为调试辅助，但石板路通过脚本当前主要依靠 Gazebo 位姿和 LCM 运动控制完成。
```
