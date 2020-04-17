import os
import time
import random
import json
import csv
import pickle

from DecryptLogin import login


class JdMobileSpider(object):
    def __init__(self):
        if os.path.isfile('session.pkl'):
            print('[INFO]: 检测到已有会话文件session.pkl, 将直接导入该文件...')
            self.session = pickle.load(open('session.pkl', 'rb'))
            self.session.headers.update({'Referer': ''})
            # print(self.session.headers)
        else:
            self.session = JdMobileSpider.jd_login()
            f = open('session.pkl', 'wb')
            pickle.dump(self.session, f)
            f.close()

    def run(self):
        search_url = 'https://club.jd.com/comment/productPageComments.action?callback='
        all_comments = []
        for p in range(1,10):
            params = {
                "callback": "fetchJSON_comment98",
                "productId": 100012015172,
                "score": 2,
                "sortType": 5,
                "page": p,
                "pageSize": 10,
                "isShadowSku": 0,
                # "rid": 0,
                "fold": 1
            }
            response = self.session.get(search_url, params=params)
            response_json = json.loads(response.text)

            if not response_json['comments']:
                break
            else:
                comments_list = response_json['comments']
                for comment in comments_list:
                    content = comment['content']
                    nickname = comment['nickname']
                    score = comment['score']
                    id = comment['id']
                    creationTime = comment['creationTime']
                    days = comment['days']
                    productColor = comment['productColor']
                    productSize = comment['productSize']

                    info = {'id':id,"content":content,'nickname':nickname,'score':score,'days':days,'creationTime':creationTime,'productColor':productColor,'productSize':productSize}
                    print(info)
                    all_comments.append(info)
                    time.sleep(random.random() + 2.)

        self.__save(all_comments,'comments_normal.csv')
        print("数据写入完成!")
    '''数据保存'''
    def __save(self, data, savepath):
        headers = ['id','content','nickname','score','days','creationTime','productColor','productSize']
        with open(savepath, 'w', newline='',encoding='utf-8') as fp:
            writer = csv.DictWriter(fp, headers)
            writer.writeheader()
            writer.writerows(data)

    '''模拟登录京东'''

    @staticmethod
    def jd_login():
        username = "wwlzxukeqing@163.com"
        password = "12354abcs"
        lg = login.Login()
        infos_return, session = lg.jingdong(username=username, password=password)
        return session

    '''run'''


if __name__ == '__main__':
    crawler = JdMobileSpider()
    crawler.run()
