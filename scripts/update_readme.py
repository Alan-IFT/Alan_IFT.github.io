#!/usr/bin/env python3
import os
from pathlib import Path
from urllib.parse import quote

def get_blog_posts():
    """扫描 blog 目录获取所有 Markdown 文件"""
    blog_dir = Path('blog')
    if not blog_dir.exists():
        return []
    
    posts = []
    for file in blog_dir.glob('*.md'):
        # 获取文件名（不含扩展名）作为标题
        title = file.stem
        # URL 编码文件路径
        url = f"blog/{quote(file.name)}"
        # 获取文件修改时间用于排序
        mtime = file.stat().st_mtime
        posts.append((title, url, mtime))
    
    # 按修改时间倒序排序（最新的在前）
    posts.sort(key=lambda x: x[2], reverse=True)
    return [(title, url) for title, url, _ in posts]

def update_readme():
    """更新 README.md 中的文章列表"""
    readme_path = Path('README.md')
    
    if not readme_path.exists():
        print("README.md 不存在")
        return
    
    # 读取现有内容
    content = readme_path.read_text(encoding='utf-8')
    
    # 生成文章列表
    posts = get_blog_posts()
    if not posts:
        posts_section = "## 📝 最新文章\n\n暂无文章\n"
    else:
        posts_list = '\n'.join([f"- [{title}]({url})" for title, url in posts])
        posts_section = f"## 📝 最新文章\n\n{posts_list}\n"
    
    # 查找并替换文章列表部分
    start_marker = "## 📝 最新文章"
    end_marker = "## 访问地址"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        # 替换现有的文章列表
        new_content = content[:start_idx] + posts_section + "\n" + content[end_idx:]
    else:
        # 如果没有找到标记，在"关于本站"后插入
        about_end = content.find("## 访问地址")
        if about_end != -1:
            new_content = content[:about_end] + posts_section + "\n" + content[about_end:]
        else:
            print("无法找到插入位置")
            return
    
    # 写回文件
    readme_path.write_text(new_content, encoding='utf-8')
    print(f"已更新 README.md，共 {len(posts)} 篇文章")

if __name__ == '__main__':
    update_readme()
