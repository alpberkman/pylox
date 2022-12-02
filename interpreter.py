from tokenType import TokenType
from environment import Environment

class Interpreter():
    def __init__(self, lox):
        self.lox = lox
        self.environment = environment.Environment()

    def visitLiteralExpr(self, expr):
        return expr.value

    def visitGroupingExpr(self, expr):
        return self.evaluate(expr.expression)

    def evaluate(self, expr):
        return expr.accept(self)

    def visitUnaryExpr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.checkNumberOperand(expr.operator, right)
            return -right
        elif expr.operator.type == TokenType.BANG:
            return not self.isTruthy(right)
        else:
            return None

    def visitBinaryExpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.checkNumberOperands(expr.operator, left, right)
            return left - right
        elif expr.operator.type == TokenType.SLASH:
            self.checkNumberOperands(expr.operator, left, right)
            return left / right
        elif expr.operator.type == TokenType.STAR:
            self.checkNumberOperands(expr.operator, left, right)
            return left * right
        elif expr.operator.type == TokenType.PLUS:
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            elif isinstance(left, (float, int)) and isinstance(right, (float, int)):
                return left + right
            else:
                raise LoxRuntimeError(
                    expr.operator, "Operands must be two numbers or two strings.")
                return None
        elif expr.operator.type == TokenType.GREATER:
            self.checkNumberOperands(expr.operator, left, right)
            return left > right
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return left >= right
        elif expr.operator.type == TokenType.LESS:
            self.checkNumberOperands(expr.operator, left, right)
            return left < right
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return left <= right
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self.isEqual(left, right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)
        else:
            return None

    def isTruthy(self, object):
        if object == None:
            return False
        elif isinstance(object, (float, int)):
            return True
        elif isinstance(object, bool):
            return object
        else:
            return True

    def isEqual(self, a, b):
        if a == None and b == None:
            return True
        elif a == b:
            return True
        else:
            return False

    def checkNumberOperand(self, operator, operand):
        if isinstance(operand, (float, int)):
            return
        else:
            raise LoxRuntimeError(operator, "Operand must be a number.")

    def checkNumberOperands(self, operator, left, right):
        if isinstance(left, (float, int)) and isinstance(right, (float, int)):
            return
        else:
            raise LoxRuntimeError(operator, "Operands must be numbers.")

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as error:
            self.lox.runtimeError(error)

    def stringify(self, object):
        if object == None:
            return "nil"
        elif isinstance(object, (float, int)):
            text = str(object)
            if text[-2:] == ".0":
                text = text[:-2]
            return text
        return str(object)

    def visitExpressionStmt(self, stmt):
        value = self.evaluate(stmt.expression)
        return None

    def visitPrintStmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def execute(self, stmt):
        stmt.accept(self)
    
    def visitVarStmt(self, stmt):
        value = None
        if stmt.initializer != None:
            value = self.evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def visitVariableExpr(self, expr):
        return self.environment.get(expr.name)

    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.value)
        return value

























