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



# Creando regla para las instrucciones permitidas por el lenguaje .
def p_instruction(p):
    '''INSTRUCTION : TkId TkAsig EXPRESSION
                |   TkOBlock TkDeclare DECLARATION_LIST INSTRUCTION_LIST TkCBlock
                |   TkOBlock INSTRUCTION_LIST TkCBlock
                |   TkRead TkId TkSemicolon
                |   TkIf EXPRESSION TkArrow INSTRUCTION_LIST TkFi
                |   TkGuard EXPRESSION TkArrow INSTRUCTION_LIST
                |   TkFor TkId TkIn EXPRESSION TkTo EXPRESSION TkArrow INSTRUCTION TkRof
                |   TkDo EXPRESSION TkArrow INSTRUCTION_LIST TkOd
    '''

# Regla que permite hacer una secuencia de instrucciones, estas siempre
# seran de la forma [<instruccion1>; ... ...<instruccion n>;] hasta que
# no exista otra (cayendo a lamda terminal).
def p_instList(p):
    '''INSTRUCTION_LIST :   INSTRUCTION
                        |   EXPRESSION TkSemicolon
                        |   INSTRUCTION_LIST TkSemicolon INSTRUCTION
                        |   INSTRUCTION_LIST TkSemicolon EXPRESSION
                        |   LAMBDA 
    '''
    if (len(p)==4):
        p[0] = InstructionList(p[1],p[3])
    elif (len(p)==2):
        pass


# Creando una regla que defina la declaracion de variables. Tienen la forma
# predefinida de [<Lista de Id's>:<Tipo de data>;] en caso de tener varias
# listas de declaraciones, finaliza con una nueva instancia de la lista. 
def p_declarationlist(p):
    '''DECLARATION_LIST   : DECLARATION
                        |   DECLARATION_LIST DECLARATION
                        |   TkId  TkTwoPoints DATATYPE TkSemicolon 
    '''



def p_declaration(p):
    ''' DECLARATION :   ARGUMENTS TkTwoPoints DATATYPE TkSemicolon
                    |   TkId TkTwoPoints TkArray TkOBracket NUMBER TkSoForth NUMBER TkCBracket
    '''


# Regla que define la creacion de listas de isentificadores de variables
# separadas por comas para implementar la declaracion listada de variables.
def p_arguments(p):
    '''ARGUMENTS    : ARGUMENTS TkComma TkId 
                    | TkId 
                    | LAMBDA
    '''


# Creando regla para definir tipajes de Gusb.
def p_datatype(p):
    ''' DATATYPE    :   TkInt
                    |   TkBool
    '''


# Defino una regla para una frase vacia
def p_lambda(p):
    ''' LAMBDA : 
    '''
    pass

# Regla para las expresiones permitidas del lenguaje. Desde identificadores,
# constantes booleanas y los operadores permitidos por guardedusb.
def p_expressions(p):
	'''EXPRESSION : NUMBER
                |   TkId
                |   TkString
                |   ARRAY
                |   TkOpenPar EXPRESSION TkClosePar
                |   TkOBracket EXPRESSION TkCBracket
                |   EXPRESSION TkPlus EXPRESSION
				|   EXPRESSION TkMinus EXPRESSION
				|   EXPRESSION TkMult EXPRESSION
				|   EXPRESSION TkDiv EXPRESSION
				|   EXPRESSION TkMod EXPRESSION
				|   EXPRESSION TkConcat EXPRESSION
                |   TkSize EXPRESSION
                |   TkMax EXPRESSION
                |   TkMin EXPRESSION
                |   TkAtoi EXPRESSION
                |   BOOLEAN
				|   EXPRESSION TkAnd EXPRESSION
				|   EXPRESSION TkOr EXPRESSION
				|   TkNot EXPRESSION %prec UMINUS
				|   EXPRESSION TkLess EXPRESSION
				|   EXPRESSION TkLeq EXPRESSION
				|   EXPRESSION TkGreater EXPRESSION
				|   EXPRESSION TkGeq EXPRESSION
				|   EXPRESSION TkEqual EXPRESSION
				|   EXPRESSION TkNEqual EXPRESSION
                |   TkPrint EXPRESSION
                |   TkPrintln EXPRESSION
    '''
	if len(p) == 4 :
		# Definicion de la regla para Operadores aritmeticos binarios.
		if (p[2]=='+' or p[2]=='-' or p[2]=='*' or p[2]=='/' or p[2]=='%') :
			p[0] = BinaryOperator(p[1],p[2],p[3])


def p_numbers(p):
    ''' NUMBER  :   TkNum
    '''

def p_booleans(p):
    ''' BOOLEAN : TkTrue
                | TkFalse
    '''

def p_array(p):
    ''' ARRAY   : TkArray TkOBracket TkNum TkSoForth TkNum TkCBracket
    '''

# Reglas de precedencia para el parser        
precedence = (
	('left', 'TkComma'),
	('left','TkOBracket','TkCBracket'),
	('left','TkOpenPar','TkClosePar'),
	('right','TkNot'),
	('left','TkAnd'),
	('left','TkOr'),
	('left','TkConcat'),
    ('right', 'UMINUS', 'TkSize'),
	('left','TkMult','TkDiv','TkMod'),
	('left','TkPlus','TkMinus'),
	('nonassoc','TkLess','TkLeq','TkGreater','TkGeq'),
	('left','TkEqual','TkNEqual'),
    )

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
        print(out)
        return (out)