import pathlib
import random
import copy
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        grid = [[0] * self.cols for _ in range(self.rows)]
        if randomize:
            for x in range(self.rows):
                for y in range(self.cols):
                    grid[x][y] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        x = cell[0]
        y = cell[1]
        neighbours = []
        delta = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for d in delta:
            if 0 <= x + d[0] < self.rows and 0 <= y + d[1] < self.cols:
                neighbours.append(self.curr_generation[x + d[0]][y + d[1]])
        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        next_grid = copy.deepcopy(self.curr_generation)
        for x in range(self.rows):
            for y in range(self.cols):
                neighbours = self.get_neighbours((x, y))
                count_of_neighbours = 0
                for i in neighbours:
                    if i == 1:
                        count_of_neighbours += 1
                if self.curr_generation[x][y] == 1 and count_of_neighbours != 2 and count_of_neighbours != 3:
                    next_grid[x][y] = 0
                elif self.curr_generation[x][y] == 0 and count_of_neighbours == 3:
                    next_grid[x][y] = 1
        return next_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations <= self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation == self.prev_generation:
            return False
        else:
            return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        file = open(filename, 'r')
        rows = file.read().splitlines()
        curr_generation = []
        for row in range(len(rows)):
            curr_generation.append(list(rows[row]))
        file.close()
        life = GameOfLife((len(rows), len(rows[0])))
        life.curr_generation = curr_generation
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, 'w')
        curr_state = ''
        for row in range(self.rows):
            for col in range(self.cols):
                curr_state += str(self.curr_generation[row][col])
            curr_state += '\n'
            file.write(curr_state)
            curr_state = ''
        file.close()
