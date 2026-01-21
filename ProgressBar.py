import shutil
import sys

class ProgressBar:
    def __init__(self, total_steps, retro=False):
        self.total_steps = max(1, total_steps)
        self.current = 0
        if retro:
            self.sign = "#"
        else:
            self.sign = "█"

    def update(self, steps=1):
        self.current += steps
        if self.current > self.total_steps:
            self.current = self.total_steps
        self._render()

    def _render(self):
        # Get terminal width
        width = shutil.get_terminal_size((80, 20)).columns

        # Reserve space for brackets, spaces, and percentage
        percent = self.current / self.total_steps
        pct_text = f"{int(percent * 100):3d}%"
        bar_width = max(10, width - len(pct_text) - 5)

        filled = int(bar_width * percent)
        bar = self.sign * filled + " " * (bar_width - filled)

        sys.stdout.write(f"\r[{bar}] {pct_text}")
        sys.stdout.flush()

        if self.current == self.total_steps:
            sys.stdout.write("\n")
            sys.stdout.flush()



