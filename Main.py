

from sys import stderr


import Lexer
import Parser
import ParseTree


def main():
	with open("Test.sequence", "r") as file:
		tokens: list = Lexer.parse([line.strip() for line in file.readlines()])
		print([token.type for token in tokens])
		try:
			abstract_syntax_tree: ParseTree.ParseTree  = Parser.parse(tokens)
			print(str(abstract_syntax_tree))
		except (Parser.UnexpectedEOF, Parser.UnexpectedToken) as error:
			print(error, file=stderr)


if __name__ == '__main__':
	main()
