"""
GUI跳舞功能快速验证脚本
检查GUI是否能正确加载跳舞模块
"""

import sys
import os

# 添加路径
sys.path.append('.')
sys.path.append('..')

def test_gui_dance_integration():
    """测试GUI与跳舞模块的集成"""
    print("🎮 GUI跳舞功能集成测试")
    print("=" * 50)
    
    try:
        # 测试导入
        print("1. 测试模块导入...")
        from dance.core.simple_actions import DanceExecutor, SimplePose
        print("   ✅ dance模块导入成功")
        
        from GUI.unified_control import RobodogUnifiedGUI
        print("   ✅ GUI模块导入成功")
        
        # 测试GUI初始化（不启动mainloop）
        print("\n2. 测试GUI初始化...")
        app = RobodogUnifiedGUI()
        print("   ✅ GUI初始化成功")
        
        # 检查跳舞执行器是否正确初始化
        print("\n3. 检查跳舞功能集成...")
        if hasattr(app, 'dance_executor') and app.dance_executor:
            print("   ✅ 跳舞执行器已集成")
            actions = app.dance_executor.get_available_actions()
            print(f"   📋 可用动作: {', '.join(actions)}")
        else:
            print("   ❌ 跳舞执行器未正确集成")
            return False
        
        # 检查GUI是否有跳舞相关方法
        print("\n4. 检查GUI跳舞方法...")
        methods_to_check = ['start_dance_action', 'stop_dance_action', 'setup_dance_area']
        for method in methods_to_check:
            if hasattr(app, method):
                print(f"   ✅ {method} 方法存在")
            else:
                print(f"   ❌ {method} 方法缺失")
                return False
        
        print("\n🎉 GUI跳舞功能集成测试通过!")
        print("\n📋 GUI启动指南:")
        print("1. 确保机器狗已连接")
        print("2. 进入GUI目录: cd GUI")
        print("3. 运行GUI: python unified_control.py")
        print("4. 在'🕺 跳舞功能'区域测试动作")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"   ❌ 其他错误: {e}")
        return False

def show_usage_guide():
    """显示使用指南"""
    print("\n" + "=" * 60)
    print("🎯 机器狗跳舞功能使用指南")
    print("=" * 60)
    
    print("\n📍 步骤1: 启动GUI")
    print("   cd GUI")
    print("   python unified_control.py")
    
    print("\n📍 步骤2: 连接机器狗")
    print("   - 输入机器狗IP地址 (默认: 192.168.118.29)")
    print("   - 点击'连接'按钮")
    print("   - 等待连接成功提示")
    
    print("\n📍 步骤3: 测试跳舞功能")
    print("   - 找到'🕺 跳舞功能 (概念验证)'区域")
    print("   - 点击任意动作按钮测试:")
    print("     • 点头 - 1.6秒点头动作")
    print("     • 摇头 - 2.0秒摇头动作") 
    print("     • 跳跃 - 1.2秒跳跃动作")
    print("     • 侧摆 - 2.4秒侧摆动作")
    print("     • 鞠躬 - 1.6秒鞠躬动作")
    print("     • 小跳舞 - 7.0秒组合动作 ⭐")
    
    print("\n📍 步骤4: 安全注意事项")
    print("   - 确保机器狗周围有足够空间")
    print("   - 随时可点击'停止跳舞'按钮")
    print("   - 出现异常时使用'紧急停止'")
    
    print("\n🎪 推荐测试顺序:")
    print("   1. 先测试简单动作: 点头 → 摇头")
    print("   2. 再测试运动动作: 跳跃 → 侧摆")
    print("   3. 最后测试组合动作: 小跳舞")
    
    print("\n📊 动作效果说明:")
    print("   • 点头: 机器狗会前后点头，类似问候")
    print("   • 摇头: 机器狗会左右摇头，类似否定")
    print("   • 跳跃: 先下蹲再跳起，展示活力")
    print("   • 侧摆: 身体左右摆动，优雅舞蹈")
    print("   • 鞠躬: 深度鞠躬，礼貌致敬")
    print("   • 小跳舞: 包含问候、摆动、转圈、跳跃、鞠躬的完整表演")

if __name__ == "__main__":
    success = test_gui_dance_integration()
    
    if success:
        show_usage_guide()
        print(f"\n✨ 概念验证阶段完成! 跳舞系统准备就绪!")
    else:
        print(f"\n❌ 集成测试失败，请检查配置")
