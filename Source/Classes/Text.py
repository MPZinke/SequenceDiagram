#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.06.29                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from os.path import join
from pathlib import Path
from PIL import ImageDraw, ImageFont
from typing import Set


from Classes.Components import Component
from Classes.Canvas import Canvas


SOURCE_DIR = "/Users/aa703739/Repos/SequenceDiagram/Source"  # .../Source
RESOURCES_DIR = join(SOURCE_DIR, "Resources")  # .../Source/Resources


class Text(Component):
	LARGE_FONT: ImageFont = ImageFont.truetype(join(RESOURCES_DIR, "FiraCode-Bold.ttf"), size=32)
	MEDIUM_FONT = ImageFont.truetype(join(RESOURCES_DIR, "FiraCode-Bold.ttf"), size=20)
	SMALL_FONT = ImageFont.truetype(join(RESOURCES_DIR, "FiraCode-Bold.ttf"), size=16)

	LEFT: int = 0
	CENTER: int = LEFT+1
	RIGHT: int = CENTER+1

	def __init__(self, text: str, *, canvas: Canvas=None, buffer: int=15, font: ImageFont=SMALL_FONT,
	  start: Set[int]=None):
		Component.__init__(self, canvas=canvas, start=start)
		self.text = text
		self.buffer = buffer
		self.font = font


	def dimensions(self: object=None, *, buffer: int=None, canvas: Canvas=None, font=SMALL_FONT, text: str=None) \
	  -> Set[int]:
		if(self is not None):
			canvas = self.canvas if(canvas is None) else canvas
			text = self.text if(text is None) else text
			buffer = self.buffer if(buffer is None) else buffer
			font = self.font if(font is None) else font

		Text.check_params("dimensions", **{"canvas": canvas, "text": text, "buffer": buffer, "font": font})

		width, height = 0, buffer * text.count("\\n")
		for line in text.split("\\n"):
			text_width, text_height = canvas.textsize(line, font=font)
			height += text_height
			if(text_width > width):
				width = text_width

		return (width, height)


	def draw(self: object=None, *, align: int=CENTER, buffer: int=None, canvas: Canvas=None, font=SMALL_FONT,
	  start: Set[int]=None, text: str=None) -> None:
		if(self is not None):
			canvas = self.canvas if(canvas is None) else canvas
			text = self.text if(text is None) else text
			buffer = self.buffer if(buffer is None) else buffer
			font = self.font if(font is None) else font
			start = self.start if(start is None) else start

		Text.check_params("draw", **{"canvas": canvas, "text": text, "buffer": buffer, "font": font, "start": start})

		for line in text.split("\\n"):
			canvas.text(start, line, fill=(255, 255, 255), font=font)
			start = (start[0], start[1] + canvas.textsize(line, font=font)[1] + buffer)

