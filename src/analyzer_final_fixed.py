# analyzer_final_fixed.py
# 修复版：完整显示历史数据，优化用户体验

import os
import time
from collections import Counter

DATA_DIR = "data"

# --- 完全正确的 ATTRIBUTES ---
ATTRIBUTES = {
    0: (0, 5, 0, 0), 1: (1, 1, 1, 1), 2: (1, 2, 1, 0), 3: (1, 3, 1, 1),
    4: (1, 4, 0, 0), 5: (1, 5, 0, 1), 6: (0, 1, 1, 0), 7: (0, 2, 1, 1),
    8: (0, 3, 1, 0), 9: (0, 4, 0, 1)
}

AB_MATRIX = [
    [0, 0, 1, 1, 0], [0, 0, 1, 0, 1], [1, 1, 0, 0, 0],
    [1, 0, 0, 0, 1], [0, 1, 0, 1, 0]
]

GANZHI_MAP = {1:'甲',8:'甲', 3:'丙',6:'丙', 9:'戊',0:'戊', 2:'乙',5:'乙', 4:'丁',7:'丁'}
YANG_SET = {'甲', '丙', '戊'}
STATE_MAP = {(1,1,1):1, (1,1,0):2, (1,0,1):3, (1,0,0):4,
             (0,1,1):5, (0,1,0):6, (0,0,1):7, (0,0,0):8}

# 更新后的历史数据
HISTORY_DATA = {
    'pi_digits_1m.txt': {
        'name': 'π (圆周率)',
        'type': '超越数',
        'yang': 572880,
        'yin': 94544,
        'ratio': 6.059
    },
    'phi_digits_1m.txt': {
        'name': 'φ (黄金分割)',
        'type': '代数无理数',
        'yang': 574082,
        'yin': 92768,
        'ratio': 6.188
    },
    'sqrt2_generated.txt': {
        'name': '√2 (根号2)',
        'type': '代数无理数',
        'yang': 2998,
        'yin': 444,
        'ratio': 6.752
    },
    'b001620_full.txt': {
        'name': 'b001620 (未知)',
        'type': '未知',
        'yang': 114012,
        'yin': 20150,
        'ratio': 5.658
    },
    'rational_142857.txt': {
        'name': '1/7 (有理数)',
        'type': '有理数',
        'yang': 0,
        'yin': 4792,
        'ratio': 0.000
    }
}

def validate_attributes():
    for num in range(10):
        small_big, layer, up_down, odd_even = ATTRIBUTES[num]
        expected_small = 1 if num in {1,2,3,4,5} else 0
        expected_up = 1 if num in {1,2,3,6,7,8} else 0
        expected_odd = num % 2
        assert small_big == expected_small, f"❌ 数字 {num} 小大属性错误"
        assert up_down == expected_up, f"❌ 数字 {num} 上下属性错误"
        assert odd_even == expected_odd, f"❌ 数字 {num} 奇偶属性错误"

def get_state(bits):
    return STATE_MAP.get(bits, 0)

def analyze_window(digits):
    parts = [digits[i:i+3] for i in range(0, 12, 3)]
    states = []
    
    for part in parts:
        s1 = get_state(tuple(ATTRIBUTES[d][0] for d in part))
        s2 = get_state(tuple(ATTRIBUTES[d][2] for d in part))
        s3 = get_state(tuple(ATTRIBUTES[d][3] for d in part))
        
        layers = [ATTRIBUTES[d][1]-1 for d in part]
        ab_bits = (
            AB_MATRIX[layers[0]][layers[1]],
            AB_MATRIX[layers[1]][layers[2]],
            AB_MATRIX[layers[2]][layers[0]]
        )
        s4 = get_state(ab_bits)
        states.append((s1, s2, s3, s4))
    
    p13_ok = all(states[0][i] + states[2][i] == 9 for i in range(4))
    p24_ok = all(states[1][i] + states[3][i] == 9 for i in range(4))
    
    local_res = []
    if not p13_ok:
        local_res.extend(parts[0] + parts[2])
    if not p24_ok:
        local_res.extend(parts[1] + parts[3])
    
    tags = [GANZHI_MAP[d] for d in digits]
    yang_nums = [d for d, t in zip(digits, tags) if t in YANG_SET]
    yin_nums = [d for d, t in zip(digits, tags) if t not in YANG_SET]
    diff = len(yang_nums) - len(yin_nums)
    
    if diff > 0:
        global_res = yang_nums[-diff:] if diff <= len(yang_nums) else yang_nums
    elif diff < 0:
        global_res = yin_nums[:abs(diff)] if abs(diff) <= len(yin_nums) else yin_nums
    else:
        global_res = []
    
    return local_res, global_res

def analyze_file(filename, description=""):
    full_path = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(full_path):
        print(f"❌ 文件不存在: {full_path}")
        return None
    
    print(f"\n{'='*60}")
    if description:
        print(f"🔬 分析: {description}")
    else:
        print(f"🔬 分析: {filename}")
    print(f"📁 文件: {filename}")
    print(f"{'='*60}")
    
    with open(full_path, 'r') as f:
        content = f.read()
    digits = [int(c) for c in content if c.isdigit()]
    
    if len(digits) < 12:
        print("❌ 数字不足12位！")
        return None
    
    print(f"📊 读取 {len(digits)} 位数字")
    
    local_counter = Counter()
    global_counter = Counter()
    window_count = 0
    
    for i in range(0, len(digits) - 11, 5):
        window = digits[i:i+12]
        local_res, global_res = analyze_window(window)
        local_counter.update(local_res)
        global_counter.update(global_res)
        window_count += 1
        
        if window_count % 50000 == 0 and len(digits) > 100000:
            print(f"  已处理 {window_count} 个窗口")
    
    total_local = sum(local_counter.values())
    total_global = sum(global_counter.values())
    
    yang_nums = [1, 3, 6, 8, 9, 0]
    yin_nums = [2, 4, 5, 7]
    
    yang_total = sum(global_counter[d] for d in yang_nums)
    yin_total = sum(global_counter[d] for d in yin_nums)
    
    ratio = yang_total / yin_total if yin_total > 0 else 0
    
    print(f"\n✅ 分析完成")
    print(f"📊 总窗口数: {window_count}")
    print(f"📊 局部残余总数: {total_local}")
    print(f"📊 全局残余总数: {total_global}")
    
    if total_local > 0:
        local_rate = (total_local / (window_count * 12)) * 100
        print(f"📈 局部残余率: {local_rate:.2f}%")
    
    print(f"🌞 阳数({yang_nums}): {yang_total} 次")
    print(f"🌙 阴数({yin_nums}): {yin_total} 次")
    
    if yin_total > 0:
        print(f"📐 阴阳比例: {ratio:.3f} : 1")
    else:
        print(f"📐 阴阳比例: 纯阴 (无阳数)")
    
    # 保存结果
    base_name = os.path.splitext(filename)[0]
    result_file = f"analysis_{base_name}_final.txt"
    
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write(f"常数光谱分析报告\n")
        f.write(f"{'='*40}\n\n")
        if description:
            f.write(f"分析对象: {description}\n")
        else:
            f.write(f"分析对象: {filename}\n")
        f.write(f"分析时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"核心统计:\n")
        f.write(f"  总窗口数: {window_count}\n")
        f.write(f"  局部残余总数: {total_local}\n")
        f.write(f"  全局残余总数: {total_global}\n")
        
        if total_local > 0:
            f.write(f"  局部残余率: {local_rate:.2f}%\n")
        
        f.write(f"  阳数总数: {yang_total}\n")
        f.write(f"  阴数总数: {yin_total}\n")
        
        if yin_total > 0:
            f.write(f"  阴阳比例: {ratio:.3f} : 1\n\n")
        else:
            f.write(f"  阴阳比例: 纯阴\n\n")
    
    print(f"💾 结果保存到: {result_file}")
    print(f"{'='*60}")
    
    return {
        '文件名': filename,
        '描述': description if description else filename,
        '窗口数': window_count,
        '局部总数': total_local,
        '全局总数': total_global,
        '阳数总数': yang_total,
        '阴数总数': yin_total,
        '阴阳比例': ratio,
        '局部残余率': local_rate if total_local > 0 else 0
    }

def show_comparison():
    """显示所有历史数据的对比"""
    print(f"\n{'='*80}")
    print("📊 数学常数阴阳光谱全览")
    print(f"{'='*80}")
    
    print(f"\n{'常数名称':<20} {'类型':<15} {'阳数':<10} {'阴数':<10} {'阴阳比':<10} {'特征分析'}")
    print(f"{'-'*80}")
    
    # 按阴阳比例排序
    sorted_data = sorted(HISTORY_DATA.items(), 
                        key=lambda x: x[1]['ratio'], 
                        reverse=True)
    
    for filename, data in sorted_data:
        name = data['name']
        const_type = data['type']
        yang = data['yang']
        yin = data['yin']
        ratio = data['ratio']
        
        # 特征分析
        if ratio > 5:
            if ratio > 6.5:
                feature = "🔥 超阳偏倚 (>6.5:1)"
            else:
                feature = "🚀 强烈阳数偏倚 (~6:1)"
            
            if const_type == "超越数":
                feature += " [核心超越数]"
            elif const_type == "代数无理数":
                feature += " [核心代数数]"
        elif ratio == 0:
            feature = "🔄 纯阴数特征"
        else:
            feature = "⚖️  中等比例"
        
        print(f"{name:<20} {const_type:<15} {yang:<10} {yin:<10} {ratio:<10.3f} {feature}")
    
    print(f"\n{'='*80}")
    print("💡 重大发现总结:")
    print(f"{'-'*80}")
    print("1. 局部不对称性：所有测试常数都100%局部残余")
    print("   → 四维同步对称条件极其严格")
    print("\n2. 全局阴阳结构发现三类：")
    print("   A类 - 超阳偏倚 (>6.5:1)：")
    print("      • √2 (根号2，代数无理数) - 6.752:1 ← 最阳！")
    print("   B类 - 强烈阳数偏倚 (~6:1)：")
    print("      • φ (黄金分割，代数无理数) - 6.188:1")
    print("      • π (圆周率，超越数) - 6.059:1")
    print("      • b001620 (未知常数) - 5.658:1")
    print("   C类 - 阴数偏倚：")
    print("      • 1/7 (有理数) - 0.000:1")
    print("\n3. 理论突破：")
    print("   重要数学常数都强烈阳数偏倚，有理数则阴数偏倚")
    print("   阴阳比例反映了常数的'数学重要性'")
    print(f"{'='*80}")

def main_menu():
    while True:
        print(f"\n{'='*60}")
        print("🧬 常数光谱分析器 FINAL 版")
        print(f"{'='*60}")
        print("功能说明：")
        print("  1. 分析新文件")
        print("  2. 查看历史对比")
        print("  3. 分析并更新历史")
        print("  4. 退出程序")
        print(f"{'-'*60}")
        
        choice = input("请选择 (1-4): ").strip()
        
        if choice == "4":
            print("👋 再见！")
            break
        
        validate_attributes()
        
        if choice == "1":
            filename = input("请输入文件名 (放在data文件夹内): ").strip()
            description = input("请输入描述 (直接回车跳过): ").strip()
            analyze_file(filename, description)
            input("\n按回车继续...")
        
        elif choice == "2":
            show_comparison()
            input("\n按回车继续...")
        
        elif choice == "3":
            print("\ndata文件夹中的文件:")
            files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
            for i, f in enumerate(files, 1):
                print(f"  {i:2d}. {f}")
            
            filename = input("\n请输入要分析的文件名: ").strip()
            
            # 检查文件是否存在
            if filename not in files:
                print(f"❌ 文件 {filename} 不在data文件夹中")
                input("\n按回车继续...")
                continue
            
            description = input("请输入描述 (直接回车使用文件名): ").strip()
            if not description:
                description = filename
            
            const_type = input("请输入常数类型 (如: 超越数, 代数无理数, 有理数等): ").strip()
            
            result = analyze_file(filename, description)
            if result:
                # 更新历史数据
                HISTORY_DATA[filename] = {
                    'name': description,
                    'type': const_type,
                    'yang': result['阳数总数'],
                    'yin': result['阴数总数'],
                    'ratio': result['阴阳比例']
                }
                print("✅ 已更新历史数据")
                show_comparison()
                input("\n按回车继续...")

if __name__ == "__main__":
    main_menu()
