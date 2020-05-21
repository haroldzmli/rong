

import os
import os.path
from utils.mbutil.util import mbtiles_connect, optimize_connection, mbtiles_setup, optimize_database, get_dirs, \
    compression_prepare, compression_do, compression_finalize
import sqlite3
import datetime
import json, logging

logger = logging.getLogger(__name__)


# 解析天地图规则数据到MbTiles
# metadata.json 参数文件
def tdttiles_to_mbtiles(directory_path, mbtiles_file, metadata_file = ""):
    silent = False   # 安静模式
    compression = False  # 压缩
    if not silent:
        logger.info("Importing disk to MBTiles")
        logger.debug("%s --> %s" % (directory_path, mbtiles_file))

    con = mbtiles_connect(mbtiles_file, silent)
    cur = con.cursor()
    optimize_connection(cur)
    mbtiles_setup(cur)
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
    # 递归查找文件写入数据库
    findAllTiles(directory_path, cur, image_format, silent)
    if not silent:
        logger.debug('tiles (and grids) inserted.')
    # 是否压缩
    if compression:
        compression_prepare(cur, silent)
        compression_do(cur, con, 256, silent)
        compression_finalize(cur, con, silent)

    optimize_database(con, silent)
    endtime = datetime.datetime.now()     # 计算时间
    print("Mbtiles数据生成成功！运行时间（s）：", (endtime-starttime).seconds )


def findAllTiles(directory_path, cur, image_format, silent):
    # 遍历根目录
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # match 方法速度有点慢
            import re
            matchObj = re.match(r'(?P<img>.*)_(?P<proj>.*)_(?P<time>\d{8})_(?P<x>\d*)'
                                r'_(?P<y>\d*)_(?P<z>\d*).(?P<type>.*)', file, re.M | re.I)
            if matchObj:
                file_name = os.path.join(root, file)
                f = open(os.path.join(file_name), 'rb')
                file_content = f.read()
                f.close()
                x = int(matchObj.groupdict()['x'])
                y = int(matchObj.groupdict()['y'])
                z = int(matchObj.groupdict()['z'])
                image_type = matchObj.groupdict()['type']

                if image_type.lower() in image_format:
                    if not silent:
                        logger.debug(' Read tile from Zoom (z): %i\tCol (x): %i\tRow (y): %i' % (z, x, y))
                    cur.execute("""insert into tiles (zoom_level,
                                        tile_column, tile_row, tile_data) values
                                        (?, ?, ?, ?);""",
                                (z, x, y, sqlite3.Binary(file_content)))
        for dirname in dirs:
            # 递归调用自身,只改变目录名称
            findAllTiles(dirname, cur, image_format, silent)
