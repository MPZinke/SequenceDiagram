


import Lexer
import Parser


def main():
	with open("Test.sequence", "r") as file:
		tokens: list = Lexer.parse([line.strip() for line in file.readlines()])
		print([token.type for token in tokens])
		abstract_syntax_tree = Parser.parse(tokens)
		print(str(abstract_syntax_tree))


if __name__ == '__main__':
	main()
