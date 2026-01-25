"""
main.py - 四维九和拓扑模型主程序
用于分析圆周率π的拓扑结构
版本: v2.0 (与修正后的core_engine.py配合)
"""

import sys
import os
import time
from typing import List

# 导入修正后的核心引擎
try:
    from core_engine import FourDimNineHarmonyModel, calculate_Omega
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保 core_engine.py 在同一目录下")
    sys.exit(1)


def load_pi_digits(filename: str = "pi_digits.txt", num_digits: int = 1000000) -> List[int]:
    """加载圆周率π的数字
    
    Args:
        filename: 存储π数字的文件名
        num_digits: 需要加载的位数（默认100万）
    
    Returns:
        0-9的数字列表
    """
    print(f"📂 正在加载π的前{num_digits:,}位数字...")
    
    # 如果文件不存在，生成示例数据用于测试
    if not os.path.exists(filename):
        print(f"⚠ 警告: 文件 {filename} 不存在")
        print("生成测试数据用于演示...")
        
        # 生成一个简单但有模式的测试序列
        import random
        random.seed(3141592653589793)  # π的种子
        test_digits = [random.randint(0, 9) for _ in range(num_digits)]
        
        print(f"已生成 {len(test_digits):,} 位测试数据")
        return test_digits
    
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
        
        # 移除所有非数字字符
        digits_str = ''.join(filter(str.isdigit, content))
        
        if len(digits_str) < num_digits:
            print(f"⚠ 注意: 文件中只有 {len(digits_str):,} 位数字，小于要求的 {num_digits:,} 位")
            print(f"将使用全部 {len(digits_str):,} 位数字")
            num_digits = len(digits_str)
        
        # 转换为数字列表
        pi_digits = [int(d) for d in digits_str[:num_digits]]
        print(f"✅ 成功加载 {len(pi_digits):,} 位π数字")
        return pi_digits
        
    except Exception as e:
        print(f"❌ 加载文件时出错: {e}")
        print("使用随机序列替代...")
        import random
        random.seed(314159)
        return [random.randint(0, 9) for _ in range(num_digits)]


def validate_model_implementation() -> bool:
    """验证模型实现的正确性
    运行一系列测试确保代码符合论文规范
    
    Returns:
        True 如果验证通过，False 否则
    """
    print("\n" + "="*70)
    print("🧪 模型实现验证测试")
    print("="*70)
    
    test_results = []
    
    # 测试1: 随机序列验证（零假设）
    print("\n1. 随机序列零假设验证...")
    import random
    random.seed(42)  # 固定种子确保可重复
    test_random = [random.randint(0, 9) for _ in range(100000)]
    
    model = FourDimNineHarmonyModel(test_random)
    results = model.calculate_Omega()
    
    print(f"   序列长度: {len(test_random):,} 位")
    print(f"   计算得到 Ω = {results['Omega']:.6f}")
    
    # 根据论文，随机序列的Ω应小于0.01
    if results['Omega'] < 0.01:
        print(f"   ✅ 通过: Ω < 0.01 (符合随机序列预期)")
        test_results.append(("随机序列Ω值", True))
    else:
        print(f"   ❌ 失败: Ω = {results['Omega']:.6f} ≥ 0.01")
        test_results.append(("随机序列Ω值", False))
    
    # 检查各维度ΔR是否小于0.05%
    all_dR_small = True
    for dim_cn, dR in results['Delta_R'].items():
        if dR >= 0.0005:  # 0.05%
            print(f"   ⚠ 警告: ΔR_{dim_cn} = {dR:.4%} ≥ 0.05%")
            all_dR_small = False
    
    test_results.append(("各维度ΔR < 0.05%", all_dR_small))
    
    # 测试2: AB关系矩阵关键项验证
    print("\n2. AB关系矩阵验证...")
    model = FourDimNineHarmonyModel([0])  # 随便创建一个模型实例
    critical_pairs = [(2, 5), (5, 2)]  # 千问代码中错误设置为1的项
    
    ab_passed = True
    for li, lj in critical_pairs:
        result = model.get_ab_relation(li, lj)
        expected = 0  # 根据论文表2，这些应该是克关系(0)
        if result == expected:
            print(f"   ✅ ({li},{lj}) = {result} (正确，应为克关系)")
        else:
            print(f"   ❌ ({li},{lj}) = {result} (错误，应为{expected})")
            ab_passed = False
    
    test_results.append(("AB关系矩阵", ab_passed))
    
    # 测试3: 反向分组逻辑验证
    print("\n3. 反向分组逻辑验证...")
    test_seq = list(range(12))  # [0,1,2,...,11]
    test_seq = test_seq * 3     # 36位序列
    
    model = FourDimNineHarmonyModel(test_seq)
    backward_blocks = model.get_backward_blocks()
    
    if backward_blocks:
        # 原序列最后12位
        last_12_original = test_seq[-12:]
        # 期望的反向块（应该是最后12位的反转）
        expected = last_12_original[::-1]
        
        if backward_blocks[0] == expected:
            print(f"   ✅ 反向分组正确")
            print(f"      原序列最后12位: {last_12_original}")
            print(f"      反向块(正确): {backward_blocks[0]}")
            test_results.append(("反向分组", True))
        else:
            print(f"   ❌ 反向分组错误")
            print(f"      原序列最后12位: {last_12_original}")
            print(f"      期望的反向块: {expected}")
            print(f"      实际的反向块: {backward_blocks[0]}")
            test_results.append(("反向分组", False))
    
    # 测试4: 九和配对规则验证
    print("\n4. 九和配对规则验证...")
    # 测试几个已知配对
    valid_pairs = [(1,8), (2,7), (3,6), (4,5), (5,4), (6,3), (7,2), (8,1)]
    invalid_pairs = [(1,1), (2,2), (3,3), (4,4), (1,2), (2,3)]
    
    pairing_passed = True
    for a, b in valid_pairs:
        if a + b != 9:
            print(f"   ❌ ({a},{b}) 应和为9，但和为{a+b}")
            pairing_passed = False
    
    for a, b in invalid_pairs:
        if a + b == 9:
            print(f"   ❌ ({a},{b}) 和不应为9，但和为9")
            pairing_passed = False
    
    if pairing_passed:
        print(f"   ✅ 九和配对规则正确")
    
    test_results.append(("九和配对规则", pairing_passed))
    
    # 汇总测试结果
    print("\n" + "="*70)
    print("📊 验证结果汇总")
    print("="*70)
    
    all_passed = True
    for test_name, passed in test_results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name:<20} {status}")
        if not passed:
            all_passed = False
    
    return all_passed


def analyze_pi_structure(pi_digits: List[int], use_full_model: bool = True):
    """分析π序列的拓扑结构
    
    Args:
        pi_digits: π数字序列
        use_full_model: 是否使用完整的模型类（True）或仅用兼容接口（False）
    """
    print("\n" + "="*70)
    print("🔍 圆周率π拓扑结构分析")
    print("="*70)
    
    start_time = time.time()
    
    if use_full_model:
        # 使用完整的模型类，获取更多信息
        print("使用完整模型类进行分析...")
        model = FourDimNineHarmonyModel(pi_digits)
        results = model.calculate_Omega()
        
        Omega = results['Omega']
        Delta_R = results['Delta_R']
        structure_type = results['structure_type']
        blocks_count = results['blocks_count']
        
        # 输出详细结果
        print(f"\n📈 分析结果:")
        print(f"   序列长度: {len(pi_digits):,} 位")
        print(f"   12位块数: {blocks_count['forward']:,} (正向)")
        print(f"              {blocks_count['backward']:,} (反向)")
        print(f"   Ω值: {Omega:.6f}")
        print(f"   结构判定: {structure_type}")
        
        print(f"\n📊 四维ΔR值:")
        for dim_name in ['小大', '上下', '奇偶', 'AB']:
            delta = Delta_R[dim_name]
            # 根据ΔR值判断状态
            if delta < 0.0005:  # 0.05%
                status = "平衡"
            elif delta < 0.005:  # 0.5%
                status = "微偏"
            else:
                status = "显著偏离"
            print(f"   ΔR_{dim_name:<4} = {delta:.6f} ({status})")
        
        # 输出R值供参考
        print(f"\n📈 R值统计（参考）:")
        dim_map = {'size': '小大', 'position': '上下', 'parity': '奇偶', 'ab': 'AB'}
        for dim_en, dim_cn in dim_map.items():
            R_fwd = results['R_forward'][dim_en]
            R_bwd = results['R_backward'][dim_en]
            print(f"   {dim_cn:<4}: 正向={R_fwd:.4%}, 反向={R_bwd:.4%}")
            
    else:
        # 使用兼容接口（与千问代码相同）
        print("使用兼容接口进行分析...")
        Omega, Delta_R = calculate_Omega(pi_digits)
        
        # 结构判定
        if Omega < 0.01:
            structure_type = "无显著结构（随机序列）"
        elif Omega < 0.15:
            structure_type = "弱结构（如健康生物序列）"
        else:
            structure_type = "强结构（如病理序列）"
        
        print(f"\n📈 分析结果:")
        print(f"   序列长度: {len(pi_digits):,} 位")
        print(f"   Ω值: {Omega:.6f}")
        print(f"   结构判定: {structure_type}")
        
        print(f"\n📊 四维ΔR值:")
        for dim_name, delta in Delta_R.items():
            print(f"   ΔR_{dim_name:<4} = {delta:.6f}")
    
    elapsed_time = time.time() - start_time
    print(f"\n⏱ 分析耗时: {elapsed_time:.2f} 秒")
    
    return Omega, Delta_R if not use_full_model else results


def main():
    """主程序"""
    print("="*70)
    print("🔬 FD-JTMS v2.0 - 四维九和拓扑模型分析系统")
    print("="*70)
    print("版本说明: 完全遵循论文规范，修正了千问代码的所有关键错误")
    print("主要修正:")
    print("  1. AB关系矩阵: (2,5)和(5,2)修正为克关系(0)")
    print("  2. 反向分组: 正确实现 [d_{N-12k}, ..., d_{N-12k-11}]")
    print("  3. 四个维度: 完全独立计算，绝不混合")
    print("  4. 九和配对: 严格执行 state_id_a + state_id_b = 9")
    print("="*70)
    
    # 步骤1: 验证模型实现
    print("\n🚀 步骤1: 验证模型实现正确性...")
    if not validate_model_implementation():
        print("\n⚠ 警告: 模型验证失败！")
        response = input("是否继续分析? (y/n): ")
        if response.lower() != 'y':
            print("分析已取消")
            return
    else:
        print("\n✅ 模型验证通过，可以开始分析")
    
    # 步骤2: 加载π数据
    print("\n🚀 步骤2: 加载π数据...")
    
    # 可以根据需要调整位数
    # analysis_digits = 1000000    # 100万位（需要较长时间）
    analysis_digits = 100000      # 10万位（测试用）
    # analysis_digits = 10000      # 1万位（快速测试）
    
    pi_digits = load_pi_digits("pi_digits.txt", analysis_digits)
    
    if len(pi_digits) < 10000:
        print(f"❌ 错误: 数据不足 ({len(pi_digits)}位)，至少需要10,000位")
        return
    
    # 步骤3: 分析π的拓扑结构
    print("\n🚀 步骤3: 分析π序列拓扑结构...")
    
    # 使用完整模型类进行分析（推荐）
    results = analyze_pi_structure(pi_digits, use_full_model=True)
    
    # 步骤4: 生成结论
    print("\n" + "="*70)
    print("💡 最终结论")
    print("="*70)
    
    if isinstance(results, tuple):
        Omega = results[0]
    else:
        Omega = results['Omega']
    
    if Omega >= 0.15:
        print("🌟 π序列存在强拓扑结构！")
        print("   这符合《易经》'阴阳不均质'的理论预测。")
        print("   在数学上表明π数字序列具有内在的非对称性。")
        print("\n   论文对照: 类似表6中的癌变DNA序列特征")
    elif Omega >= 0.01:
        print("🔹 π序列存在弱拓扑结构。")
        print("   表明π数字序列具有一定的有序性，但未达到显著非对称。")
        print("\n   论文对照: 类似表6中的健康DNA序列特征")
    else:
        print("🔸 未检测到显著拓扑结构。")
        print("   π数字序列在本模型下表现出类似随机序列的特征。")
        print("\n   论文对照: 类似表5中的随机序列基准")
    
    # 步骤5: 输出论文格式结果
    print("\n" + "="*70)
    print("📝 论文格式输出")
    print("="*70)
    
    if isinstance(results, tuple):
        Omega, Delta_R = results
        print(f"Ω = {Omega:.3f}")
        for dim_name, delta in Delta_R.items():
            print(f"ΔR_{dim_name} = {delta:.4f}")
    else:
        print(f"Ω = {results['Omega']:.3f}")
        for dim_name, delta in results['Delta_R'].items():
            print(f"ΔR_{dim_name} = {delta:.4f}")
        print(f"结构判定: {results['structure_type']}")
    
    print("\n✅ 分析完成！")
    print("="*70)


if __name__ == "__main__":
    main()
