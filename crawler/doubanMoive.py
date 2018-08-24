import urllib.request, gzip, os
from bs4 import BeautifulSoup

movie_info = ''


# 解压缩数据
def ungzip(data):
    try:
        # print("正在解压缩...")
        data = gzip.decompress(data)
        # print("解压完毕...")
    except:
        print("未经压缩，无需解压...")
    return data


def save_pic(path):
    target_path = "/Users/wong/Desktop/movie_img"

    # 检测当前路径的有效性
    if not os.path.isdir(target_path):
        os.mkdir(target_path)

    # 设置每个图片的路径
    pos = path.rindex('/')
    t = os.path.join(target_path, path[pos + 1:])
    return t


def save_movie_to_file():
    path = "/Users/wong/Desktop/movie.txt"
    file = open(path, 'wb')
    file.write(movie_info.encode('utf-8'))
    file.close()


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
        urllib.request.urlretrieve(pic, save_pic(pic))
        # print(pic)

        hd = item.find('div', "hd")
        title_main = hd.find('span', "title").string
        title_other = hd.find('span', "other").string
        # print("title_main == " + title_main)
        # print("title_other == " + title_other)

        bd = item.find('div', "bd")
        actor_info = bd.p.get_text("", strip=True)
        star = bd.find('span', "rating_num").string
        star_people = bd.find('span', "rating_num").next_sibling.next_sibling.next_sibling.next_sibling.string
        quoteNode = bd.find('p', "quote")
        quote = ''
        if quoteNode is not None:
            quote = quoteNode.get_text("", strip=True)
        # print("actor_info == " + actor_info)
        # print("star == " + star)
        # print(star_people)
        # print("quote == " + quote)

        global movie_info
        movie_info += '==============\n'
        movie_info += pic + '\n'
        movie_info += title_main + title_other + '\n'
        movie_info += actor_info + '\n'
        movie_info += '豆瓣评分：' + star + '\n'
        movie_info += star_people + '\n'
        movie_info += quote + '\n'


# save_movie("https://movie.douban.com/top250?start=0&filter=")
for i in range(0, 10):
    url = "https://movie.douban.com/top250?start=" + str(i * 25) + "&filter="
    save_movie(url)
    save_movie_to_file()
