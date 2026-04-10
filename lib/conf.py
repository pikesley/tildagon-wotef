import gzip
import json

from .asset_path import ASSET_PATH

with open(ASSET_PATH + "conf.json") as j:
    conf = json.loads(j.read())

filepath = ASSET_PATH + "data/config.json.gz"
render_config = json.loads(gzip.decompress(open(filepath, "rb").read()).decode())
scale = render_config["scale"]

filepath = ASSET_PATH + "data/rainbow.json.gz"
rainbow = json.loads(gzip.decompress(open(filepath, "rb").read()).decode())
