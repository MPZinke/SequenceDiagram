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
from typing import List, Set, Tuple, Union


from Classes.Arrow import Arrow
from Classes.Canvas import Canvas
from Classes.Lifeline import Lifeline
from Classes.SymbolTable import SymbolTable
from Classes.Text import Text


SOURCE_DIR = str(Path(__file__).absolute().parent)  # .../Source
RESOURCES_DIR = join(SOURCE_DIR, "Resources")  # .../Source/Resources

SMALL_FONT = ImageFont.truetype(join(RESOURCES_DIR, "FiraCode-Bold.ttf"), size=16)
MEDIUM_FONT = ImageFont.truetype(join(RESOURCES_DIR, "FiraCode-Bold.ttf"), size=20)


# ———————————————————————————————————————————————————— CALLBACKS  ———————————————————————————————————————————————————— #

def draw_title(canvas: Canvas, symbol_table: SymbolTable) -> None:
	if(bool(title := symbol_table.symbols_by_type("TitleDeclaration")) is False):
		return

	title_text = Text(title[0].value[1:-1], canvas=canvas)

	canvas_width, canvas_height = canvas.dimensions()
	title_text_width, title_text_height = title_text.dimensions()

	canvas.resize(canvas_width, canvas_height+title_text_height, (0, title_text_height))
	title_text.draw(start=(canvas_width/2 - title_text_width/2, 0))


def labeled_backward_sequence(left_symbol_name: str, right_symbol_name: str, text: str) -> None:
	def draw_backward_sequence(canvas: Canvas, drawn_lifelines: List[Lifeline]) -> None:
		left_lifeline = lifeline_by_name(left_symbol_name, drawn_lifelines)
		right_lifeline = lifeline_by_name(right_symbol_name, drawn_lifelines)

		left_start = (left_lifeline.start[0] + (left_lifeline.dimensions()[0] / 2), left_lifeline.start[1])
		right_start = (right_lifeline.start[0] + (right_lifeline.dimensions()[0] / 2), right_lifeline.start[1])
		draw_arrow_and_text(canvas, right_start, left_start, text[1:-1])

	return draw_backward_sequence


def labeled_circular_sequence(left_symbol_name: str, label: str) -> None:
	def draw_circular_sequence(canvas: Canvas, drawn_lifelines: List[Lifeline]) -> None:
		print("draw_circular_sequence")
		#TODO

	return draw_circular_sequence


def labeled_forward_sequence(left_symbol_name: str, right_symbol_name: str, text: str) -> None:
	def draw_forward_sequence(canvas: Canvas, drawn_lifelines: List[Lifeline]) -> None:
		left_lifeline = lifeline_by_name(left_symbol_name, drawn_lifelines)
		right_lifeline = lifeline_by_name(right_symbol_name, drawn_lifelines)

		left_start = (left_lifeline.start[0] + (left_lifeline.dimensions()[0] / 2), left_lifeline.start[1])
		right_start = (right_lifeline.start[0] + (right_lifeline.dimensions()[0] / 2), right_lifeline.start[1])
		draw_arrow_and_text(canvas, left_start, right_start, text[1:-1])

	return draw_forward_sequence


def unlabeled_backward_sequence(left_symbol_name: str, right_symbol_name: str) -> None:
	def draw_backward_sequence(canvas: Canvas, drawn_lifelines: List[Lifeline]) -> None:
		left_lifeline = lifeline_by_name(left_symbol_name, drawn_lifelines)
		right_lifeline = lifeline_by_name(right_symbol_name, drawn_lifelines)

		Arrow(left_lifeline.start, start=right_lifeline.start).draw(canvas=canvas)

	return draw_backward_sequence


def unlabeled_circular_sequence(left_symbol_name: str) -> None:
	def draw_circular_sequence(canvas: Canvas, drawn_lifelines: List[Lifeline]) -> None:
		return
		#TODO

	return draw_circular_sequence


def unlabeled_forward_sequence(left_symbol_name: str, right_symbol_name: str) -> None:
	def draw_forward_sequence(canvas: Canvas, drawn_lifelines: List[Lifeline]) -> None:
		left_lifeline = lifeline_by_name(left_symbol_name, drawn_lifelines)
		right_lifeline = lifeline_by_name(right_symbol_name, drawn_lifelines)

		Arrow(right_lifeline.start, start=left_lifeline.start).draw(canvas=canvas)

	return draw_forward_sequence


# —————————————————————————————————————————————————— MAIN FUNCTIONS —————————————————————————————————————————————————— #

def draw(sequences: List[callable], symbol_table: SymbolTable) -> None:
	canvas = Canvas((200, 200))

	lifeline_symbols = symbol_table.symbols_by_types(["LeftSequence", "RightSequence"])
	lifelines = [Lifeline(symbol.name, symbol.value[1:-1], canvas=canvas) for symbol in lifeline_symbols]
	[lifeline.append_title() for lifeline in lifelines]
	[sequence(canvas, lifelines) for sequence in sequences]
	[lifeline.draw_line() for lifeline in lifelines]

	draw_title(canvas, symbol_table)

	canvas.show()


# ——————————————————————————————————————————————————————— DRAW ——————————————————————————————————————————————————————— #

def draw_arrow_and_text(canvas: Canvas, start: Set[int], tip_point: Set[int], text: str, *, buffer: int=15,
  border: int=100, font: ImageFont=SMALL_FONT) -> None:
	text_obj = Text(text, canvas=canvas, buffer=5, font=font)
	arrow = Arrow(tip_point, canvas=canvas, start=start)

	# Get dimensions
	arrow_width, arrow_height = arrow.dimensions()
	text_width, text_height = text_obj.dimensions()
	canvas_width, canvas_height = canvas.dimensions()

	canvas.resize(canvas_width, canvas_height + text_height + arrow_height + (buffer * 2))

	arrow.translate(0, canvas_height - border - start[1] + (buffer * 2) + text_height)
	text_obj.start = (((start[0] + tip_point[0]) / 2) - (text_width / 2), canvas_height - border + buffer)

	arrow.draw()
	text_obj.draw()


# ————————————————————————————————————————————————————— UTILITY  ————————————————————————————————————————————————————— #

def lifeline_by_name(name: str, lifelines: List[Lifeline]) -> Union[Lifeline, None]:
	return next((lifeline for lifeline in lifelines if(lifeline.name == name)), None)


def start_point_to_center_around(center: set, dimensions: set) -> set:
	return (center[0] - dimensions[0] / 2, center[1] - dimensions[1] / 2)


def text_dimensions(canvas: Canvas, text: str, *, buffer: int=15, font=SMALL_FONT) -> set:
	width, height = 0, buffer * text.count("\\n")
	for line in text.split("\\n"):
		text_width, text_height = canvas.textsize(line, font=font)
		height += text_height
		if(text_width > width):
			width = text_width

	return (width, height)
