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
from os.path import join
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple


from Classes.DrawTable import DrawSymbol
from Classes.SymbolTable import SymbolTable


SOURCE_DIR = str(Path(__file__).absolute().parent)  # .../Source
RESOURCES_DIR = join(SOURCE_DIR, "Resources")  # .../Source/Resources

MEDIUM_FONT = ImageFont.truetype(join(RESOURCES_DIR, "FiraCode-Bold.ttf"), size=20)



def draw_symbol_for_name(name: str, drawn_symbols: List[DrawSymbol]) -> DrawSymbol:
	for drawn_symbol in drawn_symbols:
		if(drawn_symbol.name == name):
			return drawn_symbol

	return None


def labeled_backward_sequence(left_symbol_name: str, right_symbol_name: str, label: str) -> None:
	def draw_backward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		left_draw_symbol = draw_symbol_for_name(left_symbol_name, drawn_symbols)
		right_draw_symbol = draw_symbol_for_name(right_symbol_name, drawn_symbols)

		draw_arrow(draw_area, (right_draw_symbol.x_pos, y_pos), (left_draw_symbol.x_pos, y_pos), None, None)
		
		#TODO write label
		print(label)

	return draw_backward_sequence


def labeled_circular_sequence(left_symbol_name: str, label: str) -> None:
	def draw_circular_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		return
		print("draw_circular_sequence")
		print(A)
		print(label)
		print()
		#TODO

	return draw_circular_sequence


def labeled_forward_sequence(left_symbol_name: str, right_symbol_name: str, label: str) -> None:
	def draw_forward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		left_draw_symbol = draw_symbol_for_name(left_symbol_name, drawn_symbols)
		right_draw_symbol = draw_symbol_for_name(right_symbol_name, drawn_symbols)

		text_width, text_height = draw_area.textsize(label, font=MEDIUM_FONT)
		x_pos = (left_draw_symbol.x_pos + right_draw_symbol.x_pos - text_width) / 2
		draw_area.text((x_pos, y_pos - (text_height / 2 + 15)), label, fill=(255, 255, 255), font=MEDIUM_FONT)

		y_pos += text_height / 2
		draw_arrow(draw_area, (left_draw_symbol.x_pos, y_pos), (right_draw_symbol.x_pos, y_pos), None, None)

	return draw_forward_sequence


def unlabeled_backward_sequence(left_symbol_name: str, right_symbol_name: str) -> None:
	def draw_backward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		left_draw_symbol = draw_symbol_for_name(left_symbol_name, drawn_symbols)
		right_draw_symbol = draw_symbol_for_name(right_symbol_name, drawn_symbols)

		draw_arrow(draw_area, (right_draw_symbol.x_pos, y_pos), (left_draw_symbol.x_pos, y_pos), None, None)

	return draw_backward_sequence


def unlabeled_circular_sequence(left_symbol_name: str) -> None:
	def draw_circular_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		return
		#TODO

	return draw_circular_sequence


def unlabeled_forward_sequence(left_symbol_name: str, right_symbol_name: str) -> None:
	def draw_forward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		left_draw_symbol = draw_symbol_for_name(left_symbol_name, drawn_symbols)
		right_draw_symbol = draw_symbol_for_name(right_symbol_name, drawn_symbols)

		draw_arrow(draw_area, (left_draw_symbol.x_pos, y_pos), (right_draw_symbol.x_pos, y_pos), None, None)

	return draw_forward_sequence


def draw_arrow(draw_area: ImageDraw, start: set, end: set, A: DrawSymbol, B: DrawSymbol) -> None:
	def head_point(head_angle: float, head_length: int, line_angle: float, tip_point: set) -> Tuple[int, int]:
		vector_x = math.cos(math.radians(head_angle - 180)) * head_length
		vector_y = math.sin(math.radians(head_angle - 180)) * head_length

		cos_line_angle = math.cos(line_angle)
		sin_line_angle = math.sin(line_angle)

		x_rotation = vector_x * cos_line_angle - vector_y * sin_line_angle
		y_rotation = vector_x * sin_line_angle + vector_y * cos_line_angle

		x_tranlation = x_rotation + tip_point[0]
		y_tranlation = y_rotation + tip_point[1]

		return (x_tranlation, y_tranlation)


	if(end[0] == start[0]):
		line_theta: float = math.radians(90.0 if(end[1] > start[1]) else -90)
	else:
		line_theta: float = math.atan((end[1]-start[1]) / (end[0]-start[0]))

	if(end[0] < start[0]):
		line_theta -= 3.141592653589793

	point1 = head_point(25, 20, line_theta, end)
	point2 = head_point(-25, 20, line_theta, end)

	draw_area.line(start+end, fill=(255,255,255))
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
	height = (len(sequences) - 1) * 100 + 300  # 100 top, 100 bottom, 32 Object, 68 buffer
	image = Image.new(mode="RGBA", size=[width, height])
	return image


def draw(sequences: List[callable], symbol_table: SymbolTable) -> None:
	image = create_canvas(sequences, symbol_table)
	draw_area = ImageDraw.Draw(image)
	drawn_symbols: List[DrawSymbol] = write_symbols(draw_area, symbol_table)
	for y, sequence in enumerate(sequences):
		sequence(draw_area, (y*100) + 166, drawn_symbols)

	image.show()
