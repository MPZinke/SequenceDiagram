

from typing import Tuple, Union



class ParseTree:
	def __init__(self):
		self.start = None


	def print(self):
		self.start.print()


	def __str__(self):
		return str(self.start)


class ParseToken:
	def __init__(self, type, tokens):
		self.type = type
		self.tokens = tokens


	def __str__(self):
		return self.type + "".join(["\n    " + "\n    ".join(str(token).split("\n")) for token in self.tokens])




def Program(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Program -> Expression | ε
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def Expression(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Expression -> Declaration | Sequence
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def Declaration(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Declaration -> DeclarationString | DeclarationString Expression
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def DeclarationString(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	DeclarationString -> Identifier-Colon String-NewLine
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def Sequence(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Sequence -> LeftSequence | LeftSequence Expression | RightSequence | RightSequence Expression
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def LeftSequence(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	LeftSequence -> Identifier-LeftArrow Identifier | Identifier-LeftArrow Identifier-NewLine
	  | Identifier-LeftArrow Identifier-String | Identifier-LeftArrow Identifier-String--NewLine
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def RightSequence(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	RightSequence -> Identifier-RightArrow Identifier | Identifier-RightArrow Identifier-NewLine
	  | Identifier-RightArrow Identifier-String | Identifier-RightArrow Identifier-String--NewLine
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1



def Identifier_Colon(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Identifier-Colon -> Identifier Colon
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def Identifier_LeftArrow(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Identifier-LeftArrow -> Identifier LeftArrow
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def Identifier_RightArrow(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Identifier-RightArrow -> Identifier RightArrow
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def Identifier_NewLine(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Identifier-NewLine -> Identifier NewLine
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def Identifier_String(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Identifier-String -> Identifier String
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def Identifier_String__NewLine(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Identifier-String--NewLine -> Identifier-String NewLine
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def String_NewLine(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	String-NewLine -> String NewLine
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


# ———————————————————————————————————————————————————— TERMINALS  ———————————————————————————————————————————————————— #

def Identifier(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Identifier -> "[_a-zA-Z][_a-zA-Z0-9]*"
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def String(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	String -> "\"([^\\\"]|\\.)*\""
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def Colon(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Colon -> ":"
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def RightArrow(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	RightArrow -> "->"
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def LeftArrow(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	LeftArrow -> "<-"
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def NewLine(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	NewLine -> "\n+"
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


def WhiteSpace(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	WhiteSpace -> "[ \t\r]+"
	"""
	if(index >= len(token_list)):
		return None, index+1

	return None, index+1


# —————————————————————————————————————————————————————— PARSE  —————————————————————————————————————————————————————— #

def parse(token_list) -> Union[ParseToken, None]:
	
