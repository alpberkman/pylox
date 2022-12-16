from tokenType import TokenType
from expr import *
from stmt import *
from error import LoxParseError


class Parser:
    def __init__(self, tokens, lox):
        self.tokens = tokens
        self.lox = lox
        self.current = 0

    def expression(self):
        return self.assignment()

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
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        elif self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

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
        return self.previous()

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
        self.lox.error(token, message)
        return LoxParseError(token, message)

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
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements
    # try:
    # 	return self.expression()
    # except LoxParseError:
    # 	return None

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.printStatement()
        elif self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        elif self.match(TokenType.IF):
            return self.ifStatement()
        elif self.match(TokenType.WHILE):
            return self.whileStatement()
        elif self.match(TokenType.FOR):
            return self.forStatement()
        else:
            return self.expressionStatement()

    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expressionStatement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Expression(expr)

    def varDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON,
                     "Expect ';' after variable declaration.")

        return Var(name, initializer)

    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            else:
                return self.statement()
        except LoxParseError as error:
            self.synchronize()
            return None

    def assignment(self):
        expr = self.or_expr()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            self.lox.error2(equals, "Invalid assignment target.")

        return expr
    
    def block(self):
        statements = []
        
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())
        
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements
    
    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        
        thenBrach = self.statement()
        elseBranch = None
        if self.match(TokenType.ELSE):
            elseBranch = self.statement()
        
        return If(condition, thenBrach, elseBranch)
    
    def or_expr(self):
        expr = self.and_expr()
        
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_expr()
            expr = Logical(expr, operator, right)
        
        return expr
    
    def and_expr(self):
        expr = self.equality()
        
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        
        return expr
    
    def whileStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        
        return While(condition, body)
    

    
    def forStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        
        initializer = None
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()
        
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
        
        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
        body = self.statement()
        
        if increment is not None:
            body = Block([body, Expression(increment)])
        
        if condition is None:
            condition = Literal(True)
        
        body = While(condition, body)
        
        if initializer is not None:
            body = Block([initializer, body])
        
        return body
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
