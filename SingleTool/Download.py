# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/28
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import time
import imghdr
import requests
from requests import exceptions, Response
from pathlib import Path


def request(url, retry_times=5, timeout=1) -> Response:
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
            print('请求超时：' + str(e))
            retry_times -= 1
        except exceptions.HTTPError as e:
            print('http请求错误:' + str(e))
            retry_times -= 1
        except exceptions.ConnectionError as e:
            print('http连接错误:' + str(e))
            retry_times -= 1
        else:
            # 通过status_code判断请求结果是否正确
            print('请求耗时%ss' % (t2 - t1))
            if res.status_code == 200:
                return res
            else:
                retry_times -= 1


def download_pic(url: str, dl_path: Path):
    res = request(url)
    if res:
        suffix = imghdr.what('jpg', res.content)
        if not suffix:
            raise  # todo: raise error "not an image"

        pic_file = dl_path.parent / "{}.{}".format(dl_path.stem, suffix)
        pic_file.write_bytes(res.content)
        return pic_file
    return url
