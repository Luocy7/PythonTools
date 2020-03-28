# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/28
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import os
import re
import time
import random

from pathlib import Path
from dotenv import load_dotenv

from urllib.parse import urlparse
from SingleTool.Download import download_pic

from qiniu import Auth, put_file, etag
from qiniu import BucketManager

dotenv_path = Path(__file__).parent.absolute() / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)


class QnUpload(object):

    def __init__(self, download_folder='images', change_name=True):

        # file download init
        self.dl_folder = Path(__file__).parent.absolute() / download_folder
        self.dl_folder.mkdir(exist_ok=True)

        self.change_name = change_name

        self.randomstring = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # qn init
        try:
            self.qn_access_key = os.getenv('QN_ACCESS_KEY')
            self.qn_secret_key = os.getenv('QN_SECRET_KEY')
            self.qn_bucket_name = os.getenv('QN_BUCKET_NAME')
            self.qn_bucket_url = os.getenv('QN_BUCKET_URL')
            self.q = Auth(self.qn_access_key, self.qn_secret_key)
        except BaseException as err:
            print("Error in loadconf\n{},please check your config file".format(err))

        self.bucket = None
        self.token = self.geneate_token(expires=3600)

    def geneate_token(self, expires=15552000):
        return self.q.upload_token(self.qn_bucket_name, expires=expires)

    # format upload filename
    def format_key(self):
        ct = time.time()
        data_head = time.strftime("%Y%m%d%H%M%S")
        data_secs = (ct - int(ct)) * 1000
        return "%s%03d%s" % (data_head, data_secs, random.choice(self.randomstring))

    def download_pic(self, url: str) -> Path:
        parsed = urlparse(url)
        pic_name = Path(parsed.path).stem
        if self.change_name:
            pic_name = self.format_key()

        pic_file = self.dl_folder / pic_name
        dl_file = download_pic(url, pic_file)
        return dl_file

    def upload_pic(self, img_file: Path) -> str:
        try:
            key = img_file.name
            ret, info = put_file(self.token, key, img_file)
            assert ret['key'] == key
            assert ret['hash'] == etag(img_file)
            return self.qn_bucket_url + key
        except BaseException as err:
            print("Error in Uploading {} to qn\n{}".format(img_file, err))
            return str(img_file)

    def crawling_pic(self, url: str) -> str:
        """

        @param url:
        @return:
        """
        if not url.startswith(self.qn_bucket_url):
            try:
                bucket = BucketManager(self.q)
                key = self.format_key()
                bucket.fetch(url, self.qn_bucket_name, key)
                ret, info = bucket.stat(self.qn_bucket_name, key)
                print(info)
                assert ret['key'] == key
                return self.qn_bucket_url + key
            except BaseException as err:
                print("Error in Crawling {} to qn\n{}".format(url, err))
        return url

    def start(self, url, upload=False):
        """

        @param url:
        @param upload: For Internet Images: download or upload to Qiuniu. Default is download
        @return: Absolute Local Path or Qiuniu Url
        """

        # Origin: Internet
        if re.match('((http(s?))|(ftp))://.*', url):
            return self.download_pic(url) if upload else self.crawling_pic(url)
        # Origin: Local
        elif re.match('([C-Z]:\\.*)|(\\.*)', url):
            if Path(url).exists():
                return self.upload_pic(url)
        else:
            pass


qiniu_up = QnUpload()

if __name__ == '__main__':
    a = 'https://pic2.zhimg.com/v2-4856bafdd3465f68b46f2c86038b55b0_250x0.jpg'
    foo = QnUpload('')
    foo.download_pic(a)
