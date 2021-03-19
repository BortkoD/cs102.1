import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 20, speed: int = 50) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.rows
        self.height = self.life.cols
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for x in range(self.height):
            for y in range(self.width):
                if self.life.curr_generation[y][x] == 0:
                    pygame.draw.rect(self.screen, pygame.Color("lightskyblue"),
                                     (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color("lightseagreen"),
                                     (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE
        self.life.curr_generation = self.life.create_grid(True)

        running = True
        paused = 0
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = (paused + 1) % 2
                elif event.type == MOUSEBUTTONDOWN:
                    # получить координаты клика, изменить значение соответствующей ячейки матрицы
                    pos = event.pos
                    pos_y, pos_x = pos[0] // self.cell_size, pos[1] // self.cell_size
                    self.life.curr_generation[pos_y][pos_x] = (self.life.curr_generation[pos_y][
                                                                   pos_x] + 1) % 2
                    if self.life.curr_generation[pos_y][pos_x] == 0:
                        pygame.draw.rect(self.screen, pygame.Color("lightskyblue"),
                                         (pos_y * self.cell_size, pos_x * self.cell_size, self.cell_size, self.cell_size))
                    else:
                        pygame.draw.rect(self.screen, pygame.Color("lightseagreen"),
                                         (pos_y * self.cell_size, pos_x * self.cell_size, self.cell_size, self.cell_size))
                    self.draw_lines()
                    pygame.display.flip()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            if paused == 1:
                continue
            elif self.life.is_max_generations_exceeded is False or self.life.is_changing is False:
                running = False
            else:
                self.draw_grid()
                self.draw_lines()
                self.life.step()
                pygame.display.flip()
                clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    gol = GameOfLife((640, 240))
    ui = GUI(gol)
    ui.run()
