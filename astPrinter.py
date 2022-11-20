#!/usr/bin/env python3

from token import Token
from grammar import *
from tokenType import TokenType


class AstPrinter:
	def print(self, expr):
		return expr.accept(self)
		
	def visitBinaryExpr(self, expr):
		return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
	
	def visitGroupingExpr(self, expr):
		return self.parenthesize("group", expr.expression)

	def visitLiteralExpr(self, expr):
		if expr.value == None:
			return "nil"
		else:
			return str(expr.value)

	def visitUnaryExpr(self, expr):
		return self.parenthesize(expr.operator.lexeme, expr.right)

	def parenthesize(self, name, *exprs):
		string = "(" + name

		for expr in exprs:
			string += " "
			string += expr.accept(self)

		string += ")"

		return string


if __name__ == "__main__":
	expression = Binary(
		Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
		Token(TokenType.STAR, "*", None, 1), Grouping(Literal(45.67)))
	print(AstPrinter().print(expression))
	
	
