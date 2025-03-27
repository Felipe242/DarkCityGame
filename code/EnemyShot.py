from code.Entity import Entity
from code.const import Entity_SPEED


class EnemyShot(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)


    def move(self, ):
        self.rect.centerx -= Entity_SPEED[self.name]