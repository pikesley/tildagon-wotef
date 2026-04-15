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

        self.contact = 0

        self.new_move()

    def load_frames(self):
        """Load frames."""
        filepath = ASSET_PATH + "frames.json.gz"
        self.frames = json.loads(gzip.decompress(open(filepath, "rb").read()).decode())

    def load_framesets(self):
        """Load frames."""
        filepath = ASSET_PATH + "framesets.json.gz"
        self.framesets = json.loads(
            gzip.decompress(open(filepath, "rb").read()).decode()
        )
        self.moves = list(self.framesets.keys())

    @property
    def done(self):
        """Are we done."""
        return self.index == len(self.frameset)

    @property
    def next(self):
        """Next frame."""
        return self.screen

    def new_move(self, move=None):
        """New move."""
        self.move = move if move else choice(self.moves)
        self.frameset = expand_frameset(self.framesets[self.move]["frames"])
        self.index = 0

    def animate(self):
        """Animate."""
        self.screen = [
            Pixel(item, coloured=self.mode == "rainbow")
            for item in self.frames[self.frameset[self.index]]
        ]

        self.contact = False
        if self.index == self.framesets[self.move]["impact-frame"]:
            self.contact = True

        self.index += 1
