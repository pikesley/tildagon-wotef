import os
from pathlib import Path


class PushManager:
    """Manage pushing."""

    def __init__(self, app, app_root=".", includes="includes"):
        """Construct."""
        self.app = app
        self.app_root = Path(app_root)

        self.includes = (
            Path(app_root, includes).read_text(encoding="utf-8").strip().split("\n")
        )

        self.files = sorted(
            [entry for entry in self.includes if Path(self.app_root, entry).is_file()]
        )
        self.dirs = sorted(
            [entry for entry in self.includes if Path(self.app_root, entry).is_dir()]
        )

        self.mkdir_commands = [f"python -m mpremote fs mkdir :/apps/{app}"]
        self.cp_dir_commands = [
            f"python -m mpremote fs cp -r {directory} :/apps/{self.app}/"
            for directory in self.dirs
        ]
        self.cp_file_commands = [
            f"python -m mpremote fs cp {entry} :/apps/{app}/" for entry in self.files
        ]

    def push(self):
        """Push."""
        commands = self.mkdir_commands + self.cp_dir_commands + self.cp_file_commands
        for command in commands:
            print(command)
            os.system(command)  # noqa: S605


if __name__ == "__main__":
    import sys

    includes = "includes"
    if len(sys.argv) > 1:
        includes = sys.argv[1]

    inc = Path(includes)
    if not inc.exists():
        print(f"`{includes}` needs to exist")
        sys.exit(1)

    if Path("includes").stat().st_size == 0:
        print(f"`{includes}` needs be populated")
        sys.exit(1)

    app = Path(__file__).parent.parent.stem
    pm = PushManager(app, includes=includes)
    pm.push()

# TODO generate release-exlcudes from "includes"
