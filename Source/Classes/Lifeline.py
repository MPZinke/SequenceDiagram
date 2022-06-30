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
from Classes.Components import Component
from Classes.Text import Text


SOURCE_DIR = str(Path(__file__).absolute().parent.parent)  # .../Source
RESOURCES_DIR = join(SOURCE_DIR, "Resources")  # .../Source/Resources


class Lifeline(Component):
	def __init__(self, name: str, text: str, *, border: int=100, buffer: int=50, canvas: Canvas=None, start: Set[int]=None):
		Component.__init__(self, canvas=canvas, start=start)
		self.title: Text = Text(text, canvas=canvas, font=Text.LARGE_FONT)
		self.border: int = border
		self.buffer: int = buffer
		self.name: str = name
		self.size: Set[int] = (self.title.dimensions()[0] + (buffer * 2), self.title.dimensions()[1])


	def __reduce__(self):
		return str(self)


	def __str__(self):
		return f"{{title: {self.title}, name: {self.name}, size: {self.size}, start: {self.start}}}"


	def append_title(self=None, *, border: int=None, buffer: int=None, canvas: Canvas=None) -> None:
		if(self is not None):
			canvas = self.canvas if(canvas is None) else canvas
			buffer = self.buffer if(buffer is None) else buffer
			border = self.border if(border is None) else border

		Text.check_params("append_title", **{"border": border, "buffer": buffer, "canvas": canvas})

		canvas_width, canvas_height = canvas.dimensions()
		text_width, text_height = self.title.dimensions()

		self.title.start = (canvas_width - border + buffer, border)
		self.start = (self.title.start[0] - buffer, self.title.start[1] + buffer)
		self.size = (self.title.dimensions()[0] + (buffer * 2), self.title.dimensions()[1])

		canvas.resize(canvas_width + text_width + (buffer * 2), max([canvas_height, border * 2 + text_height]))
		self.title.draw(canvas=canvas)


	def draw_line(self=None, *, border: int=None, buffer: int=None, canvas: Canvas=None) -> None:
		if(self is not None):
			canvas = self.canvas if(canvas is None) else canvas
			buffer = self.buffer if(buffer is None) else buffer
			border = self.border if(border is None) else border

		Text.check_params("append_title", **{"border": border, "buffer": buffer, "canvas": canvas})

		width, height = self.dimensions()
		start = (self.start[0] + (width / 2), self.start[1] + height)
		end = (self.start[0] + (width / 2), canvas.dimensions()[1] - border)
		canvas.line(start + end, fill=(255, 255, 255))


	def dimensions(self) -> Set[int]:
		return self.size
		


	def draw(self, canvas) -> None:
		text_width, text_height = canvas.textsize(self.value, font=Text.LARGE_FONT)
		canvas.text((self.x_pos - text_width / 2, 100), self.value, font=Text.LARGE_FONT)
		canvas_height = canvas.size[1]

		canvas.line((self.x_pos, 100+text_height+10, self.x_pos, canvas_height-100), fill=(255,255,255))
