import requests
from bs4 import BeautifulSoup
import time
import json

class DouBanFilmViewer():

    #直接访问这两个url会转到对应城市哦！
    nowplayingurl = r"https://movie.douban.com/nowplaying"
    laterurl = r"https://movie.douban.com/later"
    detailurl = r"https://movie.douban.com/subject/" #后面加id即可，但前面已经爬到了所以这个可能用不上
    
    baseheader = {
        "User-Agent": "114514.1919810", #根据douban.com/robots.txt 其仅仅对User-Agent 为 “Wandoujia Spider” 和 “Mediapartners-Google” 有特殊规定。所以理论上UA可以乱填
        "Accept-Language": "zh-CN,zh;q=0.9",
        #放一个正常UA在这里备用。
        #"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/123 SLBVPV/64-bit",     
    }
    def __init__(self):
        pass

    def run(self):
        print("准备访问基础页面")
        nowplaying_response = requests.get(url=self.nowplayingurl, headers=self.baseheader, timeout=10)
        time.sleep(1)
        later_response = requests.get(url=self.laterurl, headers=self.baseheader, timeout=10)
        self.sp1 = BeautifulSoup(nowplaying_response.text,'html.parser')
        self.sp2 = BeautifulSoup(later_response.text,'html.parser')
        self.cityname = self.sp1.find('title').text.strip().split(' ')[0]
        self.savefilename = self.cityname + '.txt'
        print(self.sp1.find('title'),self.cityname)

        print("已完成基础页面访问!准备爬取详细信息")
        try:
            self.extract_href()
        except:
            # 用合肥默认配置
            self.nowplayinghref = eval("['https://movie.douban.com/subject/36954004/?from=playing_poster', 'https://movie.douban.com/subject/36215199/?from=playing_poster', 'https://movie.douban.com/subject/35907663/?from=playing_poster', 'https://movie.douban.com/subject/26149750/?from=playing_poster', 'https://movie.douban.com/subject/26938697/?from=playing_poster', 'https://movie.douban.com/subject/35411283/?from=playing_poster', 'https://movie.douban.com/subject/37143373/?from=playing_poster', 'https://movie.douban.com/subject/36445098/?from=playing_poster', 'https://movie.douban.com/subject/33415953/?from=playing_poster', 'https://movie.douban.com/subject/35603727/?from=playing_poster', 'https://movie.douban.com/subject/35364691/?from=playing_poster', 'https://movie.douban.com/subject/26908303/?from=playing_poster', 'https://movie.douban.com/subject/30290253/?from=playing_poster', 'https://movie.douban.com/subject/33455421/?from=playing_poster', 'https://movie.douban.com/subject/36097598/?from=playing_poster', 'https://movie.douban.com/subject/36166566/?from=playing_poster', 'https://movie.douban.com/subject/34780991/?from=playing_poster', 'https://movie.douban.com/subject/35938713/?from=playing_poster', 'https://movie.douban.com/subject/35295042/?from=playing_poster', 'https://movie.douban.com/subject/34800604/?from=playing_poster', 'https://movie.douban.com/subject/36282639/?from=playing_poster', 'https://movie.douban.com/subject/36289423/?from=playing_poster', 'https://movie.douban.com/subject/35902857/?from=playing_poster', 'https://movie.douban.com/subject/36177245/?from=playing_poster', 'https://movie.douban.com/subject/1291557/?from=playing_poster', 'https://movie.douban.com/subject/1297447/?from=playing_poster', 'https://movie.douban.com/subject/36970301/?from=playing_poster', 'https://movie.douban.com/subject/35624863/?from=playing_poster']")
            self.laterhref = eval("['https://movie.douban.com/subject/24750126/', 'https://movie.douban.com/subject/23761370/', 'https://movie.douban.com/subject/35782224/', 'https://movie.douban.com/subject/36251574/', 'https://movie.douban.com/subject/30313841/', 'https://movie.douban.com/subject/36135198/', 'https://movie.douban.com/subject/36959346/', 'https://movie.douban.com/subject/36478774/', 'https://movie.douban.com/subject/34938649/', 'https://movie.douban.com/subject/36673952/', 'https://movie.douban.com/subject/36803483/', 'https://movie.douban.com/subject/35873909/', 'https://movie.douban.com/subject/36597308/', 'https://movie.douban.com/subject/35927475/', 'https://movie.douban.com/subject/33414470/', 'https://movie.douban.com/subject/36896644/', 'https://movie.douban.com/subject/36512371/', 'https://movie.douban.com/subject/35929258/', 'https://movie.douban.com/subject/36978067/', 'https://movie.douban.com/subject/37039947/', 'https://movie.douban.com/subject/36319998/', 'https://movie.douban.com/subject/36988926/', 'https://movie.douban.com/subject/36851305/', 'https://movie.douban.com/subject/37298398/', 'https://movie.douban.com/subject/37302845/']")

        self.extract_detail()
        self.save_detail()
        
    def extract_href(self):

        self.nowplayinghref = []    
        li1 = self.sp1.find('ul', class_='lists')
        for li in li1.find_all('li', class_='list-item'):
            inner = li.find('li' , class_='stitle').find('a')
            self.nowplayinghref.append(inner['href'])

        print(self.nowplayinghref)
        print(f"已爬到正在{self.cityname}热映的影片{len(self.nowplayinghref)}部")

        self.laterhref = []    
        li2 = self.sp2.find('div',id = 'showing-soon')
        for li in li2.find_all('div' , class_ = 'intro'):
            inner = li.find('h3').find('a')
            self.laterhref.append(inner['href'])

        print(self.laterhref)
        print(f"已爬到即将在{self.cityname}上映的影片{len(self.laterhref)}部")
    
    def extract_detail(self):
        self.nowplayingdetail = []
        for i,href in enumerate(self.nowplayinghref):
            time.sleep(1)
            print(f"正在爬取第{i+1}/{len(self.nowplayinghref)}部正在热映影片信息")

            elem = [href]
            response = requests.get(href,headers=self.baseheader)
            sp = BeautifulSoup(response.text,'html.parser')
            target = sp.find('div' , class_ = "subjectwrap clearfix")
            elem.append(str(target))
            #elem.append(target.find('strong',class_ = "ll rating_num")) #豆瓣评分
            if target == None:
                print("未爬取到！可能是爬虫被反爬机制限制")
                raise RuntimeError('爬不到啊！')

            self.nowplayingdetail.append(elem)
        
        self.laterdetail = []
        for i,href in enumerate(self.laterhref):
            time.sleep(1)
            print(f"正在爬取第{i+1}/{len(self.laterhref)}部即将上映影片信息")      

            elem = [href]
            response = requests.get(href,headers=self.baseheader)
            sp = BeautifulSoup(response.text,'html.parser')
            target = sp.find('div' , class_ = "subjectwrap clearfix")
            elem.append(str(target))
            #elem.append(target.find('strong',class_ = "ll rating_num")) #豆瓣评分
            if target == None:
                print("未爬取到！可能是爬虫被反爬机制限制")
                raise RuntimeError('爬不到啊！')
            
            self.laterdetail.append(elem)
        
    def save_detail(self):
        # 因为爬虫不能使用太频繁，所以要保存一下结果咧！
        # print("nowplaying! ",self.nowplayingdetail)
        # print("later! ",self.laterdetail)
        # 居然有gbk无法搞定的字符。。
        with open(self.savefilename,"w",encoding='utf-8') as f:
            f.write(str([self.nowplayingdetail, self.laterdetail]))
        print("爬取完成！信息保存到" + self.savefilename)
        
# test
if __name__ == '__main__':
    a = DouBanFilmViewer()
    a.run()
