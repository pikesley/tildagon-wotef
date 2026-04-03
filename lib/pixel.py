from .conf import conf


class Pixel:
    """A rectangle."""

    def __init__(self, encoded):
        """Construct."""
        self.left = encoded[0]
        self.width = encoded[1]
        self.top = encoded[2]

        self.height = conf["scale"]
        self.colour = conf["fighter-colour"] + [1]

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
