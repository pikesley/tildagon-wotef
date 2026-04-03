import gc

from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable

import app

from .common.colour_tools import rgb_from_hue
from .common.led_lighter import LEDLighter
from .lib.background import Background
from .lib.conf import conf
from .lib.fighter import Fighter

moves = list(conf["moves"].keys())


class Wotef(app.App):
    """Wotef."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        self.button_states = Buttons(self)
        self.hue = 1.0
        self.fighter = Fighter("roundhouse", hue=self.hue)
        self.leds = LEDLighter(0.5)

    def update(self, _):
        """Update."""
        # if not self.fighter:
        #     self.fighter = Fighter(choice(moves), hue=self.hue)
        self.hue += conf["hue-increment"]
        self.scan_buttons()
        self.leds.light(self.hue)

        if self.fighter:
            self.fighter.animate()
            gc.collect()

        # if self.fighter.done:
        #     self.fighter = None
        #     gc.collect()

        # gc.collect()

    def draw(self, ctx):
        """Draw."""
        self.overlays = []
        self.overlays.append(Background(colour=rgb_from_hue(self.hue)))

        if self.fighter:
            self.overlays.extend(self.fighter.next)
            self.draw_overlays(ctx)

    def scan_buttons(self):
        """Buttons."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()


__app_export__ = Wotef
