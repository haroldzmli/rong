"""
主要完成功能：
1、将mibtiles文件倒入数据库，并完成迁移
2、主要完成map mapdata两个表。
3、主要完成瓦片、zip文件转mibiltes的工作。
"""
import datetime
import os
import shutil
import time

from cstddataplatform import settings
from utils.mbutil.tdttiles import tdttiles_to_mbtiles
from utils.mbutil.util import mbtiles_connect, optimize_connection


def format_file_name(name):
    '''
    去掉名称中的url关键字
    '''
    URL_KEY_WORDS = ['#', '?', '/', '&', '.', '%']
    for key in URL_KEY_WORDS:
        name_list = name.split(key)
        name = ''.join(name_list)
    return name


def readFile2db(filepath, user_id):
    image_format = 'mbtiles|zip'
    filename = os.path.basename(filepath)
    filename_list = filename.split('.')
    file_postfix = filename_list[-1]  # 后缀
    print(file_postfix)
    if file_postfix.lower() in image_format:
        filename_list_clean = filename_list[:-1]
        file_name = ''.join(filename_list_clean) + str(int(time.time() * 1000))
        file_name = format_file_name(file_name)
        sub_folder = time.strftime("%Y%m")
        upload_folder = os.path.join(settings.MEDIA_ROOT, 'upload', sub_folder, user_id)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        absolute_path = os.path.join(upload_folder, file_name) + '.%s' % file_postfix
        shutil.copy(filepath, absolute_path)
        return file_name, absolute_path


# def readtiles2db(tilespath, mbtilepath):
#     print(tilespath,mbtilepath)
#     tdttiles_to_mbtiles(tilespath, mbtilepath)

def writetable(dbfile, userid, username, filepath, filename=''):

    if os.path.isdir(filepath) and filename:
        tdttiles_to_mbtiles(filepath, filename)
        filepath = filename

    save_name, save_path = readFile2db(filepath, str(userid))
    name = os.path.splitext(save_name)[0]  # 分割，不带后缀名
    silent = False
    con = mbtiles_connect(dbfile, silent)
    cur = con.cursor()
    # cur.execute("""insert into tiles (zoom_level,
    #                                        tile_column, tile_row, tile_data) values
    #                                        (?, ?, ?, ?);""",
    #             (z, x, y, sqlite3.Binary(file_content)))
    # now_time = time.strftime('%Y-%m-%d  %H:%M:%S.%f', time.localtime())
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    cur.execute('insert into tileserver_mapdata (name, author, author_id, save_name, save_path, description, is_deleted, create_time, end_time ) values (?, ?, ?, ?,?, ?, ?, ? , ?)',
                (name, 'admin', 1, save_name, save_path, name, 0, now_time, now_time))
    # cur.execute('insert into metadata (name, value) values (?, ?)',(name, value))
    con.commit()
    cur.execute('select last_insert_rowid() from tileserver_mapdata')
    data = cur.fetchone()
    print(data[0])

    cur.execute(
        'insert into tileserver_map (name, creator, creator_id, description, is_deleted, create_time, modified_time, map_data ) values (?, ?, ?, ?,?, ?, ?, ?)',
        (name, 'admin', 1, name, 0, now_time, now_time, str(data[0] -1)))

    # cur.execute(
    #     'insert into tileserver_map (name, creator, creator_id, description, is_deleted, create_time, modified_time, map_data ) values (?, ?, ?, ?,?, ?, ?, ?)',
    #     (name, 'admin', 1, name, 0, now_time, now_time, str(data[0])))

    con.commit()
    cur.close()
    con.close()
    return str(userid)+'/'+name

# 参数
# 参数1：服务的数据库文件名称,user_id, username, 文件路径（如果是mbtiles zip格式的就是直接发布；如果是文件路径就倒入mbtiles，此时需要指定文件名称）
name = writetable('/work/cstd/rong/cstddataplatform/test.sqlite3',str(1), 'admin',  "/work/data/tiles/qingdaohutai/20190623",
                  '/work/data/tiles/qingdaohutai/test1.mbtiles')
print('url:', name)
