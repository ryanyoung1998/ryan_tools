from concurrent.futures import thread
from gevent import monkey,pool
# 将程序变成协作式运行，实现异步
# 需要在程序开始前将程序转变成协程
monkey.patch_all()

import re
import time
import requests
import gevent

# 记录程序开始时间
start = time.time()
print('程序开始运行时间：', start)

# getPictureName()      获取图片名字
# 参数 url              图片URL
# 返回值 picture_name   图片名
def getPictureName(url):
    picture_name = re.search("[\w|-]+.(jpg|gif|png|jpeg)", url)
    return picture_name.group()

# downloadPicture()     爬取并保存图片
# 参数 url              图片url    
# 返回值 None
def downloadPicture(url):
    # 截取picture原图url
    picture_url = url.split('?')[0]
    # 判断url中是否包含'.jpeg'
    if '.jpeg' in picture_url:
        print('图片链接：', picture_url)
        # 爬取图片
        picture = requests.get(picture_url, headers=browser_header)
        # 获取图片名
        picture_name = getPictureName(url=picture_url)
        # file_path = "Crawl_picture_1/" + picture_name
        # 以二进制方式打开一个文件,并保存图片
        with open(picture_name, 'wb+') as file:
            file.write(picture.content)
        print('已保存图片：', picture_name)

# https://www.pexels.com/zh-cn/api/v2/feed  Pexels_feed_url
# seed=2022-10-02T14:39:12.839Z             爬取开始时间
# per_page=5                                爬取图片数量
url = 'https://www.pexels.com/zh-cn/api/v2/feed?seed=2022-10-02T14:39:12.839Z&per_page=10'
# 浏览器的开发者工具获取user-agent、secret-key
browser_header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'secret-key': 'H2jk9uKnhRmL6WPwh89zBezWvr'}
# requests.get()发起请求
response = requests.get(url, headers=browser_header, allow_redirects=True)
# 匹配response中所有的download_link
download_link = re.findall(r'"download_link":"(.*?)"', response.text)
# 记录完成download_link解析时间
end = time.time()
print('解析download_link用时', end - start, '秒')

# 创建任务列表
task_list = []
# 限制线程数量
task_thread = pool.Pool(10)
# 遍历download_link
for link in download_link:
    # 创建任务
    task = task_thread.spawn(downloadPicture, link)
    # 将任务添加至任务列表
    task_list.append(task)
# 执行任务列表里的所有任务
gevent.joinall(task_list)

# 记录程序结束时间
end = time.time()
print('程序结束运行时间：', end)
print('程序运行了', end - start, '秒')
