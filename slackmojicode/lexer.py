
from rply import LexerGenerator
try:
    import rpython.rlib.rsre.rsre_re as re
except:
    import re

lg = LexerGenerator()

# build up a set of token names and regexes they match
lg.add('FLOAT', '-?\d+\.\d+')
lg.add('INTEGER', '-?\d+')
lg.add('STRING', '(""".*?""")|(".*?")|(\'.*?\')')
lg.add('PRINT',        ':c_print:(?!\w)')
lg.add('BOOLEAN',      ":c_true:(?!\w)|:c_false:(?!\w)")
lg.add('IF',           ':c_if:(?!\w)')
lg.add('ELSE',         ':c_else:(?!\w)')
lg.add('END',          ':c_end:(?!\w)')
lg.add('AND',          ":c_and:(?!\w)")
lg.add('OR',           ":c_or:(?!\w)")
lg.add('NOT',          ":c_not:(?!\w)")
lg.add('FOR',          ':c_for:(?!\w)')
lg.add('WHILE',        ':c_while:(?!\w)')
lg.add('BREAK',        ':c_break:(?!\w)')
lg.add('CONTINUE',     ':c_continue:(?!\w)')
lg.add('RETURN',       ':c_return:(?!\w)')
lg.add('FUNCTION',     ':c_func:(?!\w)')
lg.add('IDENTIFIER',   "[a-zA-Z_][a-zA-Z0-9_:]*")
lg.add('PLUS',         ':c_add:')
lg.add('==',           ':c_equal:')
lg.add('!=',           ':c_not_equal:')
lg.add('>=',           ':c_ge:')
lg.add('<=',           ':c_le:')
lg.add('>',            ':c_gt:')
lg.add('<',            ':c_lt:')
lg.add('=',            ':c_def:')
lg.add('[',            ':c_list_b:')
lg.add(']',            ':c_list_e:')
lg.add(',',            ',')
lg.add('DOT',          '\.')
lg.add('COLON',        ':c_colon:')
lg.add('MINUS',        ':c_sub:')
lg.add('MUL',          ':c_mul:')
lg.add('DIV',          ':c_div')
lg.add('MOD',          ':c_mod:')
lg.add('(',            ':c_par_b:')
lg.add(')',            ':c_par_e:')
lg.add('NEWLINE', '\n')

# ignore whitespace
lg.ignore('[ \t\r\f\v]+')

lexer = lg.build()

def lex(source):

    comments = r'(#.*)(?:\n|\Z)'
    multiline = r'([\s]+)(?:\n)'
    
    comment = re.search(comments,source)
    while comment is not None:
        start, end = comment.span(1)
        assert start >= 0 and end >= 0
        source = source[0:start] + source[end:] #remove string part that was a comment
        comment = re.search(comments,source)

    line = re.search(multiline,source)
    while line is not None:
        start, end = line.span(1)
        assert start >= 0 and end >= 0
        source = source[0:start] + source[end:] #remove string part that was an empty line
        line = re.search(multiline,source)

    #print "source is now: %s" % source

    return lexer.lex(source)
