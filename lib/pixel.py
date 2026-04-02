class Pixel:
    """A square."""

    def __init__(self, left, top, width, height, colour, opacity):  # noqa: PLR0913
        """Construct."""
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.colour = list(colour) + [opacity]

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
