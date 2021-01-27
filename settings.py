
class Settings:
    def __init__(self, surf, size):
        self.surf = surf

        self.file_with_weights = "weights.txt"

        self.window_size = size[:]
        self.population_size = 200

        self.cell_size = 8

        self.cells_st = None
        self.cells_num = [0, 0]

        self.dead_cells = []

        self.manual_control = True

        self.max_score = 0
        self.absolute_max_score = 0

        self.random_koefs = True
        self.use_old_data = False

        self.eaten_apples = [0] * self.population_size

        self.print_info = [0, 0, 0]
        self.weights_size = [15]
        self.best_scores = [0, 0, 0, 0]
        self.best_app = [None, None, None, None]
        self.best_block = [None, None, None, None]

        self.pause = 0
        self.autosave = 0

        self.colors = [
            (220, 20, 60), # RED
            (255, 192, 203),
            (127, 255, 0), # GREEN
            (173, 255, 47),
            (255, 215, 0), # YELLOW
            (240, 230, 140),
            (127, 255, 212), # BLUE
            (0, 206, 209),
            (65, 105, 225),
            (186, 85, 211), # PINK
            (238, 130, 238),
            (255, 105, 180),
            (169, 169, 169), # GRAY
            (119, 136, 153),
            (47, 79, 79)
        ]
