from rply import ParserGenerator
from rply.token import BaseBox
import lexer

# state instance which gets passed to parser
class ParserState(object):
    def __init__(self):
        # we want to hold a dict of declared variables
        self.variables = {}

# all token types inherit rply's basebox as rpython needs this
# these classes represent our Abstract Syntax Tree
class Integer(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

class Float(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value
    
class Variable(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()

class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()

class Mul(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()

class Div(BinaryOp):
    def eval(self):
        return self.left.eval() / self.right.eval()

class Variable(BaseBox):
    def __init__(self, value):
        self.value = value
        
    def eval(self):
        return self.value

pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    ['PRINT', 'INTEGER', 'FLOAT', 'VARIABLE', 'OPEN_PARENS', 'CLOSE_PARENS',
     'PLUS', 'MINUS', 'MUL', 'DIV', 'EQUALS', 
    ],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV'])
    ]
)

# this decorator defines the grammar to be matched and passed in as 'p'
@pg.production('statement : PRINT OPEN_PARENS expression CLOSE_PARENS')
def statement_print(state, p):
    print p[2].eval()
    return p[2]

@pg.production('statement : VARIABLE EQUALS expression')
def statement_assignment(state, p):
    # only assign value if variable is not yet defined - immutable values
    if state.variables.get(p[0].getstr(), None) is None:
        state.variables[p[0].getstr()] = p[2].eval()
        return p[2]
    
    # otherwise raise error
    raise ValueError("Cannot modify value of %s" % p[0].getstr())
    

@pg.production('statement : expression')
def statement_expr(state, p):
    return p[0]

@pg.production('const : FLOAT')
def expression_float(state, p):
    # p is a list of the pieces matched by the right hand side of the rule
    return Float(float(p[0].getstr()))

@pg.production('const : INTEGER')
def expression_integer(state, p):
    return Integer(int(p[0].getstr()))

@pg.production('expression : const')
def expression_const(state, p):
    return p[0]

@pg.production('expression : VARIABLE')
def expression_variable(state, p):
    # cannot return the value of a variable if it isn't yet defined
    if state.variables.get(p[0].getstr(), None) is None:
        raise ValueError("%s is not yet defined" % (p[0].getstr()))
    # otherwise return value from state
    return Variable(state.variables[p[0].getstr()])

@pg.production('expression : OPEN_PARENS expression CLOSE_PARENS')
def expression_parens(state, p):
    # in this case we need parens only for precedence
    # so we just need to return the inner expression
    return p[1]

@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')
def expression_binop(state, p):
    left = p[0]
    right = p[2]
    if p[1].gettokentype() == 'PLUS':
        return Add(left, right)
    elif p[1].gettokentype() == 'MINUS':
        return Sub(left, right)
    elif p[1].gettokentype() == 'MUL':
        return Mul(left, right)
    elif p[1].gettokentype() == 'DIV':
        return Div(left, right)
    else:
        raise AssertionError('Oops, this should not be possible!')

@pg.error
def error_handler(state, token):
    # we print our state for debugging porpoises
    print state.variables
    raise ValueError("Unexpected %s at %s" % (token.gettokentype(), token.getsourcepos()))

parser = pg.build()
state = ParserState()
state.variables['version'] = '0.0.0' # special value under 'version'

def parse(code):
    return parser.parse(lexer.lex(code),state)
