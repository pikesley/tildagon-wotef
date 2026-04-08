import shutil
from pathlib import Path

import yaml

root = "data"

app_conf = yaml.safe_load(Path("conf.yaml").read_text(encoding="utf-8"))


def clean():
    """Scrub before we start."""
    shutil.rmtree(root)
    Path(root).mkdir(exist_ok=True)
