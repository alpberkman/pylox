#!/usr/bin/env python3

import sys
from scanner import Scanner


class Lox:
	def __self__(self):
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
	
		for token in tokens:
			print(token)
		
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


