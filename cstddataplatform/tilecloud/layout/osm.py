import re

from tilecloud import TileCoord
from tilecloud.layout.re_ import RETileLayout


class OSMTileLayout(RETileLayout):
    """OpenStreetMap tile layout"""

    PATTERN = r'[0-9]+/[0-9]+/[0-9]+'
    RE = re.compile(r'([0-9]+)/([0-9]+)/([0-9]+)\Z')

    def __init__(self):
        RETileLayout.__init__(self, self.PATTERN, self.RE)

    @staticmethod
    def filename(tilecoord, metadata=None):
        # todo 此处需要作tdt googlemap等的判断，现在暂时就是完全天地图格式
        # if metadata:
        grade = tilecoord.z // 5
        tmp_row = tilecoord.x
        tmp_col = tilecoord.y
        mid_paths = []
        for i in range(grade):
            tmp_row = tmp_row // 32
            tmp_col = tmp_col // 32
            mid_row = tmp_row % 32
            mid_col = tmp_col % 32
            mid_paths.insert(0, "%02d%02d" % (mid_col, mid_row))
        return str(tilecoord.z) + '/' + '/'.join(mid_paths) + '/' + 'img_w_99999999_' + \
            str(tilecoord.y) + '_' + str(tilecoord.x) + '_' + str(tilecoord.z)
        # return '{0:d}/{1:d}/{2:d}'.format(tilecoord.z, tilecoord.x, tilecoord.y)

    @staticmethod
    def _tilecoord(match):
        return TileCoord(*map(int, match.groups()))
