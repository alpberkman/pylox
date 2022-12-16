from tokenType import TokenType
from environment import Environment
from error import LoxRuntimeError


class Interpreter():
    def __init__(self, lox):
        self.lox = lox
        self.environment = Environment()

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
        if object is None or object is False:
            return False
        else:
            return True
        ## Literal same as the builtin bool() function
        #if object is None:
        #    return False
        #elif isinstance(object, (float, int)):
        #    return True
        ## this line should be before the float/int line because bool is an instance of if and it will evaluate
        #elif isinstance(object, bool): to true even if it is False
        #    return object
        #else:
        #    return True

    def isEqual(self, a, b):
        if a is None and b is None:
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
        if object is None:
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
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitVariableExpr(self, expr):
        return self.environment.get(expr.name)

    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    
    def visitBlockStmt(self, stmt):
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None
    
    def executeBlock(self, statements, environment):
        previous = self.environment
        
        try:
            self.environment = environment
            
            for statement in statements:
                self.execute(statement)
                
        finally:
            self.environment = previous
    
    def visitIfStmt(self, stmt):
        if self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        
        return None
    
    def visitLogicalExpr(self, expr):
        left = self.evaluate(expr.left)
        
        if expr.operator.type == TokenType.OR:
            if self.isTruthy(left):
                return left
        else:
            if not self.isTruthy(left):
                return left
        
        return self.evaluate(expr.right)
    
    def visitWhileStmt(self, stmt):
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        
        return None
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
