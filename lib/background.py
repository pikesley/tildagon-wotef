from ..common.colour_tools import rgb_from_hue


class Background:
    """Background."""

    def __init__(self, hue, opacity=1):
        """Construct."""
        colour = rgb_from_hue(hue)
        self.bottom_colour = [int(i * 255) for i in colour]
        self.top_colour = [int(i * 127) for i in colour]
        self.opacity = opacity

    def draw(self, ctx):
        """Draw ourself."""
        ctx.linear_gradient(0, -120, 0, 120)

        ctx.add_stop(0.0, self.top_colour, self.opacity)
        ctx.add_stop(1.0, self.bottom_colour, self.opacity)

        ctx.rectangle(-120, -120, 240, 240)
        ctx.fill()


class BlackBackground:
    """Background."""

    def draw(self, ctx):
        """Draw."""
        ctx.rgba(0, 0, 0, 1)
        ctx.rectangle(-120, -120, 240, 240)
        ctx.fill()
