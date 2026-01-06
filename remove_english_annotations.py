#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量删除知识库中的英文标注
保留：法律术语、工具名称（Google Drive/Sheet/Form）、Role Spec
删除：其他所有英文标注
"""

import os
import re
from pathlib import Path

# 需要保留的标注（不删除）
KEEP_ANNOTATIONS = {
    # 法律术语
    'Working Hours & Location',
    'Compensation & Payment',
    'Rights & Obligations',
    'Term & Termination',
    'Breach of Contract',
    'Dispute Resolution',
    'Nature & Governing Law',
    'Position & Work Location',
    'Scope of Work',
    'Compensation & Performance Bonus',
    'Compensation Structure',
    'Net Operating Profit',
    'Manager Value Calculation',
    'Bonus Pool & Accumulation & Safety Reserve',
    'Distribution Schedule',
    'Eligibility & Forfeiture',
    'Retention Bonus',
    'Operational KPIs',
    'The Voluntary Clause',
    # 契约书标题
    'CEO Service Agreement',
    'Store Manager Service Agreement',
    'Photographer Contract Agreement',
    'Trainee Partner Contract Agreement',
    'Makeup Artist Contract Agreement',
    # 工具名称
    'Google Drive',
    'Google Sheet',
    'Google Form',
    # 其他需要保留的
    'Role Spec',
}

def should_keep(annotation):
    """判断是否应该保留这个标注"""
    # 移除括号
    text = annotation.strip('()')
    return text in KEEP_ANNOTATIONS

def remove_annotations_from_file(file_path):
    """从文件中删除英文标注"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 匹配所有括号中的英文标注
        pattern = r'\(([A-Z][a-zA-Z\s&\-]+\w+)\)'
        
        def replace_func(match):
            annotation = match.group(0)  # 包含括号的完整匹配
            text = match.group(1)  # 括号内的文本
            
            if should_keep(annotation):
                return annotation  # 保留
            else:
                return ''  # 删除
        
        new_content = re.sub(pattern, replace_func, content)
        
        # 清理多余的空格（如果删除标注后留下空格）
        new_content = re.sub(r'\s+\(\)', '', new_content)  # 删除空括号
        new_content = re.sub(r'\s+-\s+', ' - ', new_content)  # 清理 " - " 前后的空格
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"错误处理文件 {file_path}: {e}")
        return False

def main():
    script_dir = Path(__file__).parent
    root_dir = script_dir
    
    print("=" * 80)
    print("批量删除英文标注")
    print("=" * 80)
    print(f"扫描目录: {root_dir}\n")
    print(f"保留的标注类型: {len(KEEP_ANNOTATIONS)} 种\n")
    
    modified_files = []
    
    for file_path in root_dir.rglob('*.md'):
        if '.git' in str(file_path) or '__pycache__' in str(file_path):
            continue
        
        if remove_annotations_from_file(file_path):
            modified_files.append(file_path)
            rel_path = file_path.relative_to(root_dir)
            print(f"✓ 已处理: {rel_path}")
    
    print(f"\n共处理 {len(modified_files)} 个文件")
    print("=" * 80)
    print("完成！")
    print("=" * 80)

if __name__ == '__main__':
    main()

