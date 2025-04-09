import requests
from bs4 import BeautifulSoup
import time

class DouBanFilmViewer():

    #直接访问这两个url会转到对应城市哦！
    nowplayingurl = r"https://movie.douban.com/nowplaying"
    laterurl = r"https://movie.douban.com/later"
    detailurl = r"https://movie.douban.com/subject/" #后面加id即可，但前面已经爬到了所以这个可能用不上
    
    baseheader = {
        "User-Agent": "114514.1919810",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.douban.com/",
        }

    def __init__(self):

        print("准备访问基础页面")

        nowplaying_response = requests.get(url=self.nowplayingurl, headers=self.baseheader, timeout=10)
        later_response = requests.get(url=self.laterurl, headers=self.baseheader, timeout=10)
        self.sp1 = BeautifulSoup(nowplaying_response.text,'html.parser')
        self.sp2 = BeautifulSoup(later_response.text,'html.parser')
        
        self.cityname = self.sp1.find('title').text.strip().split(' ')[0]
        print(self.sp1)
        print(self.cityname)

        print("已完成基础页面访问!准备爬取详细信息")

        self.extract_href()
        self.extract_detail()
        self.save_detail('base.txt')

    def extract_href(self):

        self.nowplayinghref = []    
        li1 = self.sp1.find('ul', class_='lists')
        for li in li1.find_all('li', class_='list-item'):
            inner = li.find('li' , class_='stitle').find('a')
            self.nowplayinghref.append(inner['href'])

        #print(self.nowplayinghref)
        print(f"已爬到正在{self.cityname}热映的影片{len(self.nowplayinghref)}部")

        self.laterhref = []    
        li2 = self.sp2.find('div',id = 'showing-soon')
        for li in li2.find_all('div' , class_ = 'intro'):
            inner = li.find('h3').find('a')
            self.laterhref.append(inner['href'])

        #print(self.laterhref)
        print(f"已爬到即将在{self.cityname}上映的影片{len(self.laterhref)}部")
    
    def extract_detail(self):
        self.nowplayingdetail = []
        for i,href in enumerate(self.nowplayinghref):
            time.sleep(0.2)
            print(f"正在爬取第{i+1}/{len(self.nowplayinghref)}部正在热映影片信息")

            elem = [href]
            response = requests.get(href,headers=self.baseheader)
            sp = BeautifulSoup(response.text,'html.parser')
            target = sp.find('div' , class_ = "subjectwrap clearfix")
            elem.append(target)
            #elem.append(target.find('strong',class_ = "ll rating_num")) #豆瓣评分

            self.nowplayingdetail.append(elem)
        
        self.laterdetail = []
        for i,href in enumerate(self.laterhref):
            time.sleep(0.2)
            print(f"正在爬取第{i+1}/{len(self.laterhref)}部即将上映影片信息")      

            elem = [href]
            response = requests.get(href,headers=self.baseheader)
            sp = BeautifulSoup(response.text,'html.parser')
            target = sp.find('div' , class_ = "subjectwrap clearfix")
            elem.append(target)
            #elem.append(target.find('strong',class_ = "ll rating_num")) #豆瓣评分
            
            self.laterdetail.append(elem)
        
    def save_detail(self,file_name):
        # 因为爬虫不能使用太频繁，所以要保存一下结果咧！
        with open(file_name,"w") as f:
            f.write([self.nowplayingdetail,self.laterdetail])
        
# test
if __name__ == '__main__':
    a = DouBanFilmViewer()
    print(a.laterdetail[0])
