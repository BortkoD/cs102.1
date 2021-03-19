import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.box()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        grid = self.life.curr_generation
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                if grid[y][x] == 1:
                    screen.addch(y, x, '~')
                else:
                    screen.addch(y, x, ' ')

    def run(self) -> None:
        curses.initscr()
        win = curses.newwin(self.life.rows, self.life.cols, 0, 0)
        # PUT YOUR CODE HERE
        running = True
        while running:
            self.draw_borders(win)
#            self.draw_grid(screen)
            self.life.step()
            win.clear()
            win.refresh()
        curses.endwin()


if __name__ == "__main__":
    gol = GameOfLife((240, 120))
    ui = Console(gol)
    ui.run()