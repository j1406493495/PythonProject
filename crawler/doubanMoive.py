import urllib.request, gzip
from bs4 import BeautifulSoup


# 解压缩数据
def ungzip(data):
    try:
        # print("正在解压缩...")
        data = gzip.decompress(data)
        # print("解压完毕...")
    except:
        print("未经压缩，无需解压...")
    return data


def save_movie(url):
    headers = {
        "Host": "movie.douban.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/68.0.3440.106 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6"
    }

    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    data = ungzip(data)
    data = data.decode('utf-8')

    soup = BeautifulSoup(data, "html5lib")
    items = soup.find_all('div', "item")
    for item in items:
        pic = item.find('img')['src']
        print(pic)


for i in range(0, 10):
    url = "https://movie.douban.com/top250?start=" + str(i * 25) + "&filter="
    save_movie(url)
