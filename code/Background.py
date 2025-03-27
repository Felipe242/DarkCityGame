from code.Entity import Entity
from code.const import WIN_WIDTH, Entity_SPEED


class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self):
        self.rect.centerx -= Entity_SPEED[self.name] * 0.5
        if self.rect.right <= -0:
            self.rect.left = WIN_WIDTH
