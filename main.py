from settings import *
from functions import *
from zmeya import Snake
from apple import Apple
from time import sleep, perf_counter

from random import choice as chs
from random import randint as rnd

from copy import deepcopy
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (10, 10)

FPS = 30
pg.init()

size_x = 800
size_y = 800
screen = pg.display.set_mode((size_x, size_y), flags=pg.DOUBLEBUF | pg.NOFRAME)

surf = pg.Surface((size_x, size_y))
clock = pg.time.Clock()

settings = Settings(surf, (size_x, size_y))
settings.screen = screen

settings.cells_st = draw_field(settings, True)

settings.cells_num = [len(settings.cells_st), len(settings.cells_st[0])]

snakes = [Snake(settings, draw_cell, draw_crown) for k in range(settings.population_size)]
apples = [Apple(settings, snakes, draw_cell)]

for k in range(4):
	settings.best_app[k] = snakes[k].arr_app
	settings.best_block[k] = snakes[k].arr_block

counter = 0
pop_number = 1

show_info = 0

start_time = perf_counter()
pop_start_time = perf_counter()
while True:
	if not settings.pause:
		if (len(snakes) == 0):
			cur_time = perf_counter()
			time_mes = sec_to_formated(round(cur_time - start_time))
			this_pop_end_time = sec_to_formated(round(cur_time - pop_start_time))
			print("\nDEAD INFO\nPopulation Number", pop_number, "\nMAX SCORE IS: ", settings.max_score, " / ", settings.absolute_max_score, "\n", 
				settings.best_scores, "\n Num of eaten apples: ", sum(settings.eaten_apples), 
				"\nTime from start: ", time_mes, "\nPopulation play time: ", this_pop_end_time)

			pop_start_time = perf_counter()
			counter = 0
			settings.eaten_apples = [0] * settings.population_size
			pop_number += 1
			settings.use_old_data = True

			apples = [Apple(settings, snakes, draw_cell) for _ in range(settings.population_size // 2)]
			snakes = []
			for k in range(settings.population_size):
				snake = Snake(settings, draw_cell, draw_crown)

				for _ in range(5):
					snake.mutation()

				snakes.append(snake)

			settings.best_scores = [0, 0, 0, 0]
			settings.best_app = [None, None, None, None]
			settings.best_block = [None, None, None, None]

			for k in range(4):
				settings.best_app[k] = snakes[k].arr_app
				settings.best_block[k] = snakes[k].arr_block

			if (settings.max_score > settings.absolute_max_score):
				settings.absolute_max_score = settings.max_score

				if settings.autosave:
					settings.print_info = [pop_number, settings.absolute_max_score, round(perf_counter() - start_time)]
					save_weights(settings, settings.autosave_cell_ind)

			settings.max_score = 0

		counter += 1

		surf.fill((250, 250, 250))

		# draw_field(settings, False)

		[k.draw() for k in apples]

		for s_ind, snake in enumerate(snakes):
			if snake.score > settings.max_score:
				settings.max_score = snake.score
			if snake.update(snakes, snake):
				for i, b_score in enumerate(settings.best_scores):
					if (b_score < snake.score):
						settings.best_scores = [*settings.best_scores[:i], snake.score, *settings.best_scores[i:3]]
						settings.best_app = [*settings.best_app[:i], deepcopy(snake.arr_app), *settings.best_app[i:3]]
						settings.best_block = [*settings.best_block[:i], deepcopy(snake.arr_block), *settings.best_block[i:3]]
						break

				settings.eaten_apples.pop(s_ind)
				snakes.remove(snake)

				continue

			for apple in apples:
				if snake.check_apple_eating(apple):
					snake.inc_tail()

					settings.eaten_apples[s_ind] += 1

					apples.remove(apple)

			# p = input()
			snake.draw()
			snake.brain(apples, snakes)

			if rnd(1, 10) == 3:
				apples.append(Apple(settings, snakes, draw_cell))

			# if rnd(1, 10) == 3 and not settings.manual_control:
			# 	snake.change_direct(chs(["N", "E", "S", "W"]))

		clock.tick(FPS)

		screen.blit(surf, (0, 0))

		if (counter // 75 == 1):
			counter = 0
			cur_time = perf_counter()

			time_mes = sec_to_formated(round(cur_time - start_time))

			this_pop_end_time = sec_to_formated(round(cur_time - pop_start_time))

			if not (show_info):
				print("\nPopulation Number", pop_number, "\nMAX SCORE IS: ", settings.max_score, " / ", settings.absolute_max_score, "\n", 
					settings.best_scores, "\n Num of eaten apples: ", sum(settings.eaten_apples), 
					"\nTime from start: ", time_mes, "\nPopulation play time: ", this_pop_end_time)

			st_back = 0
			for ind in range(len(snakes)):
				if (settings.eaten_apples[ind - st_back] < 1):
					for i, b_score in enumerate(settings.best_scores):
						if (b_score < snake.score):
							settings.best_scores = [*settings.best_scores[:i], snake.score, *settings.best_scores[i:3]]
							settings.best_app = [*settings.best_app[:i], deepcopy(snake.arr_app), *settings.best_app[i:3]]
							settings.best_block = [*settings.best_block[:i], deepcopy(snake.arr_block), *settings.best_block[i:3]]
							break

					snakes.remove(snakes[ind - st_back])
					settings.eaten_apples.pop(ind - st_back)
					st_back += 1
				else:
					settings.eaten_apples[ind - st_back] = 0
		
	
	for i in pg.event.get():
		if i.type == pg.KEYDOWN:
			if i.key == 113 or i.key == 27:
				exit()


			elif i.key == 32: # Space	KILL AL SNAKES
				snakes = []


			elif i.key == 97: # ALL		SHOW APP ARRAYS
				show_info = 1 - show_info

				if (show_info):
					for k in range(len(settings.best_app)):
						for i in range(len(settings.best_app[0])):
							print(settings.best_app[k][i])
						print("\n")


			elif i.key == 98: # B 	SHOW BLOCK ARRAYS
				show_info = 1 - show_info

				if (show_info):
					for k in range(len(settings.best_app)):
						for i in range(len(settings.best_app[0])):
							print(settings.best_block[k][i])
						print("\n")


			elif i.key == 115: # S 		SAVE CURRENT WEIGHTS
				settings.pause = 1
				save_ind = ""
				while save_ind not in [str(k) for k in range(settings.save_cells_num + 1)]:
					save_ind = input("\nSelect save number: 1 - {} or Print 0 to cansel\t".format(settings.save_cells_num))

				if save_ind != "0":
					settings.print_info = [pop_number, settings.absolute_max_score, round(perf_counter() - start_time)]
					save_weights(settings, save_ind)
					print("\n\nSAVED TO THE {} SAVE LOCATION\n\n".format(save_ind))
				else:
					print("\n\nSAVE CANCELED\n\n")

				settings.pause = 0


			elif i.key == 108: # L 		LOAD WEIGHTS
				result_message = "\n\nLOAD CANCELED\n\n"

				settings.pause = 1
				save_ind = ""
				while save_ind not in [str(k) for k in range(settings.save_cells_num + 1)]:
					save_ind = input("\n\nSelect save number: 1 - {} or Print 0 to cansel\t".format(settings.save_cells_num))

				if save_ind != "0":
					if load_weights(settings, save_ind):
						pop_number = int(settings.print_info[0])
						settings.absolute_max_score = int(settings.print_info[1])

						start_time = round(perf_counter()) - settings.print_info[2]

						result_message = "\n\nLOADED\n\n"
						snakes = []

				print(result_message)
				settings.pause = 0


			elif i.key == 112: # P 		SET PAUSE
				settings.pause = 1 - settings.pause


			elif i.key == 99: # C 		TURNING ON/OFF AUTOSAVE 
				settings.pause = 1

				save_ind = ""
				while save_ind not in [str(k) for k in range(settings.save_cells_num + 1)]:
					save_ind = input("\n\nSelect autosave number: 1 - {} or Print 0 to cansel\t".format(settings.save_cells_num))

				if save_ind != "0":
					settings.autosave = 1 - settings.autosave
					settings.autosave_cell_ind = save_ind

					status = "ON" if (settings.autosave == 1) else "OFF"

					print("\n\nAUTOSAVE TURNED {}\n\n".format(status))
				else:
					print("\n\nAUTOSAVE CANSELED\n\n")

				settings.pause = 0


			elif i.key == 105: # I 		SHOW INFO ABAUT SAVE CELLS
				cells_info = [""] * settings.save_cells_num
				for i, info_arr in enumerate(save_cells_info(settings)):
					if type(info_arr) != type(None):
						cells_info[i] += str(i + 1) + ")" + " " * 3
						cells_info[i] += string_leveler(info_arr[0], 10) + " " * 3
						cells_info[i] += string_leveler(info_arr[1], 10) + " " * 3
						cells_info[i] += string_leveler(sec_to_formated(info_arr[2]), 10) + " " * 3
					else:
						cells_info[i] += str(i + 1) + ")" + " " * 3
						for k in range(3):
							cells_info[i] += string_leveler("-", 10) + " " * 3

				print("\n\n" + " " * 5 + "Population" + " " * 3 + string_leveler("Max score", 10) + " " * 3 + string_leveler("Work Time", 10))
				for cell_info in cells_info:
					print(cell_info)

				settings.pause = 1


			elif i.key == 100: # D 		DELETE SAVE CELL
				settings.pause = 1

				save_ind = ""
				while save_ind not in [str(k) for k in range(settings.save_cells_num + 1)]:
					save_ind = input("\n\nSelect delete number: 1 - {} or Print 0 to cansel\t".format(settings.save_cells_num))

				if (save_ind != "0"):
					if delete_save(save_ind):
						print("\n\nSAVE NUMBER {} HAS BEEN DELETED\n\n".format(save_ind))
					else:
						print("\n\nDELETE CANSELED\n\n")
				else:
					print("\n\nDELETE CANSELED\n\n")

				settings.pause = 0
			else:
				print(i.key)

	pg.display.update()
