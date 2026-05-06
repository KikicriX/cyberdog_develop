# my_loco_example

该目录对应容器中的项目目录：

```bash
/home/loco_example/loco_hl_example
```

该目录主要保存 CyberDog 高层运动控制、手动调试、激光感知相关的脚本和配置文件。

## 目录说明

| 目录 | 作用 |
|---|---|
| `basic_motion/` | 原始基础动作示例 |
| `customized_gait/` | 原始自定义步态示例 |
| `sequential_motion/` | 顺序动作执行与手动控制脚本 |
| `scripts/` | 激光感知、环境初始化等辅助脚本 |
| `motion_programs/` | 动作程序库 |



### 运行位置

在容器中进入：

```bash
cd /home/loco_example/loco_hl_example/sequential_motion
```

### 运行命令

```bash
python3 manual_drive.py
```

### 按键说明

| 按键 | 作用 |
|---|---|
| `r` | 恢复站立 |
| `w` | 增加前进速度 |
| `s` | 减小前进速度 / 后退 |
| `a` | 左转 |
| `d` | 右转 |
| `q` | 左移 |
| `e` | 右移 |
| `space` | 速度清零 |
| `z` | 阻尼停止 |
| `Ctrl+C` | 阻尼停止并退出 |
