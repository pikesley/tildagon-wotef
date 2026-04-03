import json
import os

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

        self.step_counter = 0
        self.frames_shown = 0

        self.load_frames(self.move)
        self.populate()

    def load_frames(self, move):
        """Load frames."""
        self.frames = []
        filepath = ASSET_PATH + "encoded/" + move

        files = os.listdir(filepath)  # noqa: PTH208
        for file in sorted(files):
            self.frames.append(json.loads(open(filepath + "/" + file).read()))  # noqa: PTH123, SIM115

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
        self.frame_indeces = self.frame_indeces[1:] + [self.frame_indeces[0]]
        self.frames_shown += 1

    def populate(self):
        """Pre-render pixels."""
        self.screens = [self.pixels(frame) for frame in self.frames]

    def pixels(self, frame):
        """Draw."""
        return [Pixel(item) for item in frame]
