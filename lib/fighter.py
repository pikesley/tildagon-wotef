import gzip
import json

from .asset_path import ASSET_PATH
from .pixel import Pixel


class Fighter:
    """A fighter."""

    def __init__(self):
        """Construct."""
        self.load_frames()
        self.load_framesets()

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

    def reset(self):
        """Reset."""
        self.frames_shown = 0

    @property
    def done(self):
        """Are we done."""
        return self.frames_shown > len(self.screens)

    @property
    def next(self):
        """Next frame."""
        return self.screens[0]

    def animate(self):
        """Animate."""
        if self.step_counter > self.intervals[0]:
            self.screens = self.screens[1:] + [self.screens[0]]
            self.intervals = self.intervals[1:] + [self.intervals[0]]
            self.frames_shown += 1
            self.step_counter = 0
        else:
            self.step_counter += 1

    def populate(self, move):
        """Pre-render pixels."""
        frameset = self.framesets[move]
        self.screens = [self.pixels(self.frames[frame[0]]) for frame in frameset]
        self.intervals = [frame[1] for frame in frameset]
        self.step_counter = 0
        self.frames_shown = 0

    def pixels(self, frame):
        """Draw."""
        return [Pixel(item) for item in frame]
