from core_engine import calculate_Omega

def load_pi_digits(filename='data/pi_digits_1m.txt'):
    try:
        with open(filename, 'r') as f:
            digits = f.read().strip()
        return [int(c) for c in digits if c.isdigit()]
    except FileNotFoundError:
        print("❌ 错误: 未找到 data/pi_digits_1m.txt 文件")
        print("👉 请先在 data/ 目录下上传圆周率数据")
        return None

if __name__ == "__main__":
    print("🔬 FD-JTMS v1.0 启动...")
    print("正在分析圆周率π (1,000,000位)...\n")
    
    pi_digits = load_pi_digits()
    if pi_digits is None:
        exit(1)
    
    Omega, Delta_R = calculate_Omega(pi_digits)
    
    print("✅ 验证结果:")
    print(f"  Ω值       = {Omega:.3f}")
    print(f"  ΔR_规模   = {Delta_R['规模']:.4f}")
    print(f"  ΔR_水平   = {Delta_R['水平']:.4f}")
    print(f"  ΔR_奇偶   = {Delta_R['奇偶']:.4f}")
    print(f"  ΔR_生克   = {Delta_R['生克']:.4f}")
    
    if Omega > 0.15:
        print("\n🌟 结论: π序列存在强拓扑结构！符合'阴阳不均质'理论。")
    else:
        print("\n❓ 结论: 未检测到显著结构。")
