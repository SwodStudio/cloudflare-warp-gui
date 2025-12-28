import customtkinter as ctk


class ToggleSwitch(ctk.CTkCanvas):
    def __init__(self, master, width=100, height=50, command=None, **kwargs):
        super().__init__(
            master,
            width=width,
            height=height,
            bg="white",
            highlightthickness=0,
            **kwargs,
        )
        self.command = command
        self.on = False
        self.width = width
        self.height = height
        self.radius = height // 2
        self.bg_off = "#D3D3D3"
        self.bg_on = "#FF5B2E"
        self.circle = None
        self.bind("<Button-1>", self.toggle)
        self.draw()

    def draw(self):
        self.delete("all")
        self.create_rounded_rect(
            2,
            2,
            self.width - 2,
            self.height - 2,
            self.radius,
            fill=self.bg_on if self.on else self.bg_off,
        )
        x = self.width - self.height if self.on else 0
        self.circle = self.create_oval(
            x + 4, 4, x + self.height - 4, self.height - 4, fill="white", outline=""
        )

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def toggle(self, event=None):
        new_state = not self.on
        self.on = new_state
        self.animate_toggle(new_state)
        if self.command:
            self.command(new_state)

    def animate_toggle(self, state):
        start = self.width - self.height if not state else 0
        end = self.width - self.height if state else 0
        step = 4 if end > start else -4

        def move():
            nonlocal start
            if (step > 0 and start < end) or (step < 0 and start > end):
                start += step
                self.delete("all")
                self.create_rounded_rect(
                    2,
                    2,
                    self.width - 2,
                    self.height - 2,
                    self.radius,
                    fill=self.bg_on if state else self.bg_off,
                )
                self.circle = self.create_oval(
                    start + 4,
                    4,
                    start + self.height - 4,
                    self.height - 4,
                    fill="white",
                    outline="",
                )
                self.after(10, move)
            else:
                self.draw()

        move()
