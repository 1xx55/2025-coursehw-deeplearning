import webbrowser
from bs4 import BeautifulSoup
import tempfile
import os

def display_html_in_browser(html_data_list,title):
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
        <meta charset="utf-8">
        <title>""" + str(title) +"""</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .page { margin-bottom: 40px; border-bottom: 2px solid #ccc; padding-bottom: 20px; }
            .page-header { color: #333; background-color: #f0f0f0; padding: 10px; }
        </style>
    </head>
    <body>
        <!-- 使用官方 CDN 添加JQuery -->
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <!-- 加载css -->
        <link href="https://img1.doubanio.com/f/vendors/e92483e5e4c9c60cc75cbd8b700a2fd5b5fdf7b0/css/douban.css" rel="stylesheet" type="text/css">
    """
    
    # 按顺序拼接每个HTML片段(带个性化处理)
    for href, html in html_data_list:
       
        soup = BeautifulSoup(html, 'html.parser')
        #cleaned_html = str(soup)
        img = soup.find('img')
        filmname = img['alt']
        #手动修正不正确的格式

        img['height'] = 202.5
        img['width'] = 135
        
        # 添加带href标识的区块
        full_html += f"""
        <div class="page">
            <div class="page-header">电影: 
                <a href="{href}"> {filmname} </a>
            </div>
            {str(soup)}
        </div>
        """
    
    # 闭合HTML文档
    full_html += """
    </body>
    </html>
    """
    
    # 创建临时HTML文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False , encoding='utf-8') as f:
        f.write(full_html)
        temp_path = f.name
    
    # 在浏览器中打开
    webbrowser.open('file://' + os.path.abspath(temp_path))
    print(f"已在浏览器中打开临时文件: {temp_path}")

if __name__ == "__main__":
    
    file_name = input("输入要打开的文件名:(回车则默认为合肥.txt)").strip()
    if len(file_name) == 0:
        file_name = "exp2/合肥.txt"

    with open(file_name,"r",encoding='utf-8') as f:
        data = f.read()
    data = eval(data.encode().decode('utf-8'))

    # 按豆瓣评分排序
    for i in range(2):
        data[i].sort(key = lambda x : BeautifulSoup(x[1]).find('strong',class_ = "ll rating_num").text, reverse = True)

    display_html_in_browser(data[0],file_name.replace('.txt',' ') + "正在热映")
    display_html_in_browser(data[1],file_name.replace('.txt',' ') + "即将上映")
