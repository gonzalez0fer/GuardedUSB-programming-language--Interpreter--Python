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
    ('left', 'TkAnd', 'TkOr'),
	('nonassoc', 'TkGreater', 'TkLess', 'TkGeq', 'TkLeq'),
	('left', 'TkPlus', 'TkMinus'),
	('left', 'TkMult', 'TkDiv', 'TkMod'),
	('right', 'uminus'),
	('left', 'TkConcat'),
	('left', 'TkOBracket', 'TkCBracket'),
	('left', 'TkOpenPar', 'TkClosePar'),
	('left', 'TkEqual', 'TkNEqual'),
	('right', 'TkNot'),
	('nonassoc', 'TkNum', 'TkId')
)


def p_program(p):
    ''' Block   :   TkOBlock Content TkCBlock
                |   TkOBlock TkDeclare Declaration Content TkCBlock
                |   TkOBlock TkDeclare Declaration TkCBlock
    '''
    if (len(p)==4):
        p[0] = SyntaxLeaf('Block', None, [p[2]])
    elif (len(p)==6):
        p[0] = SyntaxLeaf('Block', None, [p[3],p[4]])
    else:
        p[0] = SyntaxLeaf('Block', None, [p[3]])

   

def p_declaration(p):
    ''' Declaration :   Variables TkTwoPoints Datatype
                    |   Variables TkTwoPoints Datatype TkSemicolon Declaration
    '''
    if (len(p)==4):
        p[0] = SyntaxLeaf('Declare', None, [p[1],p[3]])
    else:
        p[0] = SyntaxLeaf('Declare', None, [p[1],p[3],p[5]])      



def p_array(p):
    ''' Array   :   TkArray TkOBracket Terminal TkSoForth Terminal TkCBracket
                |   TkArray TkOBracket AritmeticOperator TkSoForth AritmeticOperator TkCBracket
    '''
    p[0] = SyntaxLeaf('Array', None, [p[3],p[5]])



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
	if (len(p) == 4):
		p[0] = SyntaxLeaf('Terminal', None, [p[2]])
	else:
		p[0] = SyntaxLeaf('Terminal', p[1])



def p_content(p):
	''' Content :   Instruction
                |   Instruction TkSemicolon Content
                |   Block TkSemicolon Content
                |   Block
	'''
	
	if (len(p) == 2):
		p[0] = SyntaxLeaf('Content', None, [p[1]])
	else:
		p[0] = SyntaxLeaf('Content', None, [p[1], p[3]])
    


def p_instruction(p):
    ''' Instruction :   Conditional
                    |   Forloop
                    |   Doloop
                    |   Asign
                    |   Input
                    |   Output
    '''
    p[0] = SyntaxLeaf('Instruction', None, [p[1]])



def p_conditional(p):
    ''' Conditional :   TkIf RelationalOperator TkArrow Content TkFi
                    |   TkIf BooleanOperator TkArrow Content TkFi
                    |   TkIf RelationalOperator TkArrow Content Guard TkFi
                    |   TkIf BooleanOperator TkArrow Content Guard TkFi
    '''
    if (len(p)==6):
        p[0] = SyntaxLeaf('Conditional', None, [p[2],p[4]])
    else:
        p[0] = SyntaxLeaf('Conditional', None, [p[2],p[4],p[5]])



def p_guard(p):
    ''' Guard   :   TkGuard RelationalOperator TkArrow Content
                |   TkGuard BooleanOperator TkArrow Content
                |   TkGuard RelationalOperator TkArrow Content Guard
                |   TkGuard BooleanOperator TkArrow Content Guard
    '''
    if (len(p)==5):
        p[0] = SyntaxLeaf('Guard', None, [p[2],p[4]])
    else:
        p[0] = SyntaxLeaf('Guard', None, [p[2],p[4],p[5]])




def p_asign(p):
    ''' Asign    :   TkId TkAsig Expression
    '''
    p[0] = SyntaxLeaf('Asign', p[1], [p[3]])



def p_input(p):
    ''' Input   :   TkRead TkId
    '''
    p[0] = SyntaxLeaf('Input', p[1], [p[2]])



def p_output(p):
    '''Output   :   TkPrint Expression
                |   TkPrint Expression ConcatExpression
                |   TkPrintln Expression
                |   TkPrintln Expression ConcatExpression
    '''
    if(len(p)==4):
        p[0] = SyntaxLeaf('Output', None, [p[2],p[3]])
    else:
        p[0] = SyntaxLeaf('Output', None, [p[2]])



def p_concatexp(p):
    ''' ConcatExpression : TkConcat Expression
                        |   TkConcat Expression ConcatExpression
    '''
    if(len(p)==4):
        p[0] = SyntaxLeaf('ConcatExpression', None, [p[2],p[3]])
    else:
        p[0] = SyntaxLeaf('ConcatExpression', None, [p[2]])



def p_doloop(p):
    ''' Doloop :   TkDo RelationalOperator TkArrow Content TkOd
                |   TkDo BooleanOperator TkArrow Content TkOd 
    '''
    p[0] = SyntaxLeaf('Doloop', p[2], [p[4]])



def p_forloop(p):
    ''' Forloop : TkFor TkId TkIn ArrayOperator TkTo ArrayOperator TkArrow Content TkRof
                | TkFor TkId TkIn ArrayOperator TkTo Terminal TkArrow Content TkRof
                | TkFor TkId TkIn Terminal TkTo ArrayOperator TkArrow Content TkRof
                | TkFor TkId TkIn Terminal TkTo Terminal TkArrow Content TkRof
    ''' 
    p[0] = SyntaxLeaf('Forloop', p[2], [p[4],p[6],p[8]])



def p_expression(p):
    ''' Expression  :   AritmeticOperator
                    |   Terminal
                    |   RelationalOperator
                    |   BooleanOperator
                    |   StrOperator
                    |   ArrayOperator
                    |   ArrayExpression
    '''
    p[0] = SyntaxLeaf('Expression', None, [p[1]])



def p_arrayexpres(p):
    ''' ArrayExpression :   TkId TkOpenPar Terminal TkTwoPoints Terminal TkClosePar
                        |   ArrayExpression TkOpenPar Terminal TkTwoPoints Terminal TkClosePar
                        |   TkId TkOBracket Terminal TkCBracket
                        |   ArrayExpression TkOBracket Terminal TkCBracket
    '''
    if (len(p)==7):
        if p[1] == 'TkId':
            p[0] = SyntaxLeaf('ArrayExpression', p[1], [p[3],p[5]])
        else:
            p[0] = SyntaxLeaf('ArrayExpression', None, [p[1],p[3],p[5]])
    else:
        if p[1] == 'TkId':
            p[0] = SyntaxLeaf('ArrayExpression', p[1], [p[3]])
        else:
            p[0] = SyntaxLeaf('ArrayExpression', None, [p[1],p[3]])




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
    if (len(p) == 6):
        p[0] = SyntaxLeaf('AritmeticOperator', p[3], [p[2], p[4]])
    elif (len(p) == 4):
        p[0] = SyntaxLeaf('AritmeticOperator', p[2], [p[1], p[3]])
    elif (len(p) == 3):
        p[0] = SyntaxLeaf('UnaryAritmeticOperator', p[1], [p[2]])
    else:
        p[0] = SyntaxLeaf('UnaryAritmeticOperator', p[2], [p[3]])
	
		

def p_Stroper(p):
    ''' StrOperator : TkId TkConcat TkId
        | TkOpenPar TkId TkConcat TkId TkClosePar
    '''
    if (len(p)==6):
        p[0] = SyntaxLeaf('StrOperator',[p[3],p[5]])
    else:
        p[0] = SyntaxLeaf('StrOperator',[p[1],p[3]])


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
    p[0] = SyntaxLeaf('ArrayOperator',p[4])



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
	if (len(p) == 6):
		p[0] = SyntaxLeaf('RelationalOperator', p[3], [p[2], p[4]])
	else:
		p[0] = SyntaxLeaf('RelationalOperator', p[2], [p[1], p[3]])



def p_variables(p):
    ''' Variables : TkId TkComma Variables
                | TkId 
    '''
    if (len(p)==4):
        p[0] = SyntaxLeaf('Variable', p[1], [p[3]])
    else:
        p[0] = SyntaxLeaf('Variable', p[1])    



def p_boolop(p):
	'''BooleanOperator : Expression TkAnd Expression
                |   Expression TkOr Expression
                |   TkOpenPar Expression TkAnd Expression TkClosePar
                |   TkOpenPar Expression TkOr Expression TkClosePar
                |   TkNot Expression
                |   TkOpenPar TkNot Expression TkClosePar
	'''
	if (len(p) == 4):
		p[0] = SyntaxLeaf('BooleanOperator', p[2], [p[1], p[3]])
	elif (len(p) == 3):
		p[0] = SyntaxLeaf('UnaryBooleanOperator', p[1], [p[2]])
	elif (len(p) == 5):
		p[0] = SyntaxLeaf('UnaryBooleanOperator', p[2], [p[3]])
	else:
		p[0] = SyntaxLeaf('BooleanOperator', p[3], [p[2], p[4]])



def p_datatype(p):
    ''' Datatype : TkInt
                |   TkBool
                |   Array
                |   TkInt TkComma Datatype
                |   TkBool TkComma Datatype
                |   Array TkComma Datatype
    '''
    if (len(p)==4):
        p[0] = SyntaxLeaf('Datatype', p[1], [p[3]])
    else:
        p[0] = SyntaxLeaf('Datatype', p[1])    



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
        SyntaxTreePrinter(out, "")