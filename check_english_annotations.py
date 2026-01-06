#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查知识库中所有英文标注
查找所有括号中的英文标注，如 (CEO)、(Store Manager) 等
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def find_english_annotations(text):
    """查找所有括号中的英文标注"""
    # 匹配括号中的英文（可能包含空格、&、-等）
    pattern = r'\([A-Z][a-zA-Z\s&\-]+\w+\)'
    matches = re.findall(pattern, text)
    return matches

def analyze_file(file_path):
    """分析单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        annotations = find_english_annotations(content)
        
        if annotations:
            # 统计每个标注出现的行号
            lines = content.split('\n')
            annotation_details = defaultdict(list)
            
            for i, line in enumerate(lines, 1):
                line_annotations = find_english_annotations(line)
                for ann in line_annotations:
                    annotation_details[ann].append(i)
            
            return {
                'file': str(file_path),
                'annotations': dict(annotation_details),
                'total_count': len(annotations),
                'unique_count': len(set(annotations))
            }
        return None
    except Exception as e:
        print(f"错误：无法读取文件 {file_path}: {e}")
        return None

def scan_directory(root_dir):
    """扫描目录，查找所有Markdown文件"""
    results = []
    total_annotations = 0
    total_unique = set()
    
    root_path = Path(root_dir)
    
    for file_path in root_path.rglob('*.md'):
        # 跳过一些不需要检查的文件
        if '.git' in str(file_path) or '__pycache__' in str(file_path):
            continue
        
        result = analyze_file(file_path)
        if result:
            results.append(result)
            total_annotations += result['total_count']
            total_unique.update(result['annotations'].keys())
    
    return results, total_annotations, total_unique

def main():
    # 获取项目根目录
    script_dir = Path(__file__).parent
    root_dir = script_dir
    
    print("=" * 80)
    print("知识库英文标注检查")
    print("=" * 80)
    print(f"扫描目录: {root_dir}\n")
    
    # 扫描文件
    results, total_annotations, total_unique = scan_directory(root_dir)
    
    # 汇总统计
    print("\n" + "=" * 80)
    print("📊 总体统计")
    print("=" * 80)
    print(f"发现文件数:     {len(results)} 个")
    print(f"英文标注总数:   {total_annotations} 个")
    print(f"唯一标注数:     {len(total_unique)} 种")
    
    if results:
        # 按文件显示
        print("\n" + "=" * 80)
        print("📄 发现英文标注的文件")
        print("=" * 80)
        
        # 按标注数量排序
        results.sort(key=lambda x: x['total_count'], reverse=True)
        
        for result in results:
            rel_path = Path(result['file']).relative_to(root_dir)
            print(f"\n📁 {rel_path}")
            print(f"   总标注数: {result['total_count']} 个")
            print(f"   唯一标注: {result['unique_count']} 种")
            
            # 显示前10个最常见的标注
            sorted_annotations = sorted(
                result['annotations'].items(),
                key=lambda x: len(x[1]),
                reverse=True
            )[:10]
            
            for ann, lines in sorted_annotations:
                line_str = ', '.join(map(str, lines[:5]))  # 只显示前5个行号
                if len(lines) > 5:
                    line_str += f" ... (共{len(lines)}处)"
                print(f"   • {ann}: 行 {line_str}")
        
        # 显示所有唯一的标注
        print("\n" + "=" * 80)
        print("📋 所有发现的英文标注类型")
        print("=" * 80)
        
        sorted_unique = sorted(total_unique)
        for i, ann in enumerate(sorted_unique, 1):
            # 统计这个标注在多少个文件中出现
            file_count = sum(1 for r in results if ann in r['annotations'])
            print(f"{i:3d}. {ann} (出现在 {file_count} 个文件中)")
    else:
        print("\n✅ 未发现任何英文标注！")
    
    print("\n" + "=" * 80)
    print("检查完成！")
    print("=" * 80)

if __name__ == '__main__':
    main()

