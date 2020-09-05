from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import sqlite3

def main():
    baseurl = "https://movie.douban.com/top250?start="
    #爬取网页
    datalist = getData(baseurl)
    savepath = ".\\豆瓣电影top250.xls"
    #保存数据
    #saveData(savepath)

    #askURL("https://movie.douban.com/top250?start=")


#影片详情链接的规则
findlink = re.compile(r'<a href="(.*?)">')     #创建正则表达式对象来表示规则（字符串模式）
#影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)   #re.S. 让换行符包含在字符中
#影片的片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)




#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,1):    #调用获取页面信息的函数 10次
        url = baseurl + str(i*25)
        html = askURL(url)   #保存获取到的网页源码
    
        #逐一解析数据
        soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all('div',class_="item"):  #查找符合要求的字符串
            #print(item) #测试查看电影item的全部信息
            data = []    #保存一部电影的所有信息
            item = str(item)
            
            #影片详情的链接
            link = re.findall(findlink,item)[0]   #re库用于通过正则表达式查找指定字符串
            data.append(link)                     #添加链接
            
            ImgSrc = re.findall(findImgSrc,item)[0]
            data.append(ImgSrc)                   #添加图片
            
            titles = re.findall(findTitle,item)   #片名可能只有一个中文名没有外文名
            if(len(titles) == 2) :
                ctitle = titles[0]                #添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/","")   #去掉无关符号
                data.append(otitle)                  #添加外国名
            else:
                data.append(titles[0])
                data.append('')           #外国名留空
            
            rating = re.findall(findRating,item)[0]   
            data.append(rating)                      #添加评分

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)                    #添加评价人数

            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")   #去掉句号
                data.append(inq)                         #添加概述
            else:
                data.append(" ")
            
            
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)    #去掉<br/>
            bd = re.sub('/'," ",bd)    #替换/
            data.append(bd.strip())    #去掉前后空格


            datalist.append(data)      #把处理好的一部电影信息放入datalist

    print(datalist)  
    return datalist     #for 和 return 循环格式一定要对齐（这里对齐第一个for），否则只会显示第一部电影的链接，或者只爬取第一页面内容

            




            
      




#得到指定一个url的网页内容
def askURL(url): #模拟浏览器头部信息，向豆瓣服务器发送消息 (注意User-Agent一定不要有空格) （直接打开http://www.useragentstring.com/ 也可查询使用者信息）
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    }          #用户代理表示告诉豆瓣服务器：我是浏览器，本质上是告诉浏览器我们可接受什么水平文件内容
                            
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    
    return html

#保存数据
def saveData(savepath):
    print('save...')

if __name__ == "__main__":
    main()
