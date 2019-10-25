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

# De aqui en adelante escribimos las reglas que definiran la gramatica
# de nuestro lenguaje para filtrar errores sintacticos y construir 
# nuestro arbol sintactico abstracto.

def p_datatype(p):
    ''' DATATYPE    :   TkInt
                    |   TkBool
                    |   TkArray
    '''
    p[0] = p[1]


def p_declarar(p):
    '''DECLARE : TkDeclare DECLARATION_LIST
    '''
    p[0] = Declare(p[2])


def p_epsilon(p):
    ''' EPSILON : 
    '''
    pass


def p_declarationlist(p):
    '''DECLARATION_LIST   : ID_LIST TkTwoPoints DATATYPE TkSemicolon DECLARATION_LIST
                            | ID_LIST TkTwoPoints DATATYPE TkSemicolon 
    '''
    if (len(p)==4):
        p[0] = DeclarationList(p[1],p[2],None)
    else:
        p[0] = DeclarationList(p[1],p[2],p[4])


def p_idList(p):
    '''ID_LIST    : ID_LIST TkComma TkId 
                    | TkId '''
    if (len(p)==2):
        p[0] = IdList(None,OperandHandler('id',p[1]))
    else:
        p[0] = IdList(p[1],OperandHandler('id',p[3]))


def p_instList(p):
    '''INSTRUCTION_LIST : INSTRUCTION TkSemicolon INSTRUCTION_LIST
                        | EPSILON '''
    if (len(p)==4):
        p[0] = InstructionList(p[1],p[3])
    elif (len(p)==2):
        pass


def p_expressions(p):
	'''EXPRESSION : TkNum
                |   TkId
                |   TkOpenPar EXPRESSION TkClosePar
                |   TkOBracket EXPRESSION TkCBracket
                |   EXPRESSION TkPlus EXPRESSION
				|   EXPRESSION TkMinus EXPRESSION
				|   EXPRESSION TkMult EXPRESSION
				|   EXPRESSION TkDiv EXPRESSION
				|   EXPRESSION TkMod EXPRESSION
				|   EXPRESSION TkAnd EXPRESSION
				|   EXPRESSION TkOr EXPRESSION
				|   EXPRESSION TkLess EXPRESSION
				|   EXPRESSION TkLeq EXPRESSION
				|   EXPRESSION TkGreater EXPRESSION
				|   EXPRESSION TkGeq EXPRESSION
				|   EXPRESSION TkEqual EXPRESSION
				|   EXPRESSION TkNEqual EXPRESSION
				|   EXPRESSION TkConcat EXPRESSION
                |   TkSize EXPRESSION
                |   TkMax EXPRESSION
                |   TkMin EXPRESSION
                |   TkAtoi EXPRESSION
                |   TkFalse
                |   TkTrue
				|   EXPRESSION TkNot

    '''
	if len(p) == 4 :
		# Definicion de la regla para Operadores aritmeticos binarios.
		if (p[2]=='+' or p[2]=='-' or p[2]=='*' or p[2]=='/' or p[2]=='%') :
			p[0] = BinaryOperator(p[1],p[2],p[3])


def p_instruction(p):
    '''INSTRUCTION : TkId TkAsig EXPRESSION
                |   TkOBlock DECLARE INSTRUCTION_LIST TkCBlock
                |   TkOBlock INSTRUCTION_LIST TkCBlock
                |   TkRead TkId
                |   TkFor TkId TkIn EXPRESSION TkTo EXPRESSION TkArrow INSTRUCTION TkRof
                |   TkDo EXPRESSION TkArrow INSTRUCTION TkOd
                |   TkGuard EXPRESSION TkArrow INSTRUCTION
                |   TkIf EXPRESSION TkArrow INSTRUCTION TkFi
    '''

def p_error(p):
    global parser_error
    if (p is not None):
        msg = "[Syntax Error]. Wrong token found " + str(p.value) + " line "
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
    out = parser.parse(meta_program)
    if not(parser_error):
        return (out.toString(0))