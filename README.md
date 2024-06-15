# wanderbot

### **my ROS2 robot car project**

2024/06/15

### 1.底盤測試

#### 機器人端

````bash
ros2 launch ros2_stm32_bridge driver.launch.py
````

#### 本機端

```bash
rviz2
```

---

### 2. 機器人 URDF 顯示於 RViz2

#### 機器人端

```bash
ros2 launch wanderbot4W_description wanderbot.launch.py
```

#### 本地端

```bash
rviz2
```

- 選擇 `base_link`
- Add `robotModel` -> `robot_descrption`

---

### 3. 相機測試

#### 機器人端

```bash
ros2 run usb_cam usb_cam_node_exe --ros-args --params-file /home/sunrise/wanderbot/src/wanderbot_integrate/camera_config/usb_cam.yaml
```

#### 本機端

```bash
rviz2
```

---

### 4.底盤測試

#### 機器人端

```bash
ros2 launch ros2_stm32_bridge driver.launch.py
```

#### 本機端

```bash
rviz2
```
