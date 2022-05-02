class Mortal:
    def __init__(self, frames: int, dying: bool):
        self.frames = frames
        self.dying = dying
        self.count = 0
        self.dead = False

    def update(self):
        if self.dying:
            self.count += 1
            if self.count >= self.frames:
                self.dead = True



