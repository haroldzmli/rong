import json
from utils import geobuf

f = open('/work/pyproj/pygeobuf-master/test/fixtures/test.json', 'r')
content = f.read()
a = json.loads(content)

pbf = geobuf.encode(a) # GeoJSON or TopoJSON -> Geobuf string
my_json = geobuf.decode(pbf) # Geobuf string -> GeoJSON or TopoJSON
