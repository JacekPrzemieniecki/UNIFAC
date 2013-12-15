'''
Created on 12-10-2012

@author: Jacek Przemieniecki
'''
from ..ply import lex, yacc

tokens = ("AROMATIC_CARBON",
          "ATOM",
          "HALOGEN",
          "HYDROGEN",
          "NUMBER",
          "DOUBLE_BOND",
          "TRIPLE_BOND",
          "LPAREN",
          "RPAREN"
          )

def t_AROMATIC_CARBON(t):
    r"AC"
    return t

# Br and I are separate groups, Cl and F are not.
# Therefore. there is no Br2, I3 etc in group strings
def t_HALOGEN(t):
    r"Cl|F"
    return t

def t_ATOM(t):
    r"C|N|O|Si|S|Br|I"
    return t

def t_error(t):
    raise Exception(t) # TODO: Exception handling

t_HYDROGEN = r"H"
t_NUMBER = r"\d"
t_DOUBLE_BOND = r"\="
t_TRIPLE_BOND = r"\#"
t_LPAREN = r"\("
t_RPAREN = r"\)"

lexer = lex.lex()

start = "node"

def p_node(p):
    r"node : group nextnode"
    p[0] = ("node", p[1], p[2])

def p_nextnode(p):
    r"nextnode : optbond node"
    p[0] = ("next", p[1], p[2])
    
def p_nextnode_empty(p):
    r"nextnode : "
    p[0] = None

def p_optbond(p):
    r"""optbond : DOUBLE_BOND
                | TRIPLE_BOND"""
    p[0] = 2 if p[1] == "=" else 3
    
def p_optbond_empty(p):
    r"optbond : "
    p[0] = 1

def p_group_symbol(p):
    r"group : symbol"
    p[0] = p[1]

def p_group_extended(p):
    r"group : symbol extention"
    p[0] = ("ext-atom", p[1], p[2])

def p_symbol_atom(p):
    r"symbol : ATOM"
    p[0] = ("atom", p[1])

def p_symbol_aromatic_carbon(p):
    r"symbol : AROMATIC_CARBON"
    p[0] = ("aromatic-atom", "C")

def p_extention_more(p):
    r"extention : extention extention"
    p[0] = p[1] + p[2]

def p_extention_subgroup_in_paren(p):
    r"extention : LPAREN nextnode RPAREN"
    p[0] = [p[2]]

def p_extention_halogen(p):
    r"extention : HALOGEN optnum"
    if not p[2]:
        p[2] = 1
    p[0] = [("halogen", p[1], p[2])]
    
def p_extention_hydrogen(p):
    r"extention : HYDROGEN optnum"
    if p[2] is None:
        p[2] = 1
    p[0] = [("hydrogen", p[2])]

def p_optnum(p):
    r"optnum : NUMBER"
    p[0] = int(p[1])
    
def p_optnum_empty(p):
    r"optnum : "
    p[0] = None

def p_error(p):
    raise Exception(p) # TODO: Exception handling
parser = yacc.yacc(tabmodule="group_parsetab")

def parse(group_string):
    return parser.parse(group_string, lexer=lexer)
