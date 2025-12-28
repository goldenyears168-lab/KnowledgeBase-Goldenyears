#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
將 FAQ JSON 轉換為 Markdown 格式
只保留 question, answer, keywords 三個欄位
"""

import json
import os

def convert_json_to_md(json_file_path, output_md_path):
    """將 JSON FAQ 轉換為 Markdown 格式"""
    
    # 讀取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 準備 Markdown 內容
    md_content = []
    
    # 添加標題
    md_content.append("# FAQ 問答集\n\n")
    md_content.append(f"最後更新：{data.get('last_updated', 'N/A')}\n\n")
    md_content.append("---\n\n")
    
    # 遍歷所有分類
    categories = data.get('categories', {})
    
    for category_key, category_data in categories.items():
        category_title = category_data.get('title', category_key)
        questions = category_data.get('questions', [])
        
        # 添加分類標題
        md_content.append(f"## {category_title}\n\n")
        
        # 遍歷該分類下的所有問題
        for idx, q in enumerate(questions, 1):
            question = q.get('question', '')
            answer = q.get('answer', '')
            keywords = q.get('keywords', [])
            
            # 添加問題
            md_content.append(f"### Q{idx}: {question}\n\n")
            
            # 添加答案
            md_content.append(f"**答案：**\n\n{answer}\n\n")
            
            # 添加關鍵字
            if keywords:
                keywords_str = "、".join(keywords)
                md_content.append(f"**關鍵字：** {keywords_str}\n\n")
            
            # 添加分隔線（除了最後一個）
            md_content.append("---\n\n")
    
    # 寫入 Markdown 文件
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write(''.join(md_content))
    
    print(f"✅ 轉換完成！已生成：{output_md_path}")
    print(f"   共處理 {len(categories)} 個分類")

if __name__ == '__main__':
    json_file = '5-faq_detailed.json'
    output_file = 'FAQ.md'
    
    if not os.path.exists(json_file):
        print(f"❌ 錯誤：找不到文件 {json_file}")
        exit(1)
    
    convert_json_to_md(json_file, output_file)

