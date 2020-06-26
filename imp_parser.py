from imp_lexer import *
from combinators import *
from imp_ast import *
from functools import reduce

# RESERVED
def keyword(kw):
    return Reserved(kw, RESERVED)
# INT
num = Tag(INT) ^ (lambda i: int(i))
# ID
id = Tag(ID)

# 
def imp_parse(tokens):
    ast = parser()(tokens, 0)
    return ast

def parser():
    return Phrase(stmt_list())    

# Утверждения
def stmt():
    return assign_stmt() | \
           if_stmt()     | \
           while_stmt()
# ';'
def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)

# Присвоение
def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return id + keyword(':=') + aexp() ^ process

# Условие
def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)
    return keyword('if') + bexp() + \
           keyword('then') + Lazy(stmt_list) + \
           Opt(keyword('else') + Lazy(stmt_list)) + \
           keyword('end') ^ process

# Цикл
def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)
    return keyword('while') + bexp() + \
           keyword('do') + Lazy(stmt_list) + \
           keyword('end') ^ process

# Логические выражения
def bexp():
    return precedence(bexp_term(),
                      bexp_precedence_levels,
                      process_logic)
# самостоятельное выражение
def bexp_term():
    return bexp_not()   | \
           bexp_relop() | \
           bexp_group()
# отрицание
def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))
# отношение
def bexp_relop():
    relops = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop
# группировка в скобки
def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group

# Арифметические выражения
def aexp():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)
# простое самостоятельное выражение
def aexp_term():
    return aexp_value() | aexp_group()
# группировка выражений в скобки
def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group
# значение 
def aexp_value():
    return (num ^ (lambda i: IntAexp(i))) | \
           (id  ^ (lambda v: VarAexp(v)))

# для бинарных операторов выражений (арифметических и логических)
def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser

# Функции для бинарных операторов и отношений
def process_binop(op):
    return lambda l, r: BinopAexp(op, l, r)

def process_relop(parsed):
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)

def process_logic(op):
    if op == 'and':
        return lambda l, r: AndBexp(l, r)
    elif op == 'or':
        return lambda l, r: OrBexp(l, r)
    else:
        raise RuntimeError('неизвестный логический оператор: ' + op)
#
def process_group(parsed):
    ((_, p), _) = parsed
    return p

def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

# Приоритет операций:
#   арифметических
aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]
#   логических
bexp_precedence_levels = [
    ['and'],
    ['or'],
]
