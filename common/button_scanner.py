from events.input import BUTTON_TYPES, Buttons


class ButtonScanner:
    """Scan they buttons."""

    def __init__(self, app, config):
        """Construct."""
        self.button_states = Buttons(app)
        self.config = config
        self.config["CANCEL"] = {"method": app.minimise}

    def scan(self):
        """Scan."""
        for button, action in self.config.items():
            if self.button_states.get(BUTTON_TYPES[button]):
                self.button_states.clear()
                if "args" in action:
                    action["method"](*action["args"])
                else:
                    action["method"]()
