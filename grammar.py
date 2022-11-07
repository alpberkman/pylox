

class Expr:
	pass
	

class Binary(Expr):
	def __init__(self, left, operator, right):
		self.left = left
		self.operator = operator
		self.right = right
		
	def accept(self, visitor):
		return visitor.visitBinary(self)
		
		
class Grouping(Expr):
	def __init__(self, expression):
		self.expression = expression
		
	def accept(self, visitor):
		return visitor.visitGrouping(self)
		
		
class Literal(Expr):
	def __init__(self, value):
		self.value = value
		
	def accept(self, visitor):
		return visitor.visitLiteral(self)
		
		
class Unary(Expr):
	def __init__(self, operator, right):
		self.operator = operator
		self.right = right
		
	def accept(self, visitor):
		return visitor.visitUnary(self)
		
		