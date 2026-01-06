#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除知识库中所有英文标注
不保留任何英文标注
"""

import os
import re
from pathlib import Path

def remove_all_annotations_from_file(file_path):
    """从文件中删除所有英文标注"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 匹配所有括号中的英文标注（大写字母开头，可能包含空格、&、-等）
        pattern = r'\([A-Z][a-zA-Z\s&\-]+\w+\)'
        
        new_content = re.sub(pattern, '', content)
        
        # 清理多余的空格和标点
        new_content = re.sub(r'\s+-\s+', ' - ', new_content)  # 清理 " - " 前后的空格
        new_content = re.sub(r'\s+', ' ', new_content)  # 清理多余空格
        new_content = re.sub(r'\s+([，。、；：])', r'\1', new_content)  # 清理标点前的空格
        
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
    print("删除所有英文标注")
    print("=" * 80)
    print(f"扫描目录: {root_dir}\n")
    
    modified_files = []
    
    for file_path in root_dir.rglob('*.md'):
        if '.git' in str(file_path) or '__pycache__' in str(file_path):
            continue
        
        if remove_all_annotations_from_file(file_path):
            modified_files.append(file_path)
            rel_path = file_path.relative_to(root_dir)
            print(f"✓ 已处理: {rel_path}")
    
    print(f"\n共处理 {len(modified_files)} 个文件")
    print("=" * 80)
    print("完成！")
    print("=" * 80)

if __name__ == '__main__':
    main()

