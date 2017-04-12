# To import from the parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import sys
from antlr4 import *
from cGrammarLexer import cGrammarLexer
from cGrammarParser import cGrammarParser
from ASTCreator import ASTCreator
from PTranslator import PTranslator
from MyErrorListener import MyErrorListener

def main(argv):
    try:
        input = FileStream(argv[1])
        lexer = cGrammarLexer(input)
        stream = CommonTokenStream(lexer)
        parser = cGrammarParser(stream)
        parser._listeners = [MyErrorListener(argv[1])]
        tree = parser.program()

        ASTbuilder = ASTCreator()

        walker = ParseTreeWalker()
        walker.walk(ASTbuilder, tree)

        ast = ASTbuilder.getAST()

        translator = PTranslator()
        translator.translate(ast, "data/symbolTable.txt")

        translator.saveProgram("data/program.p")
        ASTbuilder.toDot("data/output.dot")

        # print("Created program text according to the Abstract Syntax Tree. (currently non functional)")
        # print("\nFinished parsing file (and building AST) without any errors.\n")

    except Exception as inst:
        print(inst)


if __name__ == '__main__':
    main(sys.argv)