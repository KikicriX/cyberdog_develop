# cyberdog_develop
开发机器狗
### 1.1 启动仿真

容器内执行：

启动 Gazebo：
cd /home/cyberdog_sim
bash src/cyberdog_simulator/cyberdog_gazebo/script/launchgazebo.sh
带激光雷达启动：bash src/cyberdog_simulator/cyberdog_gazebo/script/launchgazebo_lidar.sh

启动控制器：
cd /home/cyberdog_sim
bash src/cyberdog_simulator/cyberdog_gazebo/script/launchcontrol.sh

需要可视化时再启动rviz：
cd /home/cyberdog_sim
bash src/cyberdog_simulator/cyberdog_gazebo/script/launchvisual.sh

每次用终端运行脚本前source环境：
source /opt/ros/galactic/setup.bash
source /home/cyberdog_ws/install/setup.bash


