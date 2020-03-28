# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/28
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import os
import time
import random
import requests
import imghdr

from requests import exceptions
from pathlib import Path
from dotenv import load_dotenv

from urllib.parse import urlparse

# from qiniu import Auth, put_file
# from qiniu import BucketManager

dotenv_path = Path(__file__).parent.absolute() / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)


def request(url, retry_times=5, timeout=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Referer': ''
    }

    while retry_times:
        try:
            t1 = time.time()
            res = requests.get(url, headers=headers, timeout=timeout)
            t2 = time.time()
        except exceptions.Timeout as e:
            # print('请求超时：' + str(e))
            retry_times -= 1
        except exceptions.HTTPError as e:
            # print('http请求错误:' + str(e))
            retry_times -= 1
        except exceptions.ConnectionError as e:
            # print('http连接错误:' + str(e))
            retry_times -= 1
        else:
            # 通过status_code判断请求结果是否正确
            # print('请求耗时%ss' % (t2 - t1))
            if res.status_code == 200:
                return res
            else:
                retry_times -= 1


class QnUpload(object):

    def __init__(self, workpath, source='local', dest='qn', download_folder='images', change_name=True):

        # work path init
        self.workpath = Path(workpath)
        self.isfolder = self.workpath.is_dir()

        # method init
        self.source_from = source
        self.upload_method = dest

        self.randomstring = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # qn init
        try:
            self.qn_access_key = os.getenv('QN_ACCESS_KEY')
            self.qn_secret_key = os.getenv('QN_SECRET_KEY')
            self.qn_bucket_name = os.getenv('QN_BUCKET_NAME')
            self.qn_bucket_url = os.getenv('QN_BUCKET_URL')
            # self.q = Auth(self.qn_access_key, self.qn_secret_key)
        except BaseException as err:
            print("Error in loadconf\n{},please check your config file".format(err))

        self.bucket = None

        # file download init
        self.dl_folder = Path(__file__).parent.absolute() / download_folder
        self.dl_folder.mkdir(exist_ok=True)
        self.change_name = change_name

    # format upload filename
    def format_key(self):
        return time.strftime('%Y%m%d%H%M%S') + '-' + random.choice(self.randomstring)

    def download_pic(self, url):
        r = request(url)
        if r:
            parsed = urlparse(url)
            suffix = imghdr.what('jpg', r.content)
            pic_name = Path(parsed.path).stem
            if self.change_name:
                pic_name = self.format_key()

            pic_file = self.dl_folder / '{}.{}'.format(pic_name, suffix)
            print(pic_file)
            with open(pic_file, 'wb') as f:
                f.write(r.content)


if __name__ == '__main__':
    a = 'https://pic2.zhimg.com/v2-4856bafdd3465f68b46f2c86038b55b0_250x0.jpg'
    foo = QnUpload('')
    foo.download_pic(a)
