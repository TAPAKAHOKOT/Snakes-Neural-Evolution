from random import randint as rnd, choice as chs


class Apple:
    def __init__(self, settings, snakes, draw_fun):
        self.settings = settings
        self.draw_fun = draw_fun

        self.width_size = len(self.settings.cells_st)
        self.height_size = len(self.settings.cells_st[0])

        self.color = (255, 50, 50)

        self.x_pos = 0
        self.y_pos = 0

        while not self.x_pos and not self.y_pos:
            self.x_pos = rnd(2, self.width_size - 3)
            self.y_pos = rnd(2, self.height_size - 3)

            for snake in snakes:
                if (self.x_pos, self.y_pos) in zip(snake.x_pos, snake.y_pos):
                    self.x_pos = 0
                    self.y_pos = 0
                    break
    
    def draw(self):
        self.draw_fun((self.x_pos, self.y_pos), self.color, self.settings, conv=True, apple=True)

