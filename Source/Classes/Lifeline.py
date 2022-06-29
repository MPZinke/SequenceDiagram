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


from os.path import join
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Set


from Classes.Canvas import Canvas
from Classes.Text import Text


SOURCE_DIR = str(Path(__file__).absolute().parent.parent)  # .../Source
RESOURCES_DIR = join(SOURCE_DIR, "Resources")  # .../Source/Resources


class Lifeline:
	def __init__(self, canvas: Canvas, name: str, value: str, start: Set[int]=None):
		self.canvas: str = canvas
		self.title: str = Text(value, canvas=canvas, font=Text.LARGE_FONT)
		self.size = self.title.dimensions()
		self.start = start
		self.value: str = value


	def append_title(self, canvas: Image, *, buffer: int=50, border: int=100) -> ImageDraw:
		canvas_width, canvas_height = canvas.dimensions()
		text_width, text_height = self.title.dimensions()
		self.title.start = (canvas_width - border, border)
		print(self.title.start)

		canvas.resize((canvas_width + text_width + buffer, canvas_height))
		print(canvas.dimensions())
		self.title.draw(canvas=canvas)

		

	def dimensions(self) -> Set[int]:
		pass
		


	def draw(self, canvas) -> None:
		text_width, text_height = canvas.textsize(self.value, font=Text.LARGE_FONT)
		canvas.text((self.x_pos - text_width / 2, 100), self.value, font=Text.LARGE_FONT)
		canvas_height = canvas.size[1]

		canvas.line((self.x_pos, 100+text_height+10, self.x_pos, canvas_height-100), fill=(255,255,255))
