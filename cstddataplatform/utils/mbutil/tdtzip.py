
import zipfile

import os
import os.path
from mbutil import mbtiles_connect, optimize_connection, mbtiles_setup, optimize_database, get_dirs
import sqlite3
import datetime
import json, logging

logger = logging.getLogger(__name__)


def tdtzip_to_mbtiles(zipfile_path, mbtiles_file, metadata_file = ""):

    silent = False   # 安静模式
    compression = False  # 压缩

    if not silent:
        logger.info("Importing disk to MBTiles")
        logger.debug("%s --> %s" % (zipfile_path, mbtiles_file))

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

    zf = zipfile.ZipFile(zipfile_path, "r")
    for file in zf.namelist():
        import re
        matchObj = re.match(r'(?P<img>.*)_(?P<proj>.*)_(?P<time>\d{8})_(?P<x>\d*)'
                            r'_(?P<y>\d*)_(?P<z>\d*).(?P<type>.*)', file, re.M | re.I)
        if matchObj:
            x = int(matchObj.groupdict()['x'])
            y = int(matchObj.groupdict()['y'])
            z = int(matchObj.groupdict()['z'])
            image_type = matchObj.groupdict()['type']
            if image_type.lower() in image_format:
                bytes = zf.read(file)
                xyz = file.split('_')
                x = int(xyz[-3])
                y = int(xyz[-2])
                z = int(xyz[-1].split('.')[0])

                if not silent:
                    logger.debug(' Read tile from Zoom (z): %i\tCol (x): %i\tRow (y): %i' % (z, x, y))
                cur.execute("""insert into tiles (zoom_level,
                    tile_column, tile_row, tile_data) values
                    (?, ?, ?, ?);""",
                            (z, x, y, sqlite3.Binary(bytes)))

    optimize_database(con, silent)
    endtime = datetime.datetime.now()     # 计算时间
    print("Mbtiles数据生成成功！运行时间（s）：", (endtime-starttime).seconds )

def read_tdtzip(strZip):
    z = zipfile.ZipFile(strZip, "r")
    for filename in z.namelist():
        print(filename)
        bytes = z.read(filename)
        print( len(bytes) )
    return

