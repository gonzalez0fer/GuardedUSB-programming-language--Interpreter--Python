#!/usr/bin/env python

#######################################
# CI3715 Traductores e Interpretadores
# Entrega 2. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################
import ply.yacc as yacc
from g_lexer import *
from g_AbsSyntaxTree import *

import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

# De aqui en adelante escribimos las reglas que definiran la gramatica
# de nuestro lenguaje para filtrar errores sintacticos y construir 
# nuestro arbol sintactico abstracto.

# Reglas de precedencia para el parser        
precedence = (
	('nonassoc', 'TkGreater', 'TkLess', 'TkGeq', 'TkLeq'),
	('left', 'TkPlus', 'TkMinus'),
	('left', 'TkMult', 'TkDiv', 'TkMod'),
	('right', 'uminus'),
	('left', 'TkConcat'),
	('left', 'TkOBracket', 'TkCBracket'),
	('left', 'TkOpenPar', 'TkClosePar'),
	('left', 'TkEqual', 'TkNEqual'),
	('left', 'TkAnd', 'TkOr'),
	('right', 'TkNot'),
	('nonassoc', 'TkNum', 'TkId')
)


def p_program(p):
    ''' Block   :   TkOBlock Content TkCBlock
                |   TkOBlock TkDeclare Declaration TkSemicolon Content TkCBlock
                |   TkOBlock TkDeclare Declaration TkSemicolon TkCBlock
    '''


def p_declaration(p):
    ''' Declaration :   Variables TkTwoPoints TkInt 
                    |   Variables TkTwoPoints TkBool
                    |   Variables TkTwoPoints Array
                    |   Variables TkTwoPoints TkInt Declaration
                    |   Variables TkTwoPoints TkBool Declaration
                    |   Variables TkTwoPoints Array Declaration
    '''


def p_array(p):
    ''' Array   :   TkArray TkOBracket Terminal TkSoForth Terminal TkCBracket
                |   TkArray TkOBracket AritmeticOperator TkSoForth AritmeticOperator TkCBracket
    '''
def p_terminal(p):
	'''
	Terminal :  TkId
			  | TkString
			  | TkNum
			  | TkTrue
			  | TkFalse
              | TkQuote
			  | TkOpenPar Terminal TkClosePar
	'''

def p_content(p):
	''' Content :   Instruction
                |   Instruction Content
                |   Block Content
                |   Block
	'''


def p_instruction(p):
    ''' Instruction :   Expression TkSemicolon
                    |   Conditional
                    |   Forloop
                    |   Doloop
                    |   Asign TkSemicolon
                    |   Input TkSemicolon
                    |   Output TkSemicolon
    '''

def p_conditional(p):
    ''' Conditional :   TkIf Expression TkArrow Content TkFi
                    |   TkIf Expression TkArrow Content Guard TkFi
    '''

def p_guard(p):
    ''' Guard   :   TkGuard Expression TkArrow Content
                |   TkGuard Expression TkArrow Content Guard
    '''

def p_asign(p):
    ''' Asign    :   TkId TkAsig Expression TkSemicolon
    '''

def p_input(p):
	''' Input   :   TkRead TkId
	'''

def p_output(p):
	'''Output   :   TkPrint TkQuote Expression TkQuote
                |   TkPrintln TkQuote Expression TkQuote
	'''

def p_doloop(p):
    ''' Doloop :   TkDo RelationalOperator TkArrow Content TkOd
                |   TkDo BooleanOperator TkArrow Content TkOd 
    '''

def p_forloop(p):
    ''' Forloop : TkFor TkId TkIn AritmeticOperator TkTo AritmeticOperator TkArrow Content TkRof
                | TkFor TkId TkIn AritmeticOperator TkTo Terminal TkArrow Content TkRof
                | TkFor TkId TkIn Terminal TkTo AritmeticOperator TkArrow Content TkRof
                | TkFor TkId TkIn Terminal TkTo Terminal TkArrow Content TkRof
    ''' 

def p_expression(p):
    ''' Expression  :   AritmeticOperator
                    |   Terminal
                    |   RelationalOperator
                    |   BooleanOperator
                    |   StrOperator
                    |   ArrayOperator
    '''
def p_aritmoper(p):
	''' AritmeticOperator : Expression TkMinus Expression
                    |   Expression TkPlus Expression
                    |   Expression TkDiv Expression
                    |   Expression TkMult Expression
                    |   Expression TkMod Expression
                    |   TkOpenPar Expression TkMinus Expression TkClosePar
                    |   TkOpenPar Expression TkPlus Expression TkClosePar
                    |   TkOpenPar Expression TkDiv Expression TkClosePar
                    |   TkOpenPar Expression TkMult Expression TkClosePar
                    |   TkOpenPar Expression TkMod Expression TkClosePar
                    |   TkMinus Expression %prec uminus
                    |   TkOpenPar TkMinus Expression TkClosePar %prec uminus
    '''

def p_Stroper(p):
	''' StrOperator : TkId TkConcat TkId
                | TkOpenPar TkId TkConcat TkId TkClosePar

    '''

def p_arrayoper(p):
    ''' ArrayOperator   :   TkSize TkOpenPar TkId TkClosePar
                    | TkMax TkOpenPar TkId TkClosePar
                    | TkMin TkOpenPar TkId TkClosePar
                    | TkAtoi TkOpenPar TkId TkClosePar
                    | TkSize TkOpenPar Array TkClosePar
                    | TkMax TkOpenPar Array TkClosePar
                    | TkMin TkOpenPar Array TkClosePar
                    | TkAtoi TkOpenPar Array TkClosePar
    '''


def p_opRel(p):
	'''RelationalOperator : Expression TkLess Expression
                |   Expression TkLeq Expression
                |   Expression TkGreater Expression
                |   Expression TkGeq Expression
                |   Expression TkEqual Expression
                |   Expression TkNEqual Expression
                |   TkOpenPar Expression TkGreater Expression TkClosePar
                |   TkOpenPar Expression TkGeq Expression TkClosePar
                |   TkOpenPar Expression TkLess Expression TkClosePar
                |   TkOpenPar Expression TkLeq Expression TkClosePar
                |   TkOpenPar Expression TkEqual Expression TkClosePar
                |   TkOpenPar Expression TkNEqual Expression TkClosePar
	'''

def p_variables(p):
	''' Variables : TkId TkComma Variables
                | TkId TkAsig Expression TkComma Variables
                | TkId 
                | TkId TkAsig Expression
	'''

def p_boolop(p):
	'''BooleanOperator : Expression TkAnd Expression
                |   Expression TkOr Expression
                |   TkOpenPar Expression TkAnd Expression TkClosePar
                |   TkOpenPar Expression TkOr Expression TkClosePar
                |   TkNot Expression
                |   TkOpenPar TkNot Expression TkClosePar
	'''



def p_error(p):
    global parser_error
    if (p is not None):
        msg = "[Syntax Error] Wrong token found: '" + str(p.value) + "' in line "
        msg += str(p.lineno) + ", column " + str(find_column(p.lexer.lexdata,p))
    else:
        msg = "[Syntax Error] at end of file."
    print (msg)
    parser_error = True

# Variable global del primer error del parser si existe.
global parser_error
parser_error = False

# Funcion que se encarga de construir el parser.
def parser_builder(meta_program):
    parser = yacc.yacc(debug=True)
    log = logging.getLogger()
    out = parser.parse(meta_program, debug=log)

    if not(parser_error):
        return (out)