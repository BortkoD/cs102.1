import abc
import curses
import pygame
from pygame.locals import *

from life import GameOfLife


class UI(abc.ABC):
    def __init__(self, life: GameOfLife) -> None:
        self.life = life

    @abc.abstractmethod
    def run(self) -> None:
        pass