# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/30
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import time
from CeleryPro.task import add

for i in range(10):
    print('-- Job {} Start at:{}'.format(str(i).zfill(2), time.strftime('%H%M%S')))
    add.delay(i)