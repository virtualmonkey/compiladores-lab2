from YAPLParser import YAPLParser
from YAPLVisitor import YAPLVisitor

# This class defines a complete generic visitor for a parse tree produced by YAPLParser.
from objects.Class import Class
from objects.Function import Function
from objects.Attribute import Attribute
from objects.Error import Error

from tables.SymbolsTable import *

class MyYAPLVisitor(YAPLVisitor):
    def __init__(self):
        super().__init__()
        self.table = SymbolsTable()
        self.errors = []
        self.CLASS = ""
        self.METHOD = ""
        self.METHOD_NO = 10
        self.SCOPE = 1

    # Visit a parse tree produced by YAPLParser#start.
    def visitStart(self, ctx:YAPLParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#program.
    def visitProgram(self, ctx:YAPLParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#classExpr.
    def visitClassExpr(self, ctx:YAPLParser.ClassExprContext):
        classIdentifier = str(ctx.TYPE()[0])
        classParents = ctx.TYPE()
        if len(classParents) > 1:
            inheritedClass = str(classParents[1])
            
            if not self.table.findClass(inheritedClass):
                self.errors.append(
                    Error(
                        "NameError",
                        ctx.start.line,
                        "class '" + inheritedClass + "' is not defined"
                    )
                )
                return "Error"
        else: inheritedClass = None
        
        if inheritedClass:
            newClass = Class(classIdentifier, inheritedClass)
        else:
            newClass = Class(classIdentifier)
        addition = self.table.addClass(newClass)

        if not addition:
            self.errors.append(
                Error(
                    "NameError",
                    ctx.start.line,
                    "class '" + classIdentifier + "' has already been defined in current scope"
                )
            )
            return "Error"
        else:
            self.CLASS = classIdentifier
            self.METHOD = None
            self.SCOPE = 1
            return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#method.
    def visitMethod(self, ctx:YAPLParser.MethodContext):
        self.METHOD_NO = self.METHOD_NO + 1

        methodIdentifier = str(ctx.ID())
        methodType = str(ctx.TYPE())
        
        addition = self.table.addFunction(
            Function(
                self.METHOD_NO,
                methodIdentifier,
                methodType,
                self.SCOPE,
                self.CLASS
            )
        )
        
        self.SCOPE = 2
        if not addition:
            self.errors.append(
                Error(
                    "NameError",
                    ctx.ID().getPayload().line,
                    "method '" + methodIdentifier + "' has already been defined in current scope"
                )
            )
            return "Error"
        else:
            self.METHOD = methodIdentifier
            for child in ctx.formal(): self.visit(child)
            return self.visit(ctx.expr())


    # Visit a parse tree produced by YAPLParser#attribute.
    def visitAttribute(self, ctx:YAPLParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#formal.
    def visitFormal(self, ctx:YAPLParser.FormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#add.
    def visitAdd(self, ctx:YAPLParser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#new.
    def visitNew(self, ctx:YAPLParser.NewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#negation.
    def visitNegation(self, ctx:YAPLParser.NegationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#dispatch.
    def visitDispatch(self, ctx:YAPLParser.DispatchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#string.
    def visitString(self, ctx:YAPLParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#assignment.
    def visitAssignment(self, ctx:YAPLParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#false.
    def visitFalse(self, ctx:YAPLParser.FalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#integer.
    def visitInteger(self, ctx:YAPLParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#while.
    def visitWhile(self, ctx:YAPLParser.WhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#parenthesis.
    def visitParenthesis(self, ctx:YAPLParser.ParenthesisContext):
       return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#equal.
    def visitEqual(self, ctx:YAPLParser.EqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#not.
    def visitNot(self, ctx:YAPLParser.NotContext):
       return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#isVoid.
    def visitIsVoid(self, ctx:YAPLParser.IsVoidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#function.
    def visitFunction(self, ctx:YAPLParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#lessThan.
    def visitLessThan(self, ctx:YAPLParser.LessThanContext):
       return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#bracket.
    def visitBracket(self, ctx:YAPLParser.BracketContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#true.
    def visitTrue(self, ctx:YAPLParser.TrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#let.
    def visitLet(self, ctx:YAPLParser.LetContext):
        self.SCOPE = self.SCOPE + 1

        for x in range(len(ctx.ID())):
            newVariableIdentifier = str(ctx.ID()[x])
            newVariableType = str(ctx.TYPE()[x])
            
            addition = self.table.AddAttribute(
                Attribute(
                    newVariableIdentifier,
                    newVariableType,
                    self.SCOPE,
                    self.CLASS,
                    self.METHOD_NO
                )
            )

            if not addition:
                self.errors.append(
                    Error(
                        "NameError",
                        ctx.ID().getPayload().line,
                        "variable " + newVariableIdentifier + " has already been defined in current scope"
                    )
                )
                return "Error"

        self.SCOPE = self.SCOPE - 1
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#divide.
    def visitDivide(self, ctx:YAPLParser.DivideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#id.
    def visitId(self, ctx:YAPLParser.IdContext):
       return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#lessEqual.
    def visitLessEqual(self, ctx:YAPLParser.LessEqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#multiply.
    def visitMultiply(self, ctx:YAPLParser.MultiplyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#ifElse.
    def visitIfElse(self, ctx:YAPLParser.IfElseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#substract.
    def visitSubstract(self, ctx:YAPLParser.SubstractContext):
        return self.visitChildren(ctx)




del YAPLParser