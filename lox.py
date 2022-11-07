#!/usr/bin/env python3

import sys
from scanner import Scanner
from parser import Parser
from astPrinter import AstPrinter

class Lox:
	def __init__(self):
		self.hadError = False
		
	def runFile(self, path):
		file = open(path, "r")
		source = file.read()
		file.close()
	
		self.run(source)
		if self.had_error:
			sys.exit(65)
	
	def runPrompt(self):
		while True:
			try:
				line = input("> ")
				self.run(line)
				self.hadError = False
			except EOFError:
				break;

	def run(self, source):
		scanner = Scanner(source, self)
		tokens = scanner.scanTokens()
		parser = Parser(tokens, self)
		expression = parser.parse()
		
		if self.hadError:
			return
		
		print(AstPrinter().print(expression))
	
		
	def error(self, line, message):
		self.report(line, "", message)
	
	def report(self, line, where, message):
		print("[line ", line, "] Error", where, ": ", message, file=sys.stderr, sep = "")
		self.hadError = True


if __name__ == "__main__":
	l = Lox()
	if len(sys.argv) > 2:
		sys.exit(64)
	elif len(sys.argv) == 2:
		l.runFile(sys.argv[1])
	else:
		l.runPrompt()


