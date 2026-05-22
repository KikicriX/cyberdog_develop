# XiaomiCup CyberDog 仿真与官方例程使用说明

## 1. 启动基础环境

### 1.1 导入 Docker 镜像

```bash
sudo docker load -i cyberdog_race2026.tar
```

### 1.2 授权 X Server

```bash
xhost +
```

### 1.3 启动容器

```bash
sudo docker run -it --privileged=true \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  cyberdog_sim:v2026
```

### 1.4 安装 Python 例程依赖

```bash
sudo apt update
sudo apt install -y python3-pip
pip3 install lcm toml
```

## 2. 启动仿真

### 2.1 启动 Gazebo

```bash
cd /home/cyberdog_sim
bash src/cyberdog_simulator/cyberdog_gazebo/script/launchgazebo.sh
```
如果需要带激光雷达启动需要：
bash src/cyberdog_simulator/cyberdog_gazebo/script/launchgazebo_lidar.sh

### 2.2 启动控制器

```bash
cd /home/cyberdog_sim
bash src/cyberdog_simulator/cyberdog_gazebo/script/launchcontrol.sh
```
### 2.3启动运动管理模块

如果需要运行官方高层动作、`motion_programs`、`customized_gait` 或调用 `/motion_sequence_cmd`，需要另开一个终端启动运动管理模块：

```bash
cd /home/cyberdog_ws
source /opt/ros/galactic/setup.bash
source /home/cyberdog_ws/install/setup.bash
ros2 run motion_manager motion_manager
```
### 2.4 启动 RViz

```bash
cd /home/cyberdog_sim
bash src/cyberdog_simulator/cyberdog_gazebo/script/launchvisual.sh
```

## 3. 每个新终端先 source

```bash
source /opt/ros/galactic/setup.bash
source /home/cyberdog_ws/install/setup.bash
source /home/cyberdog_sim/install/setup.bash
```

## 4. 相机话题说明

当前已经添加两个 RGB 相机：

```text
/front_rgb_camera/front_rgb_camera_sensor/image_raw   # 原始前视角，用于第二关看球
/down_rgb_camera/down_rgb_camera_sensor/image_raw     # 俯视角 0.45，用于第三关看黄线/地面
```

查看相机话题：

```bash
ros2 topic list | grep camera
```

期望看到：

```text
/front_rgb_camera/front_rgb_camera_sensor/camera_info
/front_rgb_camera/front_rgb_camera_sensor/image_raw
/down_rgb_camera/down_rgb_camera_sensor/camera_info
/down_rgb_camera/down_rgb_camera_sensor/image_raw
```

## 5. 打开相机画面

先设置 X11 显示环境：

```bash
export QT_X11_NO_MITSHM=1
export GDK_DISABLE_SHM=1
export NO_AT_BRIDGE=1
```

打开前视相机：

```bash
ros2 run image_tools showimage --ros-args \
  -p reliability:=best_effort \
  --remap image:=/front_rgb_camera/front_rgb_camera_sensor/image_raw
```

打开俯视相机：

```bash
ros2 run image_tools showimage --ros-args \
  -p reliability:=best_effort \
  --remap image:=/down_rgb_camera/down_rgb_camera_sensor/image_raw
```


## 6. 查询和设置机器狗位置

查询机器狗位置：

```bash
ros2 service call /gazebo/get_entity_state gazebo_msgs/srv/GetEntityState "{name: 'robot', reference_frame: 'world'}"
```

设置机器狗位置：

```bash
ros2 service call /gazebo/set_entity_state gazebo_msgs/srv/SetEntityState "{state: {name: 'robot', pose: {position: {x: 2.751, y: 0.985, z: 0.25}, orientation: {x: 0.0, y: 0.0, z: 0.4778, w: 0.8785}}, twist: {linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}, reference_frame: 'world'}}"
```

## 7. 脚本中调用不同相机

第二关橙色球识别使用前视相机：

```bash
python3 your_second_stage_script.py --ros-args \
  -p image_topic:=/front_rgb_camera/front_rgb_camera_sensor/image_raw
```

第三关黄线识别使用俯视相机：

```bash
python3 your_third_stage_script.py --ros-args \
  -p image_topic:=/down_rgb_camera/down_rgb_camera_sensor/image_raw
```
### 8.使用深度相机
```bash
打开 D435 RGB 画面
export QT_X11_NO_MITSHM=1
export GDK_DISABLE_SHM=1
export NO_AT_BRIDGE=1
```
```bash
ros2 run image_tools showimage --ros-args \
  -p reliability:=best_effort \
  --remap image:=/d435_depth_camera/d435_depth_camera_sensor/image_raw
打开 D435 深度画面

export QT_X11_NO_MITSHM=1
export GDK_DISABLE_SHM=1
export NO_AT_BRIDGE=1

ros2 run image_tools showimage --ros-args \
  -p reliability:=best_effort \
  --remap image:=/d435_depth_camera/d435_depth_camera_sensor/depth/image_raw
