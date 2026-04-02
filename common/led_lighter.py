from tildagonos import tildagonos

from .colour_tools import rgb_from_hue
from .gamma import gamma_corrections


class LEDLighter:
    """Light some LEDs."""

    def __init__(self, brightness):
        """Construct."""
        self.brightness = brightness

    def light(self, hue, secondary_hue=None):
        """Light lights."""
        colour = rgb_from_hue(hue)
        for i in range(18):
            if secondary_hue and i > 11:
                colour = rgb_from_hue(secondary_hue)
            tildagonos.leds[i + 1] = [
                gamma_corrections[int(i * 255 * self.brightness)] for i in colour
            ]

        tildagonos.leds.write()
