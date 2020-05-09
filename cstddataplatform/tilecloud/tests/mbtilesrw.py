import os
import sqlite3

from tilecloud import Tile, TileCoord, consume, TileStore
from tilecloud.filter.contenttype import ContentTypeAdder
from tilecloud.store.mbtiles import MBTilesTileStore

args =['/work/data/mbtiles/chn16y2019.mbtiles']

tilestores = [(os.path.basename(arg), TileStore.load(arg)) for arg in args]
tile = Tile(TileCoord(11, 1439, 794))
# lengths = len(tilestores[0][1])
# print(lengths)
tile = tilestores[0][1].get_one(tile)
print(tile)
with open('ssss.png', 'wb') as file:
    file.write(tile.data)



aa = '6/10/40'
bb = (aa,)
print(bb)
# tilestore = MBTilesTileStore(sqlite3.connect('/work/data/mbtiles/road-trip-wilderness.mbtiles'))
# lengths = len(tilestore)
# print(lengths)
# # 13/3104/6747
# # tilestream = [Tile(TileCoord(1, 0, 0), data=b'data'), None, Tile(TileCoord(1, 0, 1), error=True)]
# # tilestream = [Tile(TileCoord(13, 3104, 6747)), Tile(TileCoord(13, 3104, 6748))]
# # tilestore = MBTilesTileStore(sqlite3.connect(':memory:'), content_type='image/png')
# # , Tile(TileCoord(11, 1439, 795))
# tile = Tile(TileCoord(6, 10, 40))
# tile = tilestore.get_one(tile)
# print(tile)
# print(tilestream.content_type)
# print(tilestream.content_encoding)
# print(tilestream.data)
# consume(tilestream, None)
# content_type_adder = ContentTypeAdder()

# tile = content_type_adder(tile)
# with open('ssss.png', 'wb') as file:
#     file.write(tile)



# print(tilestream[0].content_type)
# print(tilestream[0].content_encoding)
# print(tilestream[0].data)
# print(tilestream[0].error)


# self.assertEqual(len(tilestore), 0)
# tilestream = [Tile(TileCoord(1, 0, 0), data=b'data'), None, Tile(TileCoord(1, 0, 1), error=True)]
# tilestream = tilestore.put(tilestream)
# tiles = list(tilestream)
# self.assertEqual(len(tilestore), 2)
# self.assertEqual(len(tiles), 2)
# self.assertEqual(tiles[0].tilecoord, TileCoord(1, 0, 0))
# self.assertEqual(tiles[0].data, b'data')
# self.assertEqual(tiles[1].tilecoord, TileCoord(1, 0, 1))
# self.assertEqual(tiles[1].error, True)
# self.assertTrue(Tile(TileCoord(1, 0, 0)) in tilestore)
# self.assertTrue(Tile(TileCoord(1, 0, 1)) in tilestore)
# tilestream = [Tile(TileCoord(1, 0, 0)), Tile(TileCoord(1, 0, 1))]
# tilestream = tilestore.get(tilestream)
# consume(tilestream, None)
# self.assertEqual(tilestore.get_cheap_bounding_pyramid(), BoundingPyramid({1: (Bounds(0, 1), Bounds(0, 2))}))
# self.assertEqual(len(tilestore), 2)
# tiles = list(tilestore.list())
# self.assertEqual(len(tiles), 2)
# tiles = sorted(tilestore.get_all())
# self.assertEqual(len(tiles), 2)
# self.assertEqual(tiles[0].tilecoord, TileCoord(1, 0, 0))
# self.assertEqual(bytes(tiles[0].data), b'data')
# self.assertEqual(tiles[1].tilecoord, TileCoord(1, 0, 1))
# self.assertEqual(tiles[1].data, None)
# tilestream = [Tile(TileCoord(1, 0, 0))]
# tilestream = tilestore.delete(tilestream)
# consume(tilestream, None)
# self.assertEqual(len(tilestore), 1)
# tiles = list(tilestore.get_all())
# self.assertEqual(len(tiles), 1)
# self.assertFalse(Tile(TileCoord(1, 0, 0)) in tilestore)
# self.assertTrue(Tile(TileCoord(1, 0, 1)) in tilestore)
#
# def test_metadata(self):
#     tilestore = MBTilesTileStore(sqlite3.connect(':memory:'))
#     tilestore.put_one(Tile(TileCoord(1, 0, 0)))
#     tilestore.put_one(Tile(TileCoord(2, 0, 0)))
#     tilestore.set_metadata_zooms()
#     self.assertEqual(int(tilestore.metadata['minzoom']), 1)
#     self.assertEqual(int(tilestore.metadata['maxzoom']), 2)
#     self.assertEqual(sorted(tilestore.metadata.itervalues()), ['1', '2'])
#     self.assertEqual(sorted(tilestore.metadata.keys()), ['maxzoom', 'minzoom'])
#
# def test_content_type(self):
#     connection = sqlite3.connect(':memory:')
#     tilestore1 = MBTilesTileStore(connection)
#     tilestore1.metadata['format'] = 'png'
#     tilestore2 = MBTilesTileStore(connection)
#     self.assertEqual(tilestore2.content_type, 'image/png')
#
# def test_empty(self):
#     connection = sqlite3.connect(':memory:')
#     tilestore = MBTilesTileStore(connection)
#     self.assertEqual(len(tilestore), 0)
#     self.assertEqual(tilestore.get_one(Tile(TileCoord(0, 0, 0))), None)