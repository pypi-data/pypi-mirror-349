# FEAPDER

![](https://img.shields.io/badge/python-3.6-brightgreen)

## 环境要求：

- Python 3.6.0+
- Works on Linux, Windows, macOS

## 安装

From PyPi:

```shell
pip install nbclass
```

## 更新
### 1.4版本
*  1.4 添加装饰器
*  1.4.6 更新数据库查询, 哈希加密工具
* 1.4.7 添加AES加解密工具
```python
from nbclass import tools

key = '1234567890123456'
print(tools.aes_encrypt_cbc(key, '人生苦短我用python', key))  # => YkeE6FB0FhZaXYsj+AYWMiTJDdOJS4g1EQzZ1WRN2DQ=
print(tools.aes_encrypt_cbc(key, '人生苦短我用python', key, is_hex=True))  # => 624784e8507416165a5d8b23f806163224c90dd3894b8835110cd9d5644dd834
```
* 1.4.8 添加Hmac加解密方法
```python
from nbclass import tools

tools.get_hmac_md5('123456', '人生苦短我用python')
tools.get_hmac_sha1('123456', '人生苦短我用python')
tools.get_hmac_sha256('123456', '人生苦短我用python')
tools.get_hmac_sha256('123456', '人生苦短我用python')
```
### 1.5版本
* 1.5.0 添加账号管理池
```python
from typing import Optional

from nbclass.db.mysqldb import MysqlDB
from nbclass.db.redisdb import RedisDB
from nbclass.decorators import singleton
from nbclass.network.user_pool import NormalUser
from nbclass.network.user_pool import NormalUserPool


@singleton
class MysqlDB1341(MysqlDB):

    def __init__(self):
        super().__init__(
            ip='192.168.1.110',
            port=3306,
            db='test',
            user_name='python',
            user_pass='123456975.20',
        )


class RedisDB28(RedisDB):

    def __init__(self, db=0):
        super().__init__(
            ip_ports='192.168.2.28:6379',
            db=db,
            user_pass='feapderYYDS'
        )


class TestGuestUserPool(NormalUserPool):

    def login(self, user) -> Optional[NormalUser]:
        user = NormalUser(
            user_id=user.user_id,
            username=user.username,
            password=user.password,
            token='CAOJrYvo0VINfMyMKXeIUcNlDhteJfQk_uIg_bIeCj65b0XLJbIxoNiuIPIIle2FAbhQ_V6TklV5pwNcSTirqQ',
            mobile=None
        )
        return user


if __name__ == '__main__':
    user_pool = TestGuestUserPool(
        redis_cli=RedisDB28(db=1),
        mysql_cli=MysqlDB1341(),
        redis_key="python:mtUserPool",
        table_userbase='py_user_pool',
        keep_alive=True,
    )
    users = user_pool.get_user()
    print("取到user：", users)

```


## 爬虫工具推荐

1. 爬虫在线工具库：http://www.spidertools.cn
2. 验证码识别库：https://github.com/sml2h3/ddddocr
