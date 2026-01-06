#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计知识库项目字数
统计所有 Markdown 文件的中文字数和总字数
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def count_chinese_chars(text):
    """统计中文字符数（包括中文标点）"""
    # 匹配中文字符（包括中文标点）
    chinese_pattern = r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]'
    chinese_chars = re.findall(chinese_pattern, text)
    return len(chinese_chars)

def count_total_chars(text):
    """统计总字符数（不包括空白字符）"""
    # 移除所有空白字符后统计
    return len(text.replace(' ', '').replace('\n', '').replace('\t', ''))

def count_words(text):
    """统计总词数（按空格和换行分割）"""
    words = text.split()
    return len(words)

def analyze_file(file_path):
    """分析单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        chinese_count = count_chinese_chars(content)
        total_chars = count_total_chars(content)
        word_count = count_words(content)
        line_count = len(content.splitlines())
        
        return {
            'chinese_chars': chinese_count,
            'total_chars': total_chars,
            'words': word_count,
            'lines': line_count,
            'size': len(content)
        }
    except Exception as e:
        print(f"错误：无法读取文件 {file_path}: {e}")
        return None

def scan_directory(root_dir, extensions=None, exclude_dirs=None):
    """扫描目录，统计所有文件"""
    if extensions is None:
        extensions = ['.md', '.txt', '.py']
    
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', '.DS_Store', 'node_modules'}
    
    stats = defaultdict(lambda: {
        'files': 0,
        'chinese_chars': 0,
        'total_chars': 0,
        'words': 0,
        'lines': 0,
        'size': 0
    })
    
    file_details = []
    
    root_path = Path(root_dir)
    
    for file_path in root_path.rglob('*'):
        # 跳过排除的目录
        if any(exclude in str(file_path) for exclude in exclude_dirs):
            continue
        
        # 只处理指定扩展名的文件
        if file_path.suffix.lower() in extensions:
            rel_path = file_path.relative_to(root_path)
            folder = str(rel_path.parent) if rel_path.parent != Path('.') else '根目录'
            
            file_stat = analyze_file(file_path)
            if file_stat:
                stats[folder]['files'] += 1
                stats[folder]['chinese_chars'] += file_stat['chinese_chars']
                stats[folder]['total_chars'] += file_stat['total_chars']
                stats[folder]['words'] += file_stat['words']
                stats[folder]['lines'] += file_stat['lines']
                stats[folder]['size'] += file_stat['size']
                
                file_details.append({
                    'path': str(rel_path),
                    'folder': folder,
                    **file_stat
                })
    
    return stats, file_details

def format_number(num):
    """格式化数字，添加千位分隔符"""
    return f"{num:,}"

def main():
    # 获取项目根目录
    script_dir = Path(__file__).parent
    root_dir = script_dir
    
    print("=" * 80)
    print("知识库字数统计")
    print("=" * 80)
    print(f"扫描目录: {root_dir}\n")
    
    # 扫描文件
    stats, file_details = scan_directory(
        root_dir,
        extensions=['.md'],  # 只统计 Markdown 文件
        exclude_dirs={'.git', '__pycache__', '.DS_Store', 'node_modules', '.vscode'}
    )
    
    # 汇总统计
    total_stats = {
        'files': 0,
        'chinese_chars': 0,
        'total_chars': 0,
        'words': 0,
        'lines': 0,
        'size': 0
    }
    
    for folder_stat in stats.values():
        for key in total_stats:
            total_stats[key] += folder_stat[key]
    
    # 显示汇总
    print("\n" + "=" * 80)
    print("📊 总体统计")
    print("=" * 80)
    print(f"文件总数:     {format_number(total_stats['files'])} 个")
    print(f"中文字符数:   {format_number(total_stats['chinese_chars'])} 字")
    print(f"总字符数:     {format_number(total_stats['total_chars'])} 字")
    print(f"总词数:       {format_number(total_stats['words'])} 词")
    print(f"总行数:       {format_number(total_stats['lines'])} 行")
    print(f"文件大小:     {format_number(total_stats['size'])} 字节 ({total_stats['size'] / 1024:.2f} KB)")
    
    # 按目录分组显示
    print("\n" + "=" * 80)
    print("📁 按目录统计")
    print("=" * 80)
    
    # 按目录排序
    sorted_folders = sorted(stats.items(), key=lambda x: x[1]['chinese_chars'], reverse=True)
    
    for folder, folder_stat in sorted_folders:
        if folder_stat['files'] > 0:
            print(f"\n📂 {folder}")
            print(f"   文件数:     {format_number(folder_stat['files'])} 个")
            print(f"   中文字符:   {format_number(folder_stat['chinese_chars'])} 字")
            print(f"   总字符数:   {format_number(folder_stat['total_chars'])} 字")
            print(f"   总词数:     {format_number(folder_stat['words'])} 词")
            print(f"   总行数:     {format_number(folder_stat['lines'])} 行")
    
    # 显示最大的文件
    print("\n" + "=" * 80)
    print("📄 字数最多的前 10 个文件")
    print("=" * 80)
    
    sorted_files = sorted(file_details, key=lambda x: x['chinese_chars'], reverse=True)[:10]
    
    for i, file_info in enumerate(sorted_files, 1):
        print(f"\n{i}. {file_info['path']}")
        print(f"   中文字符: {format_number(file_info['chinese_chars'])} 字")
        print(f"   总字符数: {format_number(file_info['total_chars'])} 字")
        print(f"   行数: {format_number(file_info['lines'])} 行")
    
    print("\n" + "=" * 80)
    print("统计完成！")
    print("=" * 80)

if __name__ == '__main__':
    main()

