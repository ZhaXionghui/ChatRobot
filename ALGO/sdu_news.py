import requests
import bs4
import os
import datetime
from requests.adapters import HTTPAdapter

def fetchUrl(url):
    """
    功能：访问 url 的网页，获取网页内容并返回
    参数：目标网页的 url
    返回：目标网页的 html 内容
    """

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46',
    }
    s = requests.session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    global r
    r = requests.get(url, headers=headers, timeout=5)
    R = str(r)
    if R == '<Response [404]>':
        return '404'
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text


def getHeadlines(url):
    """
    功能：获取当天新闻的各头条的版面的链接列表
    参数：年，月，日
    """
    html = fetchUrl(url)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    temp = bsobj.find_all('span',class_="shadow")
    temp_top=bsobj.find("h2")
    print(temp_top)
    list=[]
    if temp is not None:
        for i in temp:
            if "https" in i.a["href"]:
                link = i.a["href"]
                list.append(link)
            else: continue
    else:
        return 'No page'
    list.insert(0,"https://view.sdu.edu.cn/"+temp_top.a["href"])
    print(list)
    return list

def getHighlights(url):
    """
    功能：获取当天新闻的要闻各版面的链接列表
    参数：年，月，日
    """
    html = fetchUrl(url)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    temp = bsobj.find_all("ul")
    temp1=temp[3].find_all("a") + temp[4].find_all("a")
    list=[]
    if temp1 is not None:
        for i in temp1:
            link ="https://view.sdu.edu.cn/" + i["href"]
            list.append(link)
    else:
        return 'No page'
    return list

def getAcademic(url):
    """
    功能：获取当天新闻的要闻各版面的链接列表
    参数：年，月，日
    """
    html = fetchUrl(url)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    temp_top = bsobj.find_all("dl")
    temp1=bsobj.find_all("ul")[5].find_all("a")
    list=[]
    if temp_top is not None or temp1 is not None:
        for i in temp_top:
            if "1021" in i.find("dt").a["href"]:
                link = "https://view.sdu.edu.cn/" + i.find("dt").a["href"]
                list.append(link)
            else:pass

        for i in temp1:
            link = "https://view.sdu.edu.cn/" + i["href"]
            list.append(link)
    else:
        return "No page"
    return list

def getContent(html):
    """
    功能：解析 HTML 网页，获取新闻的文章内容
    参数：网页地址
    """
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    temp = bsobj.find('title')
    # 获取文章 标题
    title = temp.text
    # 获取文章 内容
    pList = bsobj.find('div', class_="news_content").find_all('p')
    content = ''
    for p in pList:
        content += p.text
    # 返回结果 标题+内容
    resp = title + content
    return resp

def saveFile(content, path, filename):
    """
    功能：将文章内容 content 保存到本地文件中
    参数：要保存的内容，路径，文件名
    """
    # 如果没有该文件夹，则自动生成
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    with open(path + filename, 'w', encoding='utf-8') as f:
        f.write(content)


def saveFile_add(content, path, filename):
    """
    功能：保存错误信息至同一个TXT文件中
    参数：要保存的内容，路径，文件名
    """
    # 如果没有该文件夹，则自动生成
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    with open(path + filename, 'a', encoding='utf-8') as f:
        f.write(content)


def download_headlines(destdir):
    """
    功能：爬取山大新闻网站 当天的 部分新闻内容，并保存在 指定目录下
    参数：文件保存的根目录
    """
    # try:
    today = datetime.date.today()
    now = today.strftime('%y%m%d')
    print(now)
    pageList = getHeadlines("https://view.sdu.edu.cn/")
    if pageList == 'No page':
        saveFile_add(now + '\r\n', './', '错误文件.txt')
        pass

    print('PageList:', pageList)

    q = 0
    for url in pageList:
        # 获取新闻文章内容
        html = fetchUrl(url)
        if html == '404':
            saveFile_add(now + '\r\n', './', '错误文件.txt')
            continue
        content = getContent(html)
        print('内容:', content)
        print(url)
        # 生成保存的文件路径及文件名-

        temp = str(q)
        q = q + 1
        print('list:', temp)
        path = destdir + '/' + now + '/'
        # global fileName
        fileName = now + '-' + temp + '.txt'

        # 保存文件
        saveFile(content, path, fileName)


def download_heghlights(destdir):
    """
    功能：爬取山大新闻网站 当天的 要闻内容，并保存在 指定目录下
    参数：文件保存的根目录
    """
    # try:
    today = datetime.date.today()
    now = today.strftime('%y%m%d')
    print(now)
    pageList = getHighlights("https://view.sdu.edu.cn/")
    if pageList == 'No page':
        saveFile_add(now + '\r\n', './', '错误文件.txt')
        pass

    print('PageList:', pageList)
    q=0
    for url in pageList:
    # 获取新闻文章内容
        html = fetchUrl(url)
        if html == '404':
            saveFile_add(now+ '\r\n', './', '错误文件.txt')
            continue
        content = getContent(html)
        print('内容:', content)
        print(url)
        # 生成保存的文件路径及文件名-

        temp = str(q)
        q=q+1
        print('list:', temp)
        path = destdir + '/' + now + '/'
        fileName = now + '-' + temp + '.txt'
        # 保存文件
        saveFile(content, path, fileName)

def download_academic(destdir):
    """
    功能：爬取山大新闻网站 当天的 学术新闻内容，并保存在 指定目录下
    参数：文件保存的根目录
    """
    today = datetime.date.today()
    now = today.strftime('%y%m%d')
    print(now)
    pageList = getAcademic("https://view.sdu.edu.cn/")
    if pageList == 'No page':
        saveFile_add(now + '\r\n', './', '错误文件.txt')
        pass

    print('PageList:', pageList)
    q=0
    for url in pageList:
    # 获取新闻文章内容
        html = fetchUrl(url)
        if html == '404':
            saveFile_add(now+ '\r\n', './', '错误文件.txt')
            continue
        content = getContent(html)
        print('内容:', content)
        print(url)
        # 生成保存的文件路径及文件名

        temp = str(q)
        q=q+1
        print('list:', temp)
        path = destdir + '/' + now + '/'
        fileName = now + '-' + temp + '.txt'
        # 保存文件
        saveFile(content, path, fileName)


if __name__ == '__main__':
    '''
    主函数：程序入口
    '''
    
    destdir1 = "news/headlines"
    destdir2 = "news/highlights"
    destdir3 = "news/academic"
    download_academic(destdir3)
    download_headlines(destdir1)
    download_heghlights(destdir2)