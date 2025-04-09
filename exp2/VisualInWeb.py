import webbrowser
from bs4 import BeautifulSoup
import tempfile
import os

def display_html_in_browser(html_data_list):
    """
    将 [href, html源代码] 数组按顺序拼接，并在浏览器中显示
    
    参数:
        html_data_list: 包含多个 [href, html] 的列表，例如:
            [
                ["page1", "<h1>Page 1</h1><p>Content 1</p>"],
                ["page2", "<h1>Page 2</h1><p>Content 2</p>"]
            ]
    """
    # 创建完整的HTML文档结构
    full_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>拼接的HTML内容</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .page { margin-bottom: 40px; border-bottom: 2px solid #ccc; padding-bottom: 20px; }
            .page-header { color: #333; background-color: #f0f0f0; padding: 10px; }
        </style>
    </head>
    <body>
    """
    
    # 按顺序拼接每个HTML片段
    for href, html in html_data_list:
        # 使用BeautifulSoup清理HTML（可选）
        soup = BeautifulSoup(html, 'html.parser')
        cleaned_html = str(soup)
        
        # 添加带href标识的区块
        full_html += f"""
        <div class="page">
            <div class="page-header">来源: {href}</div>
            {cleaned_html}
        </div>
        """
    
    # 闭合HTML文档
    full_html += """
    </body>
    </html>
    """
    
    # 创建临时HTML文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(full_html)
        temp_path = f.name
    
    # 在浏览器中打开
    webbrowser.open('file://' + os.path.abspath(temp_path))
    print(f"已在浏览器中打开临时文件: {temp_path}")

# 示例使用
if __name__ == "__main__":
    # 示例数据 - 包含多个[href, html]的数组
    html_data = [
        ["https://example.com/page1", "<h1>第一页</h1><p>这是第一页的内容</p><a href='#'>链接</a>"],
        ["https://example.com/page2", "<div><h2>第二页</h2><ul><li>项目1</li><li>项目2</li></ul></div>"],
        ["https://example.com/page3", "<p>第三页的简单内容</p>"]
    ]
    
    display_html_in_browser(html_data)