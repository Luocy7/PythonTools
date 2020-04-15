# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/30
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import time
from CeleryPro import celery_ins


@celery_ins.task
def add(i):
    time.sleep(2)
    print('--!!--Job {} Done at:{}'.format(str(i).zfill(2), time.strftime('%H%M%S')))

