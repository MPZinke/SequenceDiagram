#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.06.16                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import math
from PIL import ImageDraw
from typing import Tuple, Union


class Arrow:
	DEFAULT_ANGLE = 25
	DEFAULT_LENGTH = 20


	def __init__(self, draw_area: ImageDraw, tip_point: set, line_angle: float=None, *, start_point: set=None,
	  head_angle: float=DEFAULT_ANGLE, head_length: int=DEFAULT_LENGTH):
		if(line_angle is None and start_point is None):
			raise Exception("line_angle and start_point cannot both be None for Arrow::()")
		self.draw_area: ImageDraw = draw_area
		self.head_angle: float = head_angle
		self.head_length: int = head_length
		self.start_point: set = start_point
		self.line_angle: float = line_angle
		self.tip_point: set = tip_point


	def draw(self: object=None, *, draw_area: ImageDraw=None, line_angle: float=None, start_point: set=None,
	  tip_point: set=None, head_angle: float=DEFAULT_ANGLE, head_length: int=DEFAULT_LENGTH) -> bool:
		if(self is not None):
			draw_area = self.draw_area if(draw_area is None) else draw_area
			line_angle = self.line_angle if(line_angle is None) else line_angle
			start_point = self.start_point if(start_point is None) else start_point
			tip_point = self.tip_point if(tip_point is None) else tip_point
			head_angle = self.head_angle if(head_angle is None) else head_angle
			head_length = self.head_length if(head_length is None) else head_length

		elif(any(param is None for param in [start_point, draw_area, tip_point, head_angle, head_length])):
			parameters = [start_point, draw_area, tip_point, head_angle, head_length]
			names = ["start_point", "draw_area", "tip_point", "head_angle", "head_length"]
			first_missing_param = [name for name, param in zip(names, parameters) if(param is None)][0]
			raise Exception(f"Parameter '{first_missing_param}' cannot be None for Arrow::draw_head")

		line_angle: float = Arrow.calculate_line_angle(start_point, tip_point)
		self.draw_head(line_angle=line_angle)

		draw_area.line(start_point+tip_point, fill=(255, 255, 255))


	def draw_head(self: object=None, *, draw_area: ImageDraw=None, line_angle: float=None, tip_point: set=None,
	  head_angle: float=DEFAULT_ANGLE, head_length: int=DEFAULT_LENGTH) -> None:
		if(self is not None):
			draw_area = self.draw_area if(draw_area is None) else draw_area
			line_angle = self.line_angle if(line_angle is None) else line_angle
			tip_point = self.tip_point if(tip_point is None) else tip_point
			head_angle = self.head_angle if(head_angle is None) else head_angle
			head_length = self.head_length if(head_length is None) else head_length

		elif(any(param is None for param in [draw_area, line_angle, tip_point, head_angle, head_length])):
			parameters = [draw_area, line_angle, tip_point, head_angle, head_length]
			names = ["draw_area", "line_angle", "tip_point", "head_angle", "head_length"]
			first_missing_param = [name for name, param in zip(names, parameters) if(param is None)][0]
			raise Exception(f"Parameter '{first_missing_param}' cannot be None for Arrow::draw_head")

		point1 = Arrow.head_point(line_angle=line_angle, tip_point=tip_point, head_angle=head_angle,
		  head_length=head_length)
		point2 = Arrow.head_point(line_angle=line_angle, tip_point=tip_point, head_angle=-head_angle,
		  head_length=head_length)

		draw_area.polygon((tip_point, point1, point2), fill=(255, 255, 255))


	def head_point(self: object=None, *, head_angle: float=None, head_length: int=None, line_angle: float=None,
	  tip_point: set=None) -> Union[Tuple[int, int], None]:
		if(self is not None):
			line_angle = self.line_angle if(line_angle is None) else line_angle
			tip_point = self.tip_point if(tip_point is None) else tip_point
			head_angle = self.head_angle if(head_angle is None) else head_angle
			head_length = self.head_length if(head_length is None) else head_length

		elif(any(param is None for param in [line_angle, tip_point, head_angle, head_length])):
			parameters = [line_angle, tip_point, head_angle, head_length]
			names = ["line_angle", "tip_point", "head_angle", "head_length"]
			first_missing_param = [name for name, param in zip(names, parameters) if(param is None)][0]
			raise Exception(f"Parameter '{first_missing_param}' cannot be None for Arrow::draw_head")

		vector_x = math.cos(math.radians(head_angle - 180)) * head_length
		vector_y = math.sin(math.radians(head_angle - 180)) * head_length

		cos_line_angle = math.cos(math.radians(line_angle))
		sin_line_angle = math.sin(math.radians(line_angle))

		x_rotation = vector_x * cos_line_angle - vector_y * sin_line_angle
		y_rotation = vector_x * sin_line_angle + vector_y * cos_line_angle

		x_tranlation = x_rotation + tip_point[0]
		y_tranlation = y_rotation + tip_point[1]

		return (x_tranlation, y_tranlation)


	@staticmethod
	def calculate_line_angle(start: set, end: set) -> float:
		if(end[0] == start[0]):
			return 90.0 if(end[1] > start[1]) else -90

		line_angle: float = math.degrees(math.atan((end[1]-start[1]) / (end[0]-start[0])))

		if(end[0] < start[0]):
			line_angle -= 180

		return line_angle


def test():
	from PIL import Image

	image = Image.new(mode="RGBA", size=[600, 600])
	draw_area = ImageDraw.Draw(image)

	start = (100, 300)
	end = (500, 300)
	arrow = Arrow(draw_area, end, start_point=start)
	arrow.draw()

	start = (100, 100)
	end = (500, 500)
	line_angle: float = Arrow.calculate_line_angle(start, end)
	arrow = Arrow(draw_area, end, line_angle)
	arrow.draw_head()
	draw_area.line(start+end, fill=(255, 255, 255))

	end = (100, 500)
	start = (500, 100)
	line_angle: float = Arrow.calculate_line_angle(start, end)

	Arrow.draw_head(draw_area=draw_area, line_angle=line_angle, tip_point=end)
	draw_area.line(start+end, fill=(255, 255, 255))

	image.show()


if __name__ == '__main__':
	test()
