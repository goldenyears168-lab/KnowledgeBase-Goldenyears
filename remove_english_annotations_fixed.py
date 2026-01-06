#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确删除知识库中的英文标注
只删除括号中的英文，不影响换行符和格式
"""

import os
import re
from pathlib import Path

def remove_annotations_from_file(file_path):
    """从文件中删除英文标注，保留格式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        modified = False
        new_lines = []
        
        for line in lines:
            original_line = line
            # 匹配括号中的英文标注（大写字母开头，可能包含空格、&、-等）
            # 使用更精确的正则，确保不匹配中文括号
            pattern = r'\(([A-Z][a-zA-Z\s&\-]+\w+)\)'
            
            def replace_func(match):
                return ''  # 只删除标注，不删除括号外的内容
            
            new_line = re.sub(pattern, replace_func, line)
            
            if new_line != original_line:
                modified = True
            
            new_lines.append(new_line)
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return True
        return False
    except Exception as e:
        print(f"错误处理文件 {file_path}: {e}")
        return False

def main():
    script_dir = Path(__file__).parent
    root_dir = script_dir
    
    print("=" * 80)
    print("精确删除英文标注（保留格式）")
    print("=" * 80)
    print(f"扫描目录: {root_dir}\n")
    
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

