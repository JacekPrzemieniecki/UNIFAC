'''
Created on 13-10-2012

@author: Jacek Przemieniecki
'''

from ..ply import lex, yacc

tokens = ("AROMATIC_SYMBOL",
          "BOND",
          "DIGIT",
          "ELEMENT_SYMBOL",
          "HYDROGEN",
          "LPAREN",
          "RPAREN",
          "LSPAREN",
          "RSPAREN"
          )

t_AROMATIC_SYMBOL = r"c|n|s|o|p"
t_BOND = r"\-|\=|\#|\$|\:|\/|\\"
t_DIGIT = r"\d"
t_ELEMENT_SYMBOL = r"C|N|O|F|Cl|Br|I|Si|S"  # parsing only elements supported be UNIFAC
t_HYDROGEN = r"H"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LSPAREN = r"\["
t_RSPAREN = r"\]"

def t_error(t):
    raise Exception(t)      # TODO: Exception handling

lexer = lex.lex()

start = "chain"

def p_chain(p):
    r"chain : branched_atom"
    p[0] = p[1]

def p_chain_more(p):
    r"chain : chain branched_atom"
    p[0] = p[1] + p[2]

def p_chain_bond(p):
    r"chain : chain bond branched_atom"
    p[0] = p[1] + [p[2]] + p[3]

def p_branched_atom(p):
    r"branched_atom : atom optringbond optbranch"
    p[0] = [("branched", p[1],  p[2],  p[3])]
    
def p_optringbond(p):
    r"optringbond : ringbond optringbond"
    p[0] = [p[1]] + p[2]

def p_optringbond_empty(p):
    r"optringbond : "
    p[0] = []

#def p_ringbond(p):        # TODO: This causes syntax errors while parsing chains with multiple bonds
#    r"ringbond : bond DIGIT"
#    p[0] = ("ringbond", p[1], int(p[2]))

def p_ringbond_single_bond(p):
    r"ringbond : DIGIT"
    p[0] = ("ringbond", ("bond", 1), 1)
    
def p_optbranch(p):
    r"optbranch : branch optbranch"
    p[0] = [p[1]] + p[2]

def p_optbranch_empty(p):
    r"optbranch : "
    p[0] = []
    
def p_branch(p):
    r"branch : LPAREN chain RPAREN"
    p[0] = ("branch", ("bond", 1), p[2])

def p_branch_explicit_bond(p):
    r"branch : LPAREN bond chain RPAREN"
    p[0] = ("branch", p[2], p[3])
    
def p_atom(p):
    r"""atom : bracket_atom
             | aliphatic_organic
             | aromatic_organic"""
    p[0] = p[1]

bond_type = {"-" : 1,
             "=" : 2,
             "#" : 3,
             "$" : 4,
             "/" : 1,
             "\\" : 1,
             }

def p_bond(p):
    r"bond : BOND"
    p[0] = ("bond", bond_type[p[1]])
    
def p_symbol(p):
    r"""symbol : aliphatic_organic
             | aromatic_organic"""
    p[0] = p[1]

def p_aliphatic_organic(p):
    r"aliphatic_organic : ELEMENT_SYMBOL"
    p[0] = ("atom", p[1])

def p_aromatic_organic(p):
    r"aromatic_organic : AROMATIC_SYMBOL"
    p[0] = ("aromatic", p[1].upper())
    
def p_bracket_atom(p):
    r"bracket_atom : LSPAREN symbol RSPAREN"
    p[0] = ("atom", p[2])
    
def p_bracket_atom_hcount(p):
    r"bracket_atom : LSPAREN symbol hcount RSPAREN"
    p[0] = ("atom-hcount", p[2], int(p[3]))

def p_hcount(p):
    r"""hcount : HYDROGEN
               | HYDROGEN DIGIT"""
    if not p[2]:
        p[2] = 1
    p[0] = ("hydrogen", p[2])

def p_error(p):
    raise Exception(p)      # TODO: Exception handling

parser = yacc.yacc(tabmodule="smiles_parsetab")

def parse(string):
    return parser.parse(string, lexer=lexer)