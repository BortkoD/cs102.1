import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife, speed = 1) -> None:
        super().__init__(life)
        self.life.curr_generation = self.life.create_grid(True)
        self.speed = speed

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        curses.resizeterm(self.life.rows + 2, self.life.cols + 2)
        screen.border()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                if self.life.curr_generation[y][x] == 1:
                    screen.addstr(y+1, x+1, '*')
                else:
                    screen.addstr(y+1, x+1, ' ')

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)
        curses.curs_set(0)
        screen.refresh()
        # PUT YOUR CODE HERE
        running = True
        while running:
            screen.clear()
            self.life.step()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(self.speed)
        curses.endwin()


if __name__ == "__main__":
    gol = GameOfLife((50, 50))
    ui = Console(gol)
    ui.run()