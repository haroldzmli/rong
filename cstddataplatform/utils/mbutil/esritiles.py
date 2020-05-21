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
from mbutil import mbtiles_connect, optimize_connection, mbtiles_setup, optimize_database, get_dirs
import sqlite3
import datetime
import json, logging

logger = logging.getLogger(__name__)


def esritiles_to_mbtiles(directory_path, mbtiles_file, metadata_file = ""):

    silent = False   # 安静模式
    compression = False  # 压缩

    if not silent:
        logger.info("Importing disk to MBTiles")
        logger.debug("%s --> %s" % (directory_path, mbtiles_file))

    con = mbtiles_connect(mbtiles_file, silent)
    cur = con.cursor()
    optimize_connection(cur)
    mbtiles_setup(cur)
    #~ image_format = 'png'
    image_format = 'png|jpg|tif'        # 支持的文件格式

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

    count = 0

    for zoom_dir in get_dirs(directory_path):
        if "L" in zoom_dir:
            z = int(zoom_dir[1:])
        for row_dir in get_dirs(os.path.join(directory_path, zoom_dir)):
            x = int(row_dir[1:],16)
            for current_file in os.listdir(os.path.join(directory_path, zoom_dir, row_dir)):
                file_name, ext = current_file.split('.',1)
                f = open(os.path.join(directory_path, zoom_dir, row_dir, current_file), 'rb')
                file_content = f.read()
                f.close()

                tile_size = len(file_content)
                if tile_size == 872: # png_kong = 876
                    continue
                y = int(file_name[1:],16)

                if (ext[1].lower() in image_format):
                    if not silent:
                        logger.debug(' Read tile from Zoom (z): %i\tCol (x): %i\tRow (y): %i' % (z, x, y))
                    cur.execute("""insert into tiles (zoom_level,
                        tile_column, tile_row, tile_data) values
                        (?, ?, ?, ?);""",
                                (z, x, y, sqlite3.Binary(file_content)))

    optimize_database(con, silent)
    endtime = datetime.datetime.now()     # 计算时间
    print("Mbtiles数据生成成功！运行时间（s）：", (endtime-starttime).seconds )
