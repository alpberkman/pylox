#!/usr/bin/env python3

import sys
from scanner import Scanner
from parser import Parser
from astPrinter import AstPrinter
from interpreter import Interpreter


class Lox:
    def __init__(self):
        self.hadError = False
        self.hadRuntimeError = False

    def runFile(self, path):
        file = open(path, "r")
        source = file.read()
        file.close()

        self.run(source)
        if self.hadError:
            sys.exit(65)
        elif self.hadRuntimeError:
            sys.exit(70)

    def runPrompt(self):
        while True:
            try:
                line = input("> ")
                self.run(line)
                self.hadError = False
            except EOFError as error:
                break

    def run(self, source):
        scanner = Scanner(source, self)
        tokens = scanner.scanTokens()

        parser = Parser(tokens, self)
        statements = parser.parse()

        if self.hadError:
            return
        # print(AstPrinter().print(expression))
        # return
        interpreter = Interpreter(self)
        interpreter.interpret(statements)

    def error(self, line, message):
        self.report(line, "", message)

    def error2(self, token, message):
        if token.type == TokenType.EOF:
            self.report(token.line, "at end", message)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", message)

    def report(self, line, where, message):
        print("[line ", line, "] Error", where,
              ": ", message, file=sys.stderr, sep="")
        self.hadError = True

    def runtimeError(error):
        print(error.message + "\n[line " +
              error.token.line + "]", file=sys.stderr)
        self.hadRuntimeError = true


if __name__ == "__main__":
    l = Lox()
    if len(sys.argv) > 2:
        sys.exit(64)
    elif len(sys.argv) == 2:
        l.runFile(sys.argv[1])
    else:
        l.runPrompt()
