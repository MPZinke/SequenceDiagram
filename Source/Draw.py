#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.06.14                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import math
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple


from Classes.DrawTable import DrawSymbol
from Classes.SymbolTable import SymbolTable


def labeled_backward_sequence(A: str, B: str, label: str) -> None:
	def draw_backward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		return
		print("draw_backward_sequence")
		print(A)
		print(B)
		print(label)
		print()
		#TODO

	return draw_backward_sequence


def labeled_circular_sequence(A: str, label: str) -> None:
	def draw_circular_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		return
		print("draw_circular_sequence")
		print(A)
		print(label)
		print()
		#TODO

	return draw_circular_sequence


def labeled_forward_sequence(A: str, B: str, label: str) -> None:
	def draw_forward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		A_draw_symbol = [drawn_symbol for drawn_symbol in drawn_symbols if(drawn_symbol.name == A)][0]
		B_draw_symbol = [drawn_symbol for drawn_symbol in drawn_symbols if(drawn_symbol.name == B)][0]

		# draw_area.line((A_draw_symbol.x_pos, y_pos, B_draw_symbol.x_pos, y_pos), fill=(255,255,255))
		draw_arrow(draw_area, (A_draw_symbol.x_pos, y_pos), (B_draw_symbol.x_pos, y_pos), None, None)
		print("draw_forward_sequence")
		print(A_draw_symbol)
		print(B_draw_symbol)
		print(label)
		print()
		return "Hello"
		#TODO

	return draw_forward_sequence


def unlabeled_backward_sequence(A: str, B: str) -> None:
	def draw_backward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		return
		print("draw_backward_sequence")
		print(A)
		print(B)
		print()
		#TODO

	return draw_backward_sequence


def unlabeled_circular_sequence(A: str) -> None:
	def draw_circular_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		return
		print("draw_circular_sequence")
		print(A)
		print()
		#TODO

	return draw_circular_sequence


def unlabeled_forward_sequence(A: str, B: str) -> None:
	def draw_forward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		return
		print("draw_forward_sequence")
		print(A)
		print(B)
		print()
		#TODO

	return draw_forward_sequence


def draw_arrow(draw_area: ImageDraw, start: set, end: set, A: DrawSymbol, B: DrawSymbol) -> None:
	def head_point(angle: float, point: set, magnitudex: int, magnitudey) -> Tuple[int, int]:
		# FROM: https://stackoverflow.com/a/1571322
		return (magnitudex * 100 * math.cos(angle) + point[0], magnitudey * 100 * math.sin(angle) + point[1])

	start1 = (150, 50)
	end1 = (500, 50)
	start2 = (100, 50)
	end2 = (500, 450)
	start3 = (50, 50)
	end3 = (50, 450)

	start4 = (150, 1250)
	end4 = (500, 1250)
	start5 = (100, 1250)
	end5 = (500, 850)
	start6 = (50, 1250)
	end6 = (50, 850)

	start7 = (1050, 50)
	end7 = (700, 50)
	start8 = (1100, 50)
	end8 = (700, 450)
	start9 = (1150, 50)
	end9 = (1150, 450)

	start10 = (1050, 1250)
	end10 = (700, 1250)
	start11 = (1100, 1250)
	end11 = (700, 850)
	start12 = (1150, 1250)
	end12 = (1150, 850)



	for end, start in zip([end1, end2, end3, end4, end5, end6, end7, end8, end9, end10, end11, end12],
	 [start1, start2, start3, start4, start5, start6, start7, start8, start9, start10, start11, start12]):
		draw_area.line(start+end, fill=(255,255,255))

		line_theta: float = math.atan((end[1]-start[1]) / (end[0]-start[0])) if(end[0] != start[0]) else 180.0
		magnitudex = -1 if(end[1] < start[1]) else 1
		magnitudey = -1 if(end[0] < start[0]) else 1
		point1 = head_point(math.radians(30+line_theta), end, magnitudex, magnitudey)  # 90 - 30°
		point2 = head_point(math.radians(30-line_theta), end, magnitudex, magnitudey)  # -90 + 30°
		# point1 = (end[0] + 100*math.cos(line_theta-150), end[1] + 100*math.sin(line_theta-150))
		# point2 = (end[0] + 100*math.cos(line_theta+150), end[1] + 100*math.sin(line_theta+150))
		draw_area.polygon((end, point1, point2), fill=(255,255,255))


def write_symbols(draw_area: ImageDraw, symbol_table: SymbolTable) -> List[DrawSymbol]:
	draw_symbols: List[DrawSymbol] = []
	for x, symbol in enumerate(symbol_table):
		x_pos = x * 200 + 200
		draw_symbol = DrawSymbol(symbol.name, symbol.value, x_pos)
		draw_symbol.draw(draw_area)

		draw_symbols.append(draw_symbol)
	return draw_symbols


def create_canvas(sequences: List[callable], symbol_table: SymbolTable) -> Image:
	width = (len(symbol_table) - 1) * 200 + 400
	height = (len(sequences) - 1) * 150 + 300  # 100 top, 100 bottom, 32 Object, 68 buffer
	image = Image.new(mode="RGBA", size=[width, height])
	return image


def draw(sequences: List[callable], symbol_table: SymbolTable) -> None:
	image = create_canvas(sequences, symbol_table)
	draw_area = ImageDraw.Draw(image)
	drawn_symbols: List[DrawSymbol] = write_symbols(draw_area, symbol_table)
	for y, sequence in enumerate(sequences):
		print(sequence)
		print(sequence(draw_area, (y*150) + 166, drawn_symbols))

	image.show()
