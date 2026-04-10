import os

if "Tildagon" in os.uname().machine:
    from .conf import rainbow, render_config


max_y, min_y = render_config["max-y"], render_config["min-y"]
scale = render_config["scale"]
index_mappings = rainbow["index-mappings"]


class Pixel:
    """A rectangle."""

    pix_rainbow = rainbow["rainbow"]

    def __init__(self, encoded, coloured=False):
        """Construct."""
        self.left = encoded[0]
        self.width = encoded[1]
        self.top = encoded[2]

        self.height = scale
        if coloured:
            self.colour = Pixel.pix_rainbow[index_mappings.index(self.top)]

        else:
            self.colour = [0, 0, 0, 1]

    def draw(self, ctx):
        """Draw."""
        ctx.rgba(*self.colour)

        ctx.rectangle(
            self.left,
            self.top,
            self.width,
            self.height,
        )

        ctx.fill()
