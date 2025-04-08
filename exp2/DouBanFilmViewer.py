import requests
from bs4 import BeautifulSoup

class DouBanFilmViewer():

    #直接访问这两个url会转到对应城市哦！
    nowplayingurl = r"https://movie.douban.com/nowplaying"
    laterurl = r"https://movie.douban.com/later"
    detailurl = r"https://movie.douban.com/subject/" #后面加id即可，但前面已经爬到了所以这个可能用不上
    
    baseheader = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.douban.com/"
        }

    def __init__(self):
        nowplaying_response = requests.get(url=self.nowplayingurl, headers=self.baseheader, timeout=10)
        later_response = requests.get(url=self.laterurl, headers=self.baseheader, timeout=10)
        self.sp1 = BeautifulSoup(nowplaying_response.text,'html.parser')
        self.sp2 = BeautifulSoup(later_response.text,'html.parser')
        
        self.cityname = self.sp1.find('title').text.strip().split(' ')[0]
        # print(self.cityname)
        self.extract_href()
        self.extract_detail()

    def extract_href(self):

        self.nowplayinghref = []    
        li1 = self.sp1.find('ul', class_='lists')
        for li in li1.find_all('li', class_='list-item'):
            inner = li.find('li' , class_='stitle').find('a')
            self.nowplayinghref.append(inner['href'])

        #print(self.nowplayinghref)

        self.laterhref = []    
        li2 = self.sp2.find('div',id = 'showing-soon')
        for li in li2.find_all('div' , class_ = 'intro'):
            inner = li.find('h3').find('a')
            self.laterhref.append(inner['href'])

        #print(self.laterhref)
    
    def extract_detail(self):

        self.nowplayingdetail = []
        for href in self.nowplayinghref:
            response = requests.get()


# test
a = DouBanFilmViewer()
