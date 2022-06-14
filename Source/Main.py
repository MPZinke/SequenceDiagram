

from sys import stderr


import Lexer
import Parser
import Classes.ParseTree
import SemanticAnalysis
from Classes.Token import TokenErr


def main():
	with open("Test.sequence", "r") as file:
		try:
			tokens: list = Lexer.parse([line.strip() for line in file.readlines()])
			print([token.type for token in tokens])
			abstract_syntax_tree: ParseTree.ParseTree  = Parser.parse(tokens)
			print(str(abstract_syntax_tree))
			SemanticAnalysis.traverse(abstract_syntax_tree)
		except TokenErr as error:
			print(error, file=stderr)



if __name__ == '__main__':
	main()
