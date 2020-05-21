#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Version  : 1.0
# @Date     : 2018/3/5 16:11
# @Author   : Zhang Erfeng
# @Email    : zhang2feng@126.com
# @File     : esritile.py
# @Software : PyCharm
# @Project  : 2FengStudioPyTools

"""
定义了一个EsriCompactCache类，用不带后缀的bundle文件名（如'R22e80C14380')进行实例化。
包含以下属性：
name                      对象名称，如'R22e80C14380'
bundle_name               bundle文件名，如'R22e80C14380.bundle'
bundlx_name               bundlx文件名，如'R22e80C14380.bundlx'
package_row               package的行号，如1117（R22e80转十进制后，除以128所得）
package_col               package的列号，如647（C14380转十进制后，除以128所得）
package_row_min, max      package内部瓦片的最小行号、最大行号，如142976（R22e80转十进制后所得）、143104（最小行号+128所得）
package_col_min, max      package内部瓦片的最小列号、最大列号，如82816（C14380转十进制后所得）、82944（最小行号+128所得）
package_extent_row_col    package内部瓦片行列范围（最小行号，最大行号，最小列号，最大列号）如(142976, 143104, 82816, 82944)
"""

import os
import os.path
import time
import multiprocessing
from io import BytesIO
from multiprocessing import Pool
from mbutil import mbtiles_connect, optimize_connection, mbtiles_setup, optimize_database
import sqlite3
import datetime
import json, logging

logger = logging.getLogger(__name__)

# 得到指定路径下的所有esri压缩包
def get_bundle_list_from_dir(compact_cache_dir):
    bundle_list = []
    for root, dirs, files in os.walk(compact_cache_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.bundle':
                lev = int(os.path.split(root)[1][1:])
                bundle_list.append([lev, os.path.splitext(file)[0], root])
    return bundle_list

# 解析Esri压缩包数据到MbTiles
# metadata.json 参数文件
def esripack_to_mbtiles(directory_path, mbtiles_file, metadata_file = ""):
    silent = False   # 安静模式
    con = mbtiles_connect(mbtiles_file, silent)
    cur = con.cursor()
    optimize_connection(cur)
    mbtiles_setup(cur)

    starttime = datetime.datetime.now()     # 计算时间
    # 写入配置参数
    try:
        metadata = json.load(open(metadata_file, 'r')) # metadata.json
        for name, value in metadata.items():
            cur.execute('insert into metadata (name, value) values (?, ?)',
                (name, value))
        if not silent:
            logger.info('metadata from metadata.json restored')
    except IOError:
        if not silent:
            logger.warning('metadata.json not found')

    bundle_list = get_bundle_list_from_dir( directory_path )
    for bundle in bundle_list:
        get_tdt_tile_from_bundle(bundle,cur)

    optimize_database(con, silent)
    endtime = datetime.datetime.now()     # 计算时间
    print("Mbtiles数据生成成功！运行时间（s）：", (endtime-starttime).seconds )

# 解析一个压缩包文件
def get_tdt_tile_from_bundle(bundle, cur):
    filebundlx = os.path.join(bundle[2],"%s.bundlx" % bundle[1])
    filebundle = os.path.join(bundle[2],"%s.bundle" % bundle[1])

    rowb = int(str(bundle[1]).split('C')[0][1:], 16)         # 基础行x
    colb = int(str(bundle[1]).split('C')[1], 16)             # 基础列y

    f = open(filebundlx, 'rb')
    f.seek(16)
    file_content = f.read( 5*128*128 )
    f.close()

    # 实体文件
    fimg = open(filebundle, 'rb')
    for row in range(128):
        for col in range(128):
            pos = int.from_bytes(file_content[row*128*5+col*5 : row*128*5+col*5+5], 'little')   # 每个瓦片的位置
            fimg.seek(pos)
            tile_size = int.from_bytes(fimg.read(4), 'little')
            if tile_size == 0:
                tile = None
            elif tile_size == 872: # png_kong = 876
                tile = None
            else:
                tile = fimg.read(tile_size)
                cur.execute("""insert into tiles (zoom_level,
                    tile_column, tile_row, tile_data) values
                    (?, ?, ?, ?);""",
                            (bundle[0], rowb+row, colb+col, sqlite3.Binary(tile)))

    fimg.close()
    return
