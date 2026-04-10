import shutil
from pathlib import Path

import yaml

root = "data"

pre_render_conf = yaml.safe_load(
    Path("tools/pre-render-conf.yaml").read_text(encoding="utf-8")
)


def clean():
    """Scrub before we start."""
    shutil.rmtree(root)
    Path(root).mkdir(exist_ok=True)
