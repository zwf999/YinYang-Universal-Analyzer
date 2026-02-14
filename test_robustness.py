#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鲁棒性测试脚本
直接执行DNA分析系统的鲁棒性测试功能
"""

from dna_four_track_enhanced import DNAFourTrackSystem

# 创建分析系统实例
system = DNAFourTrackSystem()

# 执行鲁棒性测试
print("执行鲁棒性测试...")
results = system.perform_robustness_test()

# 保存测试结果
print("\n保存测试结果...")
system.save_results(results, "robustness_test_results.json")

print("\n鲁棒性测试完成！")
