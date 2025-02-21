from tilecloud import Tile, TileCoord, TileStore


class BSDDBTileStore(TileStore):

    def __init__(self, db, **kwargs):
        self.db = db
        TileStore.__init__(self, **kwargs)

    def __contains__(self, tile):
        return tile and str(tile.tilecoord) in self.db

    def __len__(self):
        return len(self.db)

    def delete_one(self, tile):
        key = str(tile.tilecoord).encode('utf-8')
        if key in self.db:
            del self.db[key]
        return tile

    def get_all(self):
        for key, data in self.db.items():
            tile = Tile(TileCoord.from_string(key), content_type=self.content_type, data=data)
            yield tile

    def get_one(self, tile):
        try:
            tile.content_type = self.content_type
            tile.data = self.db[str(tile.tilecoord).encode('utf-8')]
            return tile
        except KeyError:
            return None

    def list(self):
        return map(lambda s: Tile(TileCoord.from_string(s)), self.db.keys())

    def put_one(self, tile):
        self.db[str(tile.tilecoord).encode('utf-8')] = getattr(tile, 'data', '')
        return tile
