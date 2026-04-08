import gc
from random import choice

from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable

import app

from .common.led_lighter import LEDLighter
from .common.rotation_monitor import RotationMonitor
from .lib.background import Background
from .lib.conf import conf
from .lib.fighter import Fighter


class Wotef(app.App):
    """Wotef."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        self.moves = list(conf["moves"].keys())
        self.button_states = Buttons(self)
        self.hue = 1.0
        self.leds = LEDLighter(0.5)
        self.rotation_monitor = RotationMonitor()
        self.fighter = Fighter()
        self.next_move()

    def next_move(self):
        """Get next move."""
        self.fighter.populate(choice(self.moves))

    def update(self, _):
        """Update."""
        self.hue += conf["hue-increment"]
        self.scan_buttons()
        self.leds.light(self.hue)

        self.fighter.animate()

        if self.fighter.done:
            gc.collect()
            self.next_move()

    def draw(self, ctx):
        """Draw."""
        ctx.rotate(self.rotation_monitor.read())
        self.overlays = []
        self.overlays.append(Background(self.hue))

        self.overlays.extend(self.fighter.next)
        self.draw_overlays(ctx)

    def scan_buttons(self):
        """Buttons."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()


__app_export__ = Wotef
