# RoboDog SDK

[English](README.md) | [中文](README_zh.md)

AlphaDog 机器狗 Python SDK，提供简单直观的编程接口。

## 安装

```bash
pip install robodog
```

## 快速开始

1. 确保您的电脑与机器狗在同一网络下
2. 记录机器狗的 IP 地址（默认：10.10.10.10）

### 基本示例

```python
from robodog import Dog

# 使用默认IP连接机器狗
with Dog() as dog:

    # 调整站立高度
    dog.body_height=0.25
    time.sleep(2)
    
    # 恢复默认高度
    dog.set_parameters({'body_height': 0.23})
```

## 核心功能

* 切换用户模式（普通、安静、儿童等）
* 调整身体姿态（高度、倾斜等）
* 实时状态监控

查看 `examples` 目录获取更多示例。

### 贡献代码

欢迎提交 Issue 和 Pull Request。如需重大变更，请先开 Issue 讨论您的建议。

### 许可证

本项目采用 MIT 许可证 - 详见 `LICENSE` 文件。

### 联系方式

如有问题或建议：

* 提交 GitHub Issues
* 电子邮件：<towardsrwby@gmail.com>
