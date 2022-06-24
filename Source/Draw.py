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


from Classes.Arrow import Arrow
from Classes.DrawTable import DrawSymbol
from Classes.SymbolTable import SymbolTable


SOURCE_DIR = str(Path(__file__).absolute().parent)  # .../Source
RESOURCES_DIR = join(SOURCE_DIR, "Resources")  # .../Source/Resources

MEDIUM_FONT = ImageFont.truetype(join(RESOURCES_DIR, "FiraCode-Bold.ttf"), size=20)

def start_point_to_center_around(center: set, dimensions: set) -> set:
	return (center[0] + dimensions[0] /  2, center[2] + dimensions[2] /  2)


# def center_objects_over_point(point: int, size1: int, buffer: int, size2: int):
def text_dimensions(draw_area: ImageDraw, text: str, *, buffer: int=15, font=MEDIUM_FONT) -> set:
	height, width = buffer * text.count("\\n"), 0
	for line in text.split("\\n"):
		text_width, text_height = draw_area.textsize(line, font=font)
		height += text_height
		if(text_width > width):
			width = text_width

	return (height, width)


def write_text(draw_area: ImageDraw, text: str, center: set, border: set) -> None:
	
	for x, line in enumerate(text.split("\\n")):

		text_width, text_height = draw_area.textsize(line, font=font)
		height += text_height
		if(text_width > width):
			width = text_width

	return (height, width)



def draw_symbol_for_name(name: str, drawn_symbols: List[DrawSymbol]) -> DrawSymbol:
	for drawn_symbol in drawn_symbols:
		if(drawn_symbol.name == name):
			return drawn_symbol

	return None


def labeled_backward_sequence(left_symbol_name: str, right_symbol_name: str, label: str) -> None:
	def draw_backward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		left_draw_symbol = draw_symbol_for_name(left_symbol_name, drawn_symbols)
		right_draw_symbol = draw_symbol_for_name(right_symbol_name, drawn_symbols)

		Arrow((left_draw_symbol.x_pos, y_pos), start_point=(right_draw_symbol.x_pos, y_pos)).draw(draw_area=draw_area)

		#TODO write label
		print(label)

	return draw_backward_sequence


def labeled_circular_sequence(left_symbol_name: str, label: str) -> None:
	def draw_circular_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		print("draw_circular_sequence")
		#TODO

	return draw_circular_sequence


def labeled_forward_sequence(left_symbol_name: str, right_symbol_name: str, label: str) -> None:
	def draw_forward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		left_draw_symbol = draw_symbol_for_name(left_symbol_name, drawn_symbols)
		right_draw_symbol = draw_symbol_for_name(right_symbol_name, drawn_symbols)

		arrow = Arrow((right_draw_symbol.x_pos, y_pos), start_point=(left_draw_symbol.x_pos, y_pos))

		_, arrow_height = arrow.dimensions()
		text_width, text_height = text_dimensions(draw_area, label)

		text_x_pos = (left_draw_symbol.x_pos + right_draw_symbol.x_pos - text_width) / 2
		text_y_position = y_pos - (text_height + arrow_height + 15) / 2
		draw_area.text((text_x_pos, text_y_position), label, fill=(255, 255, 255), font=MEDIUM_FONT)
		# OR text_y_pos + text_height + 15
		arrow_y_position = y_pos + (text_height + arrow_height + 15) / 2 - arrow_height
		arrow.translate(0, arrow_y_position - y_pos)
		arrow.draw(draw_area=draw_area)



	return draw_forward_sequence


def unlabeled_backward_sequence(left_symbol_name: str, right_symbol_name: str) -> None:
	def draw_backward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		left_draw_symbol = draw_symbol_for_name(left_symbol_name, drawn_symbols)
		right_draw_symbol = draw_symbol_for_name(right_symbol_name, drawn_symbols)

		Arrow((left_draw_symbol.x_pos, y_pos), start_point=(right_draw_symbol.x_pos, y_pos)).draw(draw_area=draw_area)

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

		Arrow((right_draw_symbol.x_pos, y_pos), start_point=(left_draw_symbol.x_pos, y_pos)).draw(draw_area=draw_area)

	return draw_forward_sequence


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
