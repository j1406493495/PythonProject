
import urllib.request,socket,re,sys,os

'''
第一个示例：简单的网页爬虫
爬取豆瓣首页
'''


# 定义保存函数
def save_file(info):
    path = "/Users/wong/Desktop/douban.txt"
    f = open(path, 'wb')
    f.write(info)
    f.close()


def save_pic(path):
    target_path = "/Users/wong/Desktop/doubanImg"

    # 检测当前路径的有效性
    if not os.path.isdir(target_path):
        os.mkdir(target_path)

    # 设置每个图片的路径
    pos = path.rindex('/')
    t = os.path.join(target_path, path[pos + 1:])
    return t


# 网址
url = "http://www.douban.com/"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/51.0.2704.63 Safari/537.36'}
req = urllib.request.Request(url=url, headers=headers)

# 爬取结果
response = urllib.request.urlopen(req)

data = response.read()

save_file(data)

# 设置解码方式
data = data.decode('utf-8')

for link, t in set(re.findall(r'(https:[^s]*?(jpg|png|gif))', str(data))):
    print(link)
    try:
        urllib.request.urlretrieve(link, save_pic(link))
    except:
        print('失败')


# 打印结果
# print(data)

# 打印爬取网页的各类信息
# print(type(response))
# print(response.geturl())
# print(response.info())
# print(response.getcode())
