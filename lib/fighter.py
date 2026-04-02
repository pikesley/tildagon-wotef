import json
import os

from .asset_path import ASSET_PATH
from .pixel import Pixel

intervals = {"roundhouse": [3, 1, 1, 2, 2, 5, 1, 2]}


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

        self.frame_index = 0

        self.step_counter = 0

        self.load_frames(self.move)
        self.populate()

    def load_frames(self, move):
        """Load frames."""
        self.frames = []
        filepath = ASSET_PATH + "rle/" + move

        files = os.listdir(filepath)
        for file in sorted(files):
            self.frames.append(json.loads(open(filepath + "/" + file).read()))

        self.width = sum([x[1] for x in self.frames[0][0]])
        self.height = len(self.frames[0])

    def animate(self):
        """Animate."""
        if self.step_counter > intervals[self.move][self.frame_index]:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
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
