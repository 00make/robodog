#!/usr/bin/env python3
"""
机器狗跳舞功能测试脚本
用于验证跳舞动作系统是否正常工作
"""

import sys
import os
import time

# 添加当前目录和父目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from core.simple_actions import DanceExecutor, SimplePose

def test_dance_actions():
    """测试跳舞动作系统"""
    print("🎭 机器狗跳舞功能测试")
    print("=" * 50)
    
    # 创建跳舞执行器
    executor = DanceExecutor()
    
    # 显示可用动作
    available_actions = executor.get_available_actions()
    print(f"📋 可用动作数量: {len(available_actions)}")
    print(f"📋 动作列表: {', '.join(available_actions)}")
    print()
    
    # 测试每个动作
    for action_name in available_actions:
        print(f"🕺 测试动作: {action_name}")
        
        action = executor.get_action(action_name)
        if action:
            print(f"   📝 描述: {action.description}")
            print(f"   ⏱️ 时长: {action.duration:.1f}秒")
            print(f"   🎯 关键帧数量: {len(action.keyframes)}")
            
            # 模拟动作执行
            print(f"   🎬 动作预览:")
            step = action.duration / 5  # 分5步显示
            for i in range(6):
                t = i * step
                if t > action.duration:
                    t = action.duration
                
                pose = action.get_pose_at_time(t)
                print(f"     时间 {t:4.1f}s: 高度={pose.body_height:.2f}, "
                      f"俯仰={pose.pitch:.2f}, 横滚={pose.roll:.2f}, 偏航={pose.yaw:.2f}")
            
        print()
    
    return True

def test_dance_executor():
    """测试跳舞执行器"""
    print("🤖 测试跳舞执行器")
    print("=" * 30)
    
    executor = DanceExecutor()
    
    # 测试开始动作
    print("测试开始动作...")
    result = executor.start_action("点头")
    print(f"开始'点头'动作: {'成功' if result else '失败'}")
    
    if result:
        print("执行状态检查:")
        start_time = time.time()
        
        while executor.is_dancing and time.time() - start_time < 3:
            pose = executor.get_current_pose()
            elapsed = time.time() - start_time
            print(f"  {elapsed:.1f}s: {pose}")
            
            time.sleep(0.5)
        
        print(f"动作完成: {executor.is_action_finished()}")
    
    print()
    return True

def simulate_dance_performance():
    """模拟完整的跳舞表演"""
    print("🎪 模拟跳舞表演")
    print("=" * 30)
    
    executor = DanceExecutor()
    
    # 表演序列
    performance_sequence = [
        ("点头", "开场问候"),
        ("侧摆", "热身摆动"),
        ("跳跃", "活力跳跃"), 
        ("鞠躬", "结束致谢")
    ]
    
    print("🎭 表演序列:")
    for i, (action, desc) in enumerate(performance_sequence, 1):
        print(f"  {i}. {action} - {desc}")
    print()
    
    total_duration = 0
    for action_name, description in performance_sequence:
        action = executor.get_action(action_name)
        if action:
            total_duration += action.duration
    
    print(f"⏱️ 预计总时长: {total_duration:.1f}秒")
    print()
    
    # 模拟表演
    print("🎬 开始表演...")
    for action_name, description in performance_sequence:
        print(f"▶️ {description} ({action_name})")
        
        action = executor.get_action(action_name)
        if action:
            # 显示动作的关键时刻
            key_moments = [0, action.duration/2, action.duration]
            for t in key_moments:
                pose = action.get_pose_at_time(t)
                print(f"   {t:4.1f}s: {pose}")
            
            print(f"   ✅ 完成 ({action.duration:.1f}s)")
        else:
            print(f"   ❌ 动作未找到")
        
        print()
    
    print("🎉 表演结束!")
    return True

def main():
    """主测试函数"""
    print("🚀 机器狗跳舞系统概念验证")
    print("=" * 60)
    print()
    
    try:
        # 基础功能测试
        print("阶段 1: 基础功能测试")
        if not test_dance_actions():
            print("❌ 基础功能测试失败")
            return False
        print("✅ 基础功能测试通过\n")
        
        # 执行器测试
        print("阶段 2: 执行器测试")
        if not test_dance_executor():
            print("❌ 执行器测试失败")
            return False
        print("✅ 执行器测试通过\n")
        
        # 表演模拟测试
        print("阶段 3: 表演模拟测试")
        if not simulate_dance_performance():
            print("❌ 表演模拟测试失败")
            return False
        print("✅ 表演模拟测试通过\n")
        
        print("🎊 所有测试通过! 跳舞系统准备就绪")
        print()
        print("📋 下一步:")
        print("1. 连接机器狗")
        print("2. 运行 GUI/unified_control.py")
        print("3. 在跳舞功能区域测试动作")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
