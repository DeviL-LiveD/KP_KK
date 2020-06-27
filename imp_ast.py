from equality import *

# Арифметическое выражение
class Aexp(Equality):
    pass

# константы
class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'IntAexp(%d)' % self.i

# переменные
class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VarAexp(%s)' % self.name

# бинарные операции
class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.op, self.left, self.right)

# Логическое выражение
class Bexp(Equality):
    pass

# отношения
class RelopBexp(Bexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'RelopBexp(%s, %s, %s)' % (self.op, self.left, self.right)

# And
class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'AndBexp(%s, %s)' % (self.left, self.right)

# Or
class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'OrBexp(%s, %s)' % (self.left, self.right)

# Not
class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'NotBexp(%s)' % self.exp

# Утверждения
class Statement(Equality):
    pass

# присвоение
class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp
    ''''''
    def __repr__(self):
        return 'AssignStatement(%s, %s)' % (self.name, self.aexp)

# соединение
class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second
    ''''''
    def __repr__(self):
        return 'CompoundStatement(%s, %s)' % (self.first, self.second)

# условие
class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt
    ''''''
    def __repr__(self):
        return 'IfStatement(%s, %s, %s)' % (self.condition, self.true_stmt, self.false_stmt)

# цикл
class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    ''''''
    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)
