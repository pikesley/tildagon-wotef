import gzip
import json
import os
from random import choice

if "Tildagon" in os.uname().machine:
    from .asset_path import ASSET_PATH
    from .expand_frameset import expand_frameset
    from .pixel import Pixel

else:
    from lib.expand_frameset import expand_frameset
    from lib.pixel import Pixel

    ASSET_PATH = "tests/fixtures/"


class Fighter:
    """A fighter."""

    def __init__(self, mode):
        """Construct."""
        self.load_frames()
        self.load_framesets()
        self.mode = mode

        self.new_move()

    def load_frames(self):
        """Load frames."""
        filepath = ASSET_PATH + "data/frames.json.gz"
        self.frames = json.loads(gzip.decompress(open(filepath, "rb").read()).decode())

    def load_framesets(self):
        """Load frames."""
        filepath = ASSET_PATH + "data/framesets.json.gz"
        self.framesets = json.loads(
            gzip.decompress(open(filepath, "rb").read()).decode()
        )
        self.moves = list(self.framesets.keys())

    @property
    def done(self):
        """Are we done."""
        return self.frames_shown > len(self.frameset)

    @property
    def next(self):
        """Next frame."""
        return self.screen

    def new_move(self):
        """New move."""
        self.move = choice(self.moves)
        self.frameset = expand_frameset(self.framesets[self.move])
        self.frames_shown = 0

    def animate(self):
        """Animate."""
        self.screen = [
            Pixel(item, coloured=self.mode == "rainbow")
            for item in self.frames[self.frameset[0]]
        ]
        self.frameset = self.frameset[1:] + [self.frameset[0]]
        self.frames_shown += 1
