# 机器狗统一控制中心 - 快速安装指南

## 🚀 一键启动

### Windows用户
1. 双击 `start.bat` 文件
2. 脚本会自动检查依赖并启动程序

### Linux/macOS用户
1. 打开终端，进入GUI文件夹
2. 运行启动脚本：
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

## 📦 手动安装

### 1. 检查Python版本
确保安装了Python 3.7或更高版本：
```bash
python --version
```

### 2. 安装依赖
在项目根目录运行：
```bash
pip install -r requirements.txt
```

### 3. 运行程序
```bash
cd GUI
python unified_control.py
```

## 🎮 支持的设备

### 键盘
- ✅ 所有标准键盘
- ✅ 即按即走控制
- ✅ 组合按键支持

### 游戏手柄
- ✅ Xbox 360/One/Series X|S
- ✅ PlayStation 3/4/5
- ✅ 通用USB游戏手柄
- ✅ 蓝牙游戏手柄

### 鼠标
- ✅ GUI按钮控制
- ✅ 触屏设备支持

## 🔧 常见问题

### Q: pygame导入失败
**A:** 运行 `pip install pygame`

### Q: 检测不到手柄
**A:** 
1. 确保手柄驱动已安装
2. 重新插拔手柄
3. 点击"刷新手柄"按钮

### Q: 键盘控制无响应
**A:**
1. 确保键盘监听已启动
2. 点击程序窗口获得焦点
3. 检查是否选择了键盘控制模式

### Q: 无法连接机器狗
**A:**
1. 检查机器狗是否开机
2. 确认IP地址正确
3. 检查网络连接

## 📞 技术支持

如遇问题，请查看：
1. `README.md` - 详细使用说明
2. `config_example.ini` - 配置参数说明
3. 程序内的状态日志

## 🎯 快速上手

1. **启动程序** → 运行 `start.bat` (Windows) 或 `start.sh` (Linux/macOS)
2. **连接机器狗** → 输入IP地址，点击连接
3. **选择控制模式** → 键盘/手柄/GUI按钮
4. **开始控制** → 点击"开始控制"按钮
5. **享受操控** → 使用选定的方式控制机器狗！

---
**提示：** 首次使用建议先阅读完整的 `README.md` 文档。
