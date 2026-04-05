import gzip
import json

from .asset_path import ASSET_PATH
from .conf import conf
from .pixel import Pixel


class Fighter:
    """A fighter."""

    def __init__(self, move="roundhouse"):
        """Construct."""
        self.x = 0
        self.y = 0
        self.scale = 1.5

        self.move = move

        self.frame_indeces = conf["moves"][move]["order"]
        self.intervals = conf["moves"][move]["intervals"]

        self.step_counter = 0
        self.frames_shown = 0

        self.load_frames(self.move)
        self.populate()

    def load_frames(self, move):
        """Load frames."""
        filepath = ASSET_PATH + "sources/encoded/" + move

        self.frames = json.loads(
            gzip.decompress(open(filepath + ".json.gz", "rb").read()).decode()
        )

    def reset(self):
        """Reset."""
        self.frames_shown = 0

    @property
    def done(self):
        """Are we done."""
        return self.frames_shown > len(self.frame_indeces)

    @property
    def next(self):
        """Next frame."""
        return self.screens[self.frame_indeces[0]]

    def animate(self):
        """Animate."""
        if self.step_counter > self.intervals[0]:
            self.frame_indeces = self.frame_indeces[1:] + [self.frame_indeces[0]]
            self.intervals = self.intervals[1:] + [self.intervals[0]]
            self.frames_shown += 1
            self.step_counter = 0
        else:
            self.step_counter += 1

    def populate(self):
        """Pre-render pixels."""
        self.screens = [self.pixels(frame) for frame in self.frames]

    def pixels(self, frame):
        """Draw."""
        return [Pixel(item) for item in frame]
