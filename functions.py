import math
import pygame as pg
import numpy as np 
import os

def sec_to_formated(sec):
    h = int(sec // 3600)
    m = int((sec - h * 3600) // 60)
    sec = int(sec - h * 3600 - m * 60)
    time_mes = "{}:{}:{}".format(h,m,sec)

    return time_mes

def coords_to_pos(coords, settings):
    return [k * settings.cell_size for k in coords]

def draw_crown(pos, settings, conv=False):
    color = (255, 215, 0)
    x, y = coords_to_pos(pos, settings) if conv else pos

    c_s = settings.cell_size

    pg.draw.line(settings.surf, color, (x, y), (x + c_s // 4, y + c_s // 3), 3)
    pg.draw.line(settings.surf, color, (x + c_s // 4, y + c_s // 3), (x + c_s // 2, y + c_s // 5), 3)
    pg.draw.line(settings.surf, color, (x + c_s // 2, y + c_s // 5), (x + 3 * c_s // 4, y + c_s // 3), 3)
    pg.draw.line(settings.surf, color, (x + 3 * c_s // 4, y + c_s // 3), (x + c_s, y), 3)


def draw_cell(pos, color, settings, conv=False, apple=False):
    x, y = coords_to_pos(pos, settings) if conv else pos
    rect = (x, y, settings.cell_size, settings.cell_size)

    pg.draw.rect(settings.surf, color, rect)

    if apple:
        pg.draw.line(settings.surf, (0, 120, 0), (x + settings.cell_size // 3, y - settings.cell_size // 2), 
                                            (x + settings.cell_size // 2, y + settings.cell_size // 3), 2)

        pg.draw.line(settings.surf, (0, 120, 0), (x + settings.cell_size // 2, y + settings.cell_size // 3), 
                                            (x + 2 * settings.cell_size // 3, y - settings.cell_size // 2), 2)


def draw_field(settings, feadBack):

    window_size = settings.window_size
    line_color = (100, 100, 100)
    for k in range(0, window_size[0], settings.cell_size):
        pg.draw.line(settings.surf, line_color, (0, window_size[1] - k), (window_size[0], window_size[1] - k))

        pg.draw.line(settings.surf, line_color, (window_size[0] - k, 0), (window_size[0] - k, window_size[1]))

    if (feadBack):
        arr = [[1 for i in range(math.ceil(window_size[1] / settings.cell_size))] \
                            for k in range(math.ceil(window_size[0] / settings.cell_size))]

        return arr

def save_weights(settings, save_ind):
    np.save("size_" + save_ind, settings.weights_size)
    np.save("app_" + save_ind, settings.best_app)
    np.save("block_" + save_ind, settings.best_block)
    np.save("scores_" + save_ind, settings.best_scores)
    np.save("print_info_" + save_ind, settings.print_info)

def save_cells_info(settings):
    info_arr = [None] * settings.save_cells_num
    for i, save_ind in enumerate([str(k) for k in range(1, settings.save_cells_num + 1)]):
        try:
            info_arr[i] = np.load("print_info_{}.npy".format(save_ind))
        except:
            pass

    return info_arr

def load_weights(settings, save_ind):
    try:
        settings.weights_size = np.load("size_{}.npy".format(save_ind))
        settings.best_app = np.load("app_{}.npy".format(save_ind))
        settings.best_block = np.load("block_{}.npy".format(save_ind))
        settings.best_scores = np.load("scores_{}.npy".format(save_ind))
        settings.print_info = np.load("print_info_{}.npy".format(save_ind))

        return True
    except:
        return False


def string_leveler(line, size):
    line = str(line)
    return (size - len(line)) // 2 * " " + line + (size - (size - len(line)) // 2 - len(line)) * " "

def delete_save(save_ind):
    try:
        os.remove("size_{}.npy".format(save_ind))
        os.remove("app_{}.npy".format(save_ind))
        os.remove("block_{}.npy".format(save_ind))
        os.remove("scores_{}.npy".format(save_ind))
        os.remove("print_info_{}.npy".format(save_ind))
        return True
    except:
        return False