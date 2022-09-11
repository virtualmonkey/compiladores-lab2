import sys
import os
from antlr4 import *
from YAPLLexer import YAPLLexer
from YAPLParser import YAPLParser
from YAPLVisitor import YAPLVisitor
from antlr4.tree.Trees import Trees
from MyYAPLVisitor import MyYAPLVisitor
from MyYAPLNewVisitor import MyYAPLNewVisitor
from objects.Error import Error

if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = FileStream(sys.argv[1])
    else:
        data = InputStream(sys.stdin.readline())

    #lexer
    lexer = YAPLLexer(data)
    stream = CommonTokenStream(lexer)
    #parser
    parser = YAPLParser(stream)
    tree = parser.program()

    # evaluator
    myYAPLVisitor = MyYAPLVisitor()
    myYAPLVisitor.visit(tree)

    myYAPLNewVisitor = MyYAPLNewVisitor(myYAPLVisitor.table, myYAPLVisitor.errors)
    myYAPLNewVisitor.visit(tree)

    print(30*"=" + " Symbols Table " + 30*"=")
    print("\n")
    for myClass in myYAPLNewVisitor.table.classes:
        print(myClass)
    print("\n")
    for myFunction in myYAPLNewVisitor.table.attributes:
        print(myFunction)
    print("\n")
    for myAttribute in myYAPLNewVisitor.table.functions:
        print(myAttribute)
    print("\n")
    print(30*"=" + " End of Table " + 30*"=")
    
    
    if not myYAPLNewVisitor.table.findClass("Main"):
        myYAPLNewVisitor.errors.append(
            Error(
                "SyntaxError",
                "0",
                "YAPL programas must have a Main class"
            )
        )
    
    if not myYAPLNewVisitor.table.getFunctionWithName("main", "Main"):
        myYAPLNewVisitor.errors.append(
            Error(
                "SyntaxError",
                "0",
                "Main class must have a main method"
            )
        )

    if len(myYAPLNewVisitor.errors) > 0:
        for myError in myYAPLNewVisitor.errors:
            print(str(myError))
    else:
        print("Compiled successfully!")