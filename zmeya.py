from random import randint as rnd
from random import choice as chs

from copy import deepcopy


class Snake:
    def __init__(self, settings, draw_fun, draw_crown):
        self.settings = settings
        self.draw_fun = draw_fun
        self.draw_crown = draw_crown

        self.score = 0

        self.width_size = len(self.settings.cells_st)
        self.height_size = len(self.settings.cells_st[0])

        self.x_pos = [rnd(0, self.width_size - 1)]
        self.y_pos = [rnd(0, self.height_size - 1)]

        rn_speed = rnd(-1, 1)
        self.speed = [rn_speed, chs([-1, 1]) if rn_speed == 0 else 0]

        self.settings.dead_cells.append([self.x_pos[0], self.y_pos[0]])
        self.to_move = ["W", "N", "E", "S"]

        self.last_side = "N"

        self.color = chs(self.settings.colors)
        self.head_color = tuple([ k + k // 10 - (k + k // 10) % 255 for k in self.color])

        self.e_s = 20
        self.min_e_s = -30
        self.max_e_s = 30
        if (self.settings.use_old_data):
            ind = rnd(0, 100)
            koefs = [50, 75, 90, 101]
            for k, i in enumerate(koefs):
                if (ind < i):
                    ind = k
                    break

            self.arr_app = deepcopy(self.settings.best_app[ind])
            self.arr_block = deepcopy(self.settings.best_block[ind])
        elif(self.settings.random_koefs):
            self.arr_app = [[rnd(self.min_e_s, self.max_e_s) for k in range(self.e_s)] for k in range(self.e_s)]
            self.arr_block = [[rnd(self.min_e_s, self.max_e_s) for k in range(self.e_s)] for k in range(self.e_s)]
        else:
            self.arr_app = [
                [0, 1, 1, 1, 1, 1, 0],
                [1, 1, 2, 3, 2, 1, 1],
                [1, 2, 6, 8, 6, 2, 1],
                [1, 3, 8, 0, 8, 3, 1],
                [1, 2, 6, 8, 6, 2, 1],
                [1, 1, 2, 3, 2, 1, 1],
                [0, 1, 1, 1, 1, 1, 0]
            ]

            self.arr_block = [
                [-2, -2, -2, -2, -2, -2, -2],
                [-2, -2, -3, -4, -3, -2, -2],
                [-2, -3, -10, -20, -10, -3, -2],
                [-2, -4, -20, 0, -20, -4, -2],
                [-2, -3, -10, -20, -10, -3, -2],
                [-2, -2, -3, -4, -3, -2, -2],
                [-2, -2, -2, -2, -2, -2, -2]
            ]



    def draw(self):
        for k in range(len(self.x_pos)):
            if k == 0:
                col = self.head_color
            else:
                col = []
                for i in self.color:
                    i = int(i + (40 * (k / len(self.x_pos)) ))
                    i = i if i < 255 else 255
                    col.append(i)

                col = tuple(col)
            # col = self.head_color if k == 0 else self.color
            self.draw_fun((self.x_pos[k], self.y_pos[k]), col, self.settings, conv=True)

        if (self.score == self.settings.max_score):
            self.draw_crown((self.x_pos[0], self.y_pos[0]), self.settings, conv=True)


    def update(self, snakes, this_snake):
        # try:
        #     self.settings.dead_cells.remove(
        #         [self.x_pos[-1], self.y_pos[-1]])
        # except:
        #     pass

        for k in range(1, len(self.x_pos)):
            self.x_pos[-k] = self.x_pos[-k - 1]
            self.y_pos[-k] = self.y_pos[-k - 1]

        self.x_pos[0] += self.speed[0]
        self.y_pos[0] += self.speed[1]

        # self.settings.dead_cells.append([self.x_pos[0], self.y_pos[0]])

        return self.check_lose(snakes, this_snake)
        # return False

    def inc_tail(self):
        self.x_pos.append(self.x_pos[-1])
        self.y_pos.append(self.y_pos[-1])

        self.score += 1
        # print("Score is >>> ", self.score)

    def change_direct(self, side):
        if side == "N" and self.speed != [0, 1]:
            self.speed = [0, -1]
        elif side == "S" and self.speed != [0, -1]:
            self.speed = [0, 1]
        elif side == "E" and self.speed != [-1, 0]:
            self.speed = [1, 0]
        elif side == "W" and self.speed != [1, 0]:
            self.speed = [-1, 0]

    def check_lose(self, snakes, this_snake):
        if not (0 < self.x_pos[0] < self.settings.cells_num[0] and 0 < self.y_pos[0] < self.settings.cells_num[1]):
            return True

        for snake in snakes:
            if snake != this_snake:
                if (self.x_pos[0], self.y_pos[0]) in zip(snake.x_pos, snake.y_pos):
                    return True
            else:
                if (self.x_pos[0], self.y_pos[0]) in zip(snake.x_pos[1:], snake.y_pos[1:]):
                    return True
        return False

    def check_apple_eating(self, apple):

        if [self.x_pos[0], self.y_pos[0]] == [apple.x_pos, apple.y_pos]:
            return True
        return False


    def mutation(self):
        x, y = (rnd(0, self.e_s-1), rnd(0, self.e_s-1))
        ind = rnd(0, 1)

        if (rnd(0, 1) == 0):
            if ind == 0:
                self.arr_app[y][x] = rnd(self.min_e_s, self.max_e_s)
            else:
                self.arr_block[y][x] = rnd(self.min_e_s, self.max_e_s)

    def get_side(self, x, y):
        sides = []
        if (self.x_pos[0] - x > 0):
            sides.append(0)
        if (self.x_pos[0] - x < 0):
            sides.append(2)
        if (self.y_pos[0] - y > 0):
            sides.append(1)
        if (self.y_pos[0] - y < 0):
            sides.append(3)

        return sides
    def brain(self, apples, snakes):

        # self.arr_app = [
        #     [0, 1, 1, 1, 1, 1, 0],
        #     [1, 1, 2, 3, 2, 1, 1],
        #     [1, 2, 6, 8, 6, 2, 1],
        #     [1, 3, 8, 0, 8, 3, 1],
        #     [1, 2, 6, 8, 6, 2, 1],
        #     [1, 1, 2, 3, 2, 1, 1],
        #     [0, 1, 1, 1, 1, 1, 0]
        # ]

        # self.arr_block = [
        #     [-2, -2, -2, -2, -2, -2, -2],
        #     [-2, -2, -3, -4, -3, -2, -2],
        #     [-2, -3, -10, -20, -10, -3, -2],
        #     [-2, -4, -20, 0, -20, -4, -2],
        #     [-2, -3, -10, -20, -10, -3, -2],
        #     [-2, -2, -3, -4, -3, -2, -2],
        #     [-2, -2, -2, -2, -2, -2, -2]
        # ]


        weights_sum = [0, 0, 0, 0]

        for apple in apples:
            x, y = apple.x_pos, apple.y_pos
            
            if (abs(self.x_pos[0] - x) < self.e_s//2 and abs(self.y_pos[0] - y) < self.e_s//2):
                sides = self.get_side(x, y)

                x = x - self.x_pos[0] + self.e_s // 2
                y = y - self.y_pos[0] + self.e_s // 2

                for k in sides:
                    weights_sum[k] += self.arr_app[y][x]

        for snake in snakes:
           
            for k in range(len(snake.x_pos)):
                x, y = snake.x_pos[k], snake.y_pos[k]

                if (abs(self.x_pos[0] - x) < self.e_s//2 and abs(self.y_pos[0] - y) < self.e_s//2):
                    sides = self.get_side(x, y)

                    x = x - self.x_pos[0] + self.e_s // 2
                    y = y - self.y_pos[0] + self.e_s // 2

                    for k in sides:
                        weights_sum[k] += self.arr_block[y][x]
        # print(self.x_pos[0], self.y_pos[0])
        # print(self.settings.cells_num)
        if (self.y_pos[0] < self.e_s // 2):
            for k in range(int(self.e_s // 2 - self.y_pos[0])):
                weights_sum[1] += sum(self.arr_block[k])
        elif (self.settings.cells_num[1] - self.y_pos[0] < self.e_s // 2):
            for k in range(int(self.e_s // 2 - self.settings.cells_num[1] + self.y_pos[0])):
                weights_sum[3] += sum(self.arr_block[k])

        if (self.x_pos[0] < self.e_s // 2):
            for k in range(int(self.e_s // 2 - self.x_pos[0])):
                weights_sum[0] += sum(self.arr_block[k])
        elif (self.settings.cells_num[0] - self.x_pos[0] < self.e_s // 2):
            for k in range(int(self.e_s // 2 - self.settings.cells_num[0] + self.x_pos[0])):
                weights_sum[2] += sum(self.arr_block[k])


        # print(weights_sum)
        inds = []

        # print("ls = ", self.last_side)
        if weights_sum.count(max(weights_sum)) > 1:
            for k in range(4):
                if weights_sum[k] == max(weights_sum):
                    inds.append(k)

            side = self.to_move[chs(inds)]
        else:
            side = self.to_move[weights_sum.index(max(weights_sum))]

        if side == "N" and self.speed == [0, 1]:
            weights_sum[weights_sum.index(max(weights_sum))] -= 100
            side = self.to_move[weights_sum.index(max(weights_sum))]
        elif side == "S" and self.speed == [0, -1]:
            weights_sum[weights_sum.index(max(weights_sum))] -= 100
            side = self.to_move[weights_sum.index(max(weights_sum))]
        elif side == "E" and self.speed == [-1, 0]:
            weights_sum[weights_sum.index(max(weights_sum))] -= 100
            side = self.to_move[weights_sum.index(max(weights_sum))]
        elif side == "W" and self.speed == [1, 0]:
            weights_sum[weights_sum.index(max(weights_sum))] -= 100
            side = self.to_move[weights_sum.index(max(weights_sum))]

        # print(side)

        self.change_direct(side)
