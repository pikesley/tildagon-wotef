import gc

import app

from .common.button_scanner import ButtonScanner
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
        self.hue = 1.0
        self.led_brightnesses = {
            "max": conf["led-brightness"],
            "min": conf["led-brightness"] / 2,
        }
        self.leds = LEDLighter(self.led_brightnesses["min"])  # TODO isolate this
        self.rotation_monitor = RotationMonitor()
        self.buttons = ButtonScanner(
            self,
            {
                "UP": {"method": self.update_mode, "args": ["rainbow"]},
                "DOWN": {"method": self.update_mode, "args": ["plain"]},
            },
        )

        self.mode = conf["start-mode"]
        self.fighter = Fighter(self.mode)

    def update(self, _):
        """Update."""
        self.hue += conf["hue-increment"]
        self.buttons.scan()

        self.fighter.animate()
        self.manage_brightness()

        if self.fighter.done:
            gc.collect()
            self.fighter.new_move()

        if self.mode == "rainbow":
            self.rainbow_lights()
        else:
            self.leds.light(self.hue)

    def update_mode(self, mode):
        """Set mode."""
        self.mode = mode
        self.fighter.mode = mode

    def manage_brightness(self):
        """Manage LED brightness."""
        self.reduce_brightness()
        self.reset_brightness()

    def reduce_brightness(self):
        """Drop the LED brightness."""
        if self.leds.brightness > self.led_brightnesses["min"]:
            self.leds.brightness -= conf["led-decay-rate"]
            self.leds.brightness = max(
                self.leds.brightness, self.led_brightnesses["min"]
            )

    def reset_brightness(self):
        """Reset the LED brightness."""
        if self.fighter.contact:
            self.leds.brightness = self.led_brightnesses["max"]

    def rainbow_lights(self):
        """Rainbow lights."""
        for _ in range(conf["rainbow-rotation-rate"]):
            Pixel.pix_rainbow = [Pixel.pix_rainbow[-1]] + Pixel.pix_rainbow[:-1]
        self.leds.light_rgb(Pixel.pix_rainbow[(int(len(Pixel.pix_rainbow) / 2))])

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


__app_export__ = Wotef
