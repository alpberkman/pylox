from tokenType import TokenType
from grammar import *
from error import ParseError

class Parser:
	def __init__(self, tokens, interpreter):
		self.tokens = tokens
		self.interpreter = interpreter
		self.current = 0
		
	def expression(self):
		return self.equality()
		
	def equality(self):
		expr = self.comparison()
		
		while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
			operator = self.previous()
			right = self.comparison()
			expr = Binary(expr, operator, right)
		
		return expr
	
	def comparison(self):
		expr = self.term()
		
		while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
			operator = self.previous()
			right = self.term()
			expr = Binary(expr, operator, right)
		
		return expr
	
	def term(self):
		expr = self.factor()
		
		while self.match(TokenType.MINUS, TokenType.PLUS):
			operator = self.previous()
			right = self.factor()
			expr = Binary(expr, operator, right)
		
		return expr
	
	def factor(self):
		expr = self.unary()
		
		while self.match(TokenType.SLASH, TokenType.STAR):
			operator = self.previous()
			right = self.unary()
			expr = Binary(expr, operator, right)
		
		return expr
	
	def unary(self):
		if self.match(TokenType.BANG, TokenType.MINUS):
			operator = self.previous()
			right = self.unary()
			return Unary(operator, right)
		else:
			return self.primary()
	
	def primary(self):
		if self.match(TokenType.FALSE):
			return Literal(False)
		elif self.match(TokenType.TRUE):
			return Literal(True)
		elif self.match(TokenType.NIL):
			return Literal(None)
		elif self.match(TokenType.NUMBER, TokenType.STRING):
			return Literal(self.previous().literal)
		elif self.match(TokenType.LEFT_PAREN):
			expr = self.expression()
			self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.");
			return Grouping(expr)
		
		raise self.error(self.peek(), "Expect expression.")
	
	def match(self, *types):
		for type in types:
			if self.check(type):
				self.advance()
				return True
		
		return False
	
	def check(self, type):
		if self.isAtEnd():
			return False
		else:
			return self.peek().type == type
	
	def advance(self):
		if not self.isAtEnd():
			self.current += 1
		else:
			return self.previous
	
	def isAtEnd(self):
		return self.peek().type == TokenType.EOF
	
	def peek(self):
		return self.tokens[self.current]
		
	def previous(self):
		return self.tokens[self.current - 1]
	
	def consume(self, type, message):
		if self.check(type):
			return self.advance()
		else:
			raise self.error(self.peek(), message)
	
	def error(self, token, message):
		if token.type == TokenType.EOF:
			self.interpreter.report(token.line, "at end", message)
		else:
			self.interpreter.report(token.line, " at '" + token.lexeme + "'", message)
			
		return ParseError(token, message)
	
	def synchronize(self):
		self.advance()
		
		while not self.isAtEnd():
			if self.previous().type == TokenType.SEMICOLON:
				return
			
			if self.peek().type == TokenType.CLASS:
				return
			elif self.peek().type == TokenType.FUN:
				return
			elif self.peek().type == TokenType.VAR:
				return
			elif self.peek().type == TokenType.FOR:
				return
			elif self.peek().type == TokenType.IF:
				return
			elif self.peek().type == TokenType.WHILE:
				return
			elif self.peek().type == TokenType.PRINT:
				return
			elif self.peek().type == TokenType.RETURN:
				return
			
			self.advance()
	
	def parse(self):
		try:
			return self.expression()
		except ParseError:
			return None
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		
		