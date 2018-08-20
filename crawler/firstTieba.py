from urllib import request

url = "http://tieba.baidu.com/p/1753935195"
page = request.urlopen(url, timeout=1)
print(page.read().decode('utf-8'))