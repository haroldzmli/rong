from django.test import TestCase

# Create your tests here.
import os
import sqlite3

from tilecloud import Tile, TileCoord, consume, TileStore
from tilecloud.filter.contenttype import ContentTypeAdder
from tilecloud.store.mbtiles import MBTilesTileStore

# args =['/work/data/mbtiles/chn16y2019.mbtiles']
#
# tilestores = [(os.path.basename(arg), TileStore.load(arg)) for arg in args]
# tile = Tile(TileCoord(11, 1439, 794))
# # lengths = len(tilestores[0][1])
# # print(lengths)
# tile = tilestores[0][1].get_one(tile)
# print(tile)
# with open('ssss.png', 'wb') as file:
#     file.write(tile.data)
#
#
#
# aa = '6/10/40'
# bb = (aa,)
# print(bb)

# mapserver = {'china16':'/work/data/mbtiles/chn16y2019.mbtiles',}
#
# aaa = mapserver['china16']
# print(aaa)


# -*- coding:utf-8 -*-
import re

# # 验证手机号是否正确
#
# phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
#
# while True:
#     phone = input('请输入您的手机号:')
#
#     res = re.search(phone_pat, phone)
#     if res:
#         print('正常手机号')
#     else:
#         print('不是手机号')
# phonenum = '1368332301'
# phonenum = phonenum or ''
# try:
#     phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
#     re.search(phone_pat, phonenum)
# except ValueError:
#     pass
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
email = '111@qq.com'
aaa = BaseUserManager.normalize_email(email)
print(aaa)
#     print(phonenum)
# else:
#     print(ValueError)

# print(phonenum)