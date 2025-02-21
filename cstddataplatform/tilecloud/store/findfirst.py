from tilecloud import TileStore


class FindFirstTileStore(TileStore):

    def __init__(self, tilestores, **kwargs):
        TileStore.__init__(self, **kwargs)
        self.tilestores = tilestores

    def get_one(self, tile):
        return next(filter(
            None,
            (store.get_one(tile) for store in self.tilestores)
        ), None)
