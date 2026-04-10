import gc

from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable

import app

from .common.led_lighter import LEDLighter
from .common.rotation_monitor import RotationMonitor
from .lib.background import Background, BlackBackground
from .lib.conf import conf
from .lib.fighter import Fighter
from .lib.pixel import Pixel


class Wotef(app.App):
    """Wotef."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        self.button_states = Buttons(self)
        self.hue = 1.0
        self.leds = LEDLighter(0.5)  # TODO isolate this
        self.rotation_monitor = RotationMonitor()
        self.mode = conf["start-mode"]
        self.fighter = Fighter(self.mode)

    def update(self, _):
        """Update."""
        self.hue += conf["hue-increment"]
        self.scan_buttons()

        self.fighter.animate()

        if self.fighter.done:
            gc.collect()
            self.fighter.new_move()

        if self.mode == "rainbow":
            for _ in range(conf["rainbow-rotation-rate"]):
                Pixel.pix_rainbow = [Pixel.pix_rainbow[-1]] + Pixel.pix_rainbow[:-1]
            self.leds.light_rgb(Pixel.pix_rainbow[(int(len(Pixel.pix_rainbow) / 2))])

        else:
            self.leds.light(self.hue)

    def update_mode(self, mode):
        """Set mode."""
        self.mode = mode
        self.fighter.mode = mode
        # TODO update light pattern

    def draw(self, ctx):
        """Draw."""
        ctx.rotate(self.rotation_monitor.read())
        self.overlays = []

        if self.mode == "rainbow":
            self.overlays.append(BlackBackground())
        else:
            self.overlays.append(Background(self.hue))

        self.overlays.extend(self.fighter.next)
        self.draw_overlays(ctx)

    def scan_buttons(self):
        """Buttons."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

        if self.button_states.get(BUTTON_TYPES["UP"]):
            self.button_states.clear()
            self.update_mode("rainbow")

        if self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.button_states.clear()
            self.update_mode("plain")


__app_export__ = Wotef
