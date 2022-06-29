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
from typing import List, Set, Tuple


from Classes.Arrow import Arrow
from Classes.Lifeline import Lifeline
from Classes.SymbolTable import SymbolTable


SOURCE_DIR = str(Path(__file__).absolute().parent)  # .../Source
RESOURCES_DIR = join(SOURCE_DIR, "Resources")  # .../Source/Resources

SMALL_FONT = ImageFont.truetype(join(RESOURCES_DIR, "FiraCode-Bold.ttf"), size=16)
MEDIUM_FONT = ImageFont.truetype(join(RESOURCES_DIR, "FiraCode-Bold.ttf"), size=20)


# ———————————————————————————————————————————————————— CALLBACKS  ———————————————————————————————————————————————————— #

def labeled_backward_sequence(left_symbol_name: str, right_symbol_name: str, text: str) -> None:
	def draw_backward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[Lifeline]) -> None:
		left_draw_symbol = draw_symbol_for_name(left_symbol_name, drawn_symbols)
		right_draw_symbol = draw_symbol_for_name(right_symbol_name, drawn_symbols)

		draw_arrow_and_text(draw_area, (right_draw_symbol.x_pos, y_pos), (left_draw_symbol.x_pos, y_pos), text)

	return draw_backward_sequence


def labeled_circular_sequence(left_symbol_name: str, label: str) -> None:
	def draw_circular_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[Lifeline]) -> None:
		print("draw_circular_sequence")
		#TODO

	return draw_circular_sequence


def labeled_forward_sequence(left_symbol_name: str, right_symbol_name: str, text: str) -> None:
	def draw_forward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[Lifeline]) -> None:
		left_draw_symbol = draw_symbol_for_name(left_symbol_name, drawn_symbols)
		right_draw_symbol = draw_symbol_for_name(right_symbol_name, drawn_symbols)

		draw_arrow_and_text(draw_area, (left_draw_symbol.x_pos, y_pos), (right_draw_symbol.x_pos, y_pos), text)

	return draw_forward_sequence


def unlabeled_backward_sequence(left_symbol_name: str, right_symbol_name: str) -> None:
	def draw_backward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[Lifeline]) -> None:
		left_draw_symbol = draw_symbol_for_name(left_symbol_name, drawn_symbols)
		right_draw_symbol = draw_symbol_for_name(right_symbol_name, drawn_symbols)

		Arrow((left_draw_symbol.x_pos, y_pos), start_point=(right_draw_symbol.x_pos, y_pos)).draw(draw_area=draw_area)

	return draw_backward_sequence


def unlabeled_circular_sequence(left_symbol_name: str) -> None:
	def draw_circular_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[Lifeline]) -> None:
		return
		#TODO

	return draw_circular_sequence


def unlabeled_forward_sequence(left_symbol_name: str, right_symbol_name: str) -> None:
	def draw_forward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[Lifeline]) -> None:
		left_draw_symbol = draw_symbol_for_name(left_symbol_name, drawn_symbols)
		right_draw_symbol = draw_symbol_for_name(right_symbol_name, drawn_symbols)

		Arrow((right_draw_symbol.x_pos, y_pos), start_point=(left_draw_symbol.x_pos, y_pos)).draw(draw_area=draw_area)

	return draw_forward_sequence


# —————————————————————————————————————————————————— MAIN FUNCTIONS —————————————————————————————————————————————————— #

def draw(sequences: List[callable], symbol_table: SymbolTable) -> None:
	lifelines = [Lifeline(symbol.name, symbol.value, x * 200 + 200) for x, symbol in enumerate(symbol_table)]

	# Create draw_area
	width = (len(symbol_table) - 1) * 200 + 400
	height = (len(sequences) - 1) * 100 + 300  # 100 top, 100 bottom, 32 Object, 68 buffer
	image = Image.new(mode="RGBA", size=[width, height])
	draw_area = ImageDraw.Draw(image)

	[lifeline.draw(draw_area) for lifeline in lifelines]
	[sequence(draw_area, (y*100) + 166, lifelines) for y, sequence in enumerate(sequences)]

	image.show()


# ——————————————————————————————————————————————————————— DRAW ——————————————————————————————————————————————————————— #

def draw_arrow_and_text(draw_area: ImageDraw, start_point: Set[int], tip_point: Set[int], text: str, *, buffer: int=15,
  font=SMALL_FONT) -> None:
	arrow = Arrow(tip_point, start_point=start_point)

	# Get dimensions
	_, arrow_height = arrow.dimensions()
	text_width, text_height = text_dimensions(draw_area, text)

	# Get positions based on center point
	center: Set[int] = arrow.center()
	text_position = (center[0] - (text_width / 2), center[1] - ((text_height+arrow_height+15) / 2))
	arrow_translation = (0, (text_height+arrow_height) / 2 - arrow_height + 15)

	for line in text.split("\\n"):
		draw_area.text(text_position, line, fill=(255, 255, 255), font=font)
		text_position = (text_position[0], text_position[1] + draw_area.textsize(line, font=font)[1] + buffer)

	arrow.translate(*arrow_translation)
	arrow.draw(draw_area=draw_area)


# ————————————————————————————————————————————————————— UTILITY  ————————————————————————————————————————————————————— #

def draw_symbol_for_name(name: str, drawn_symbols: List[Lifeline]) -> Lifeline:
	for drawn_symbol in drawn_symbols:
		if(drawn_symbol.name == name):
			return drawn_symbol

	return None


def start_point_to_center_around(center: set, dimensions: set) -> set:
	return (center[0] - dimensions[0] / 2, center[1] - dimensions[1] / 2)


def text_dimensions(draw_area: ImageDraw, text: str, *, buffer: int=15, font=SMALL_FONT) -> set:
	width, height = 0, buffer * text.count("\\n")
	for line in text.split("\\n"):
		text_width, text_height = draw_area.textsize(line, font=font)
		height += text_height
		if(text_width > width):
			width = text_width

	return (width, height)
