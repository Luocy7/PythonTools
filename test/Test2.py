import re
from datetime import datetime, timedelta, timezone

text1 = 'tags: [Linux/Command]'
text2 = 'title: Centos7基于nginx搭建v2ray服务端配置vmess+tls+websocket完全手册'
text3 = '2019-10-11T08:28:52.029Z'
UTC_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
LOCAL_FORMAT = '%Y-%m-%d %H:%M:%S'

print(re.search(r'\[(.*)\]', text1).group(1))
# print(text2.replace('title: ', ''))


utc_dt = datetime.strptime(text3, UTC_FORMAT)
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
print(utc_dt.strftime(UTC_FORMAT))
print(bj_dt.strftime(LOCAL_FORMAT))