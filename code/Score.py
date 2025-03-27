import pygame


class Score:

    def __int__(self, window):
        self.window = window
        self.surf = pygame.image.load('./assets/Menu.png')
        self.rect = self.surf.get_rect(left=0, top=0)
        pass


    def save_score(self):
        pass


    def show_score(self):
        pass