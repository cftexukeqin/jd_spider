import requests
import json
from bs4 import BeautifulSoup as bs
import time, pandas
from datetime import datetime


def get_comments(url):
    res = requests.get(url)
    result = res.text.split('fetchJSON_comment98vv40575(')[1].split(');')[0]
    result = json.loads(result)
    comments = []
    comment_list = result['comments']
    for i in comment_list:
        comments.append(i['content'])
    return comments


def save_data():
    global time_stamp
    df = pandas.DataFrame(total_comments)
    df.to_excel('Cpu.xlsx')
    end_time = datetime.now()
    time_stamp = (end_time - start_time).total_seconds()
    print('Success')


if __name__ == '__main__':
    print('Spidering...')
    start_time = datetime.now()
    total_comments = []
    url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv40575&productId=3701943&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
    for i in range(0, 200):
        new_url = url.format(i)
        comms = get_comments(new_url)
        total_comments.extend(comms)
    length = len(total_comments)
    save_data()
    print('共爬取%s页%s条好评,用时%s秒' % (i + 1, length, time_stamp))
