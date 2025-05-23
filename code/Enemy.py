from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.const import Entity_SPEED, WIN_WIDTH, ENTITY_SHOT_DELAY

class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self):
        self.rect.centerx -= Entity_SPEED[self.name]  # Move o inimigo

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))  # Cria o tiro do inimigo


