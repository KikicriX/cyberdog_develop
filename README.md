# cyberdog_develop
开发机器狗
### 1.1 启动仿真

容器内执行：

启动 Gazebo：
```
cd /home/cyberdog_sim
bash src/cyberdog_simulator/cyberdog_gazebo/script/launchgazebo.sh
```
带激光雷达启动：
```
bash src/cyberdog_simulator/cyberdog_gazebo/script/launchgazebo_lidar.sh
```
启动控制器：
```
cd /home/cyberdog_sim
bash src/cyberdog_simulator/cyberdog_gazebo/script/launchcontrol.sh
```

需要可视化时再启动rviz：
```
cd /home/cyberdog_sim
bash src/cyberdog_simulator/cyberdog_gazebo/script/launchvisual.sh
```

每次用终端运行脚本前source环境：
```
source /opt/ros/galactic/setup.bash
source /home/cyberdog_ws/install/setup.bash
```
启动相机画面：
```bash
export QT_X11_NO_MITSHM=1
export GDK_DISABLE_SHM=1

ros2 run image_tools showimage --ros-args \
  -p reliability:=best_effort \
  --remap image:=/rgb_camera/rgb_camera_sensor/image_raw
```

