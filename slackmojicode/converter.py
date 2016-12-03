from collections import OrderedDict

token_dict = OrderedDict([
    (':',     ' :c_colon: '),
    ('print', ' :c_print: '),
    ('true',  ' :c_true: '),
    ('false', ' :c_false: '),
    ('if',    ' :c_if: '),
    ('else',  ' :c_else: '),
    ('end',   ' :c_end: '),
    ('and',   ' :c_and: '),
    ('or',    ' :c_or: '),
    ('not',   ' :c_not: '),
    ('while', ' :c_while: '),
    ('func',  ' :c_func: '),
    ('+',     ' :c_add: '),
    ('==',    ' :c_eq: '),
    ('!=',    ' :c_neq: '),
    ('>=',    ' :c_ge: '),
    ('<=',    ' :c_le: '),
    ('>',     ' :c_gt: '),
    ('<',     ' :c_lt: '),
    ('=',     ' :c_def: '),
    ('[',     ' :c_list_b: '),
    (']',     ' :c_list_e: '),
    ('-',     ' :c_sub: '),
    ('*',     ' :c_mul: '),
    ('/',     ' :c_div'),
    ('%',     ' :c_mod: '),
    ('(',     ' :c_par_b: '),
    (')',     ' :c_par_e: ')])


def convert(source):
    for t_from, t_to in token_dict.iteritems():
        source = source.replace(t_from, t_to)
    return source
