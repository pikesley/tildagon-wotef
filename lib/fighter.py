import json
import os

from .asset_path import ASSET_PATH
from .conf import conf
from .pixel import Pixel


class Fighter:
    """A fighter."""

    def __init__(self, move="roundhouse", hue=1.0):
        """Construct."""
        self.width = 130
        self.height = 131

        self.x = 0
        self.y = 0
        self.scale = 1.5
        self.hue = hue

        self.move = move

        self.frame_indeces = conf["moves"][move]["order"]
        self.intervals = conf["moves"][move]["intervals"]

        self.step_counter = 0
        self.frames_shown = 0

        self.load_frames(self.move)
        self.populate()

    def load_frames(self, move):
        """Load frames."""
        self.frames = []
        filepath = ASSET_PATH + "rle/" + move

        files = os.listdir(filepath)  # noqa: PTH208
        for file in sorted(files):
            self.frames.append(json.loads(open(filepath + "/" + file).read()))  # noqa: PTH123, SIM115

        self.width = sum([x[1] for x in self.frames[0][0]])
        self.height = len(self.frames[0])

    @property
    def done(self):
        """Are we done."""
        return self.frames_shown > len(self.frame_indeces)

    @property
    def next(self):
        """Next frame."""
        self.frames_shown += 1
        return self.screens[self.frame_indeces[0]]

    def animate(self):
        """Animate."""
        if self.step_counter > self.intervals[0]:
            self.frame_indeces = self.frame_indeces[1:] + [self.frame_indeces[0]]
            self.intervals = self.intervals[1:] + [self.intervals[0]]
            self.step_counter = 0
        else:
            self.step_counter += 1

    def populate(self):
        """Pre-render pixels."""
        self.screens = [self.pixels(frame) for frame in self.frames]

    def pixels(self, frame):
        """Draw."""
        pix = []
        start_x = self.x - (self.width * self.scale / 2)
        start_y = self.y - (self.height * self.scale / 2)
        colour = (0, 0, 0)
        # colour = rgb_from_hue(self.hue)
        for i, row in enumerate(frame):
            counter = 0
            for item in row:
                opacity = 1
                if item[0] == "0":
                    opacity = 0
                pix.append(
                    Pixel(
                        start_x + (counter * self.scale),
                        start_y + (i * self.scale),
                        self.scale * item[1],
                        self.scale,
                        colour,
                        opacity,
                    )
                )
                counter += item[1]

        return pix
