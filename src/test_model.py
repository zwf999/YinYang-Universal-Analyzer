"""
test_model.py - 模型测试脚本
用于验证实现的正确性
"""

import sys
sys.path.append('.')

from core_engine import FourDimNineHarmonyModel
import random


def test_random_sequence():
    """测试随机序列（零假设验证）"""
    print("测试1: 随机序列零假设验证")
    print("-" * 50)
    
    random.seed(42)
    test_seq = [random.randint(0, 9) for _ in range(100000)]
    
    model = FourDimNineHarmonyModel(test_seq)
    results = model.calculate_Omega()
    
    print(f"序列长度: {len(test_seq):,}")
    print(f"Ω值: {results['Omega']:.6f}")
    print(f"期望: < 0.01")
    print(f"通过: {results['Omega'] < 0.01}")
    
    print("\nΔR值:")
    for dim_name, delta in results['Delta_R'].items():
        print(f"  {dim_name}: {delta:.6f} (期望: < 0.0005)")
    
    return results['Omega'] < 0.01


def test_ab_matrix():
    """测试AB关系矩阵的正确性"""
    print("\n测试2: AB关系矩阵验证")
    print("-" * 50)
    
    # 测试几个关键组合
    model = FourDimNineHarmonyModel([0])
    
    # 克关系 (AB=0) 的组合
    ke_relations = [(1,1), (1,2), (1,5), (2,1), (2,2), (2,4), 
                   (2,5), (3,3), (3,4), (3,5), (4,2), (4,3), 
                   (4,4), (5,1), (5,2), (5,3), (5,5)]
    
    errors = []
    for li, lj in ke_relations:
        if model.get_ab_relation(li, lj) != 0:
            errors.append(f"({li},{lj}) 应为克关系(0)，但得到: {model.get_ab_relation(li, lj)}")
    
    if errors:
        print("错误发现:")
        for err in errors[:10]:  # 只显示前10个错误
            print(f"  {err}")
        return False
    else:
        print("✓ 所有克关系组合正确")
        return True


def test_backward_grouping():
    """测试反向分组逻辑"""
    print("\n测试3: 反向分组验证")
    print("-" * 50)
    
    # 创建测试序列: 0-11重复
    test_seq = list(range(12)) * 3  # 36位
    
    model = FourDimNineHarmonyModel(test_seq)
    backward_blocks = model.get_backward_blocks()
    
    print(f"原序列最后12位: {test_seq[-12:]}")
    print(f"期望的反向块: {test_seq[-12:][::-1]}")
    print(f"实际的反向块: {backward_blocks[0] if backward_blocks else '无'}")
    
    correct = backward_blocks and backward_blocks[0] == test_seq[-12:][::-1]
    print(f"正确: {correct}")
    
    return correct


def test_state_id_calculation():
    """测试八卦状态ID计算"""
    print("\n测试4: 八卦状态ID计算验证")
    print("-" * 50)
    
    model = FourDimNineHarmonyModel([0, 1, 2])
    
    # 测试各种位组合
    test_cases = [
        ((1,1,1), 1),
        ((1,1,0), 2),
        ((1,0,1), 3),
        ((1,0,0), 4),
        ((0,1,1), 5),
        ((0,1,0), 6),
        ((0,0,1), 7),
        ((0,0,0), 8)
    ]
    
    errors = []
    for bits, expected in test_cases:
        actual = model.get_state_id(bits)
        if actual != expected:
            errors.append(f"bits{bits}: 期望{expected}, 实际{actual}")
    
    if errors:
        print("错误发现:")
        for err in errors:
            print(f"  {err}")
        return False
    else:
        print("✓ 所有状态ID计算正确")
        return True


def main():
    """运行所有测试"""
    print("四维九和拓扑模型测试套件")
    print("=" * 60)
    
    tests = [
        ("随机序列零假设", test_random_sequence),
        ("AB关系矩阵", test_ab_matrix),
        ("反向分组", test_backward_grouping),
        ("八卦状态ID", test_state_id_calculation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"✓ {test_name}测试通过")
                passed += 1
            else:
                print(f"✗ {test_name}测试失败")
        except Exception as e:
            print(f"✗ {test_name}测试出错: {e}")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过，模型实现正确！")
        return True
    else:
        print("⚠ 部分测试失败，请检查实现")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
