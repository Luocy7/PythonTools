# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/30
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from celery import Celery

celery_ins = Celery(__name__,broker='redis://192.168.235.129:6379/3')
celery_ins.config_from_object('CeleryPro.celery_cfg')
