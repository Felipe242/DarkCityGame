import sys
from datetime import datetime
import pygame
from pygame.font import Font
from pygame.surface import Surface
from pygame import Rect, KEYDOWN, K_RETURN, K_BACKSPACE, K_ESCAPE

from code.DBProxy import DBProxy
from code.const import C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE, C_DARK, C_GREEN


class Score:
    def __init__(self, window: Surface):
        self.window = window

        # Tenta carregar a imagem corretamente
        try:
            self.surf = pygame.image.load('./assets/ScoreBg.png').convert()
        except pygame.error as e:
            print(f"Erro ao carregar a imagem: {e}")
            self.surf = pygame.Surface((800, 600))  # Se der erro, cria uma superfície vazia

        self.rect = self.surf.get_rect(left=0, top=0)

    def save(self, game_mode: str, player_score: list[int]):
        pygame.mixer.music.load('./assets/Score.wav')
        pygame.mixer.music.play(0)
        db_proxy = DBProxy('DBScore')
        name = ''

        while True:
            self.window.blit(self.surf, self.rect)  # Primeiro desenha o fundo
            self.score_text(48, 'Game Over!', C_DARK, SCORE_POS['Title'])

            if game_mode == MENU_OPTION[0]:
                score = player_score[0]
                text = 'Enter Player 1 name (4 characters):'
            elif game_mode == MENU_OPTION[1]:
                score = (player_score[0] + player_score[1]) / 2
                text = 'Enter Team name (4 characters):'
            elif game_mode == MENU_OPTION[2]:
                score = player_score[1]
                text = 'Enter Player 1 name (4 characters):'

            self.score_text(20, text, C_DARK, SCORE_POS['EnterName'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and len(name) == 4:
                        db_proxy.save({'name': name, 'score': score, 'date': get_formatted_date()})
                        return self.show()
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 4:
                        name += event.unicode

            self.score_text(20, name, C_DARK, SCORE_POS['Name'])
            pygame.display.flip()

    def show(self):
        pygame.mixer.music.load('./assets/Score.wav')
        pygame.mixer.music.play(0)

        self.window.blit(self.surf, self.rect)  # Garante que o fundo seja desenhado corretamente
        self.score_text(48, 'TOP 10 SCORE', C_DARK, SCORE_POS['Title'])
        self.score_text(20, 'NAME     SCORE           DATE      ', C_DARK, SCORE_POS['Label'])

        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for index, player_score in enumerate(list_score):
            _, name, score, date = player_score
            self.score_text(20, f'{name}     {score:05d}     {date}', C_YELLOW, SCORE_POS[index])

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    return

    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)


def get_formatted_date():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M")
    current_date = current_datetime.strftime("%d/%m/%y")
    return f"{current_time} - {current_date}"
