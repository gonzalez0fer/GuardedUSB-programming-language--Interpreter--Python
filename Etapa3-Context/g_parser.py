#!/usr/bin/env python

#######################################
# CI3715 Traductores e Interpretadores
# Entrega 3. 
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

# Reglas que definen al elemento [Block]
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

   
# Reglas que definen al elemento [Declare]
def p_declaration(p):
    ''' Declaration :   Variables TkTwoPoints Datatype
                    |   Variables TkTwoPoints Datatype TkSemicolon Declaration
    '''
    if (len(p)==4):
        p[0] = SyntaxLeaf('Declare', None, [p[1],p[3]])
    else:
        p[0] = SyntaxLeaf('Declare', None, [p[1],p[3],p[4],p[5]])      


# Reglas que definen al elemento [Array]
def p_array(p):
    ''' Array   :   TkArray TkOBracket Terminal TkSoForth Terminal TkCBracket
                |   TkArray TkOBracket AritmeticOperator TkSoForth AritmeticOperator TkCBracket
    '''
    p[0] = SyntaxLeaf('Array', None, [p[3],p[5]])


# Reglas que definen al elemento [Terminal]
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
        if (str(p[2].lexeme)).isdigit():
            p[0].c_type = 'int'
            p[0].lexeme = str(p[2].lexeme)
        elif (p[2].lexeme == "True" \
            or p[2].lexeme == "False"):
            p[0].c_type = 'bool'
            p[0].lexeme = str(p[2].lexeme)
        else:
            p[0].type = "var"
            p[0].lexeme = p[2].lexeme           

    else:
        p[0] = SyntaxLeaf('Terminal', p[1])
        if ((str(p[1])).isdigit()):
            p[0].type = "int"
            p[0].lexeme = p[1]
        elif (p[1] == "True" \
            or p[1] == "False"):
            p[0].type = "bool"
            p[0].lexeme = p[1]
        else:
            p[0].type = "var"
            p[0].lexeme = p[1]




# Reglas que definen al elemento [Content]
def p_content(p):
	''' Content :   Instruction
                |   Instruction TkSemicolon Content
                |   Block TkSemicolon Content
                |   Block
	'''
	if (len(p) == 2):
		p[0] = SyntaxLeaf('Content', None, [p[1]])
	else:
		p[0] = SyntaxLeaf('Content', None, [p[1], p[2], p[3]])
    

# Reglas que definen al elemento [Instruction]
def p_instruction(p):
    ''' Instruction :   Conditional
                    |   Forloop
                    |   Doloop
                    |   Asign
                    |   Input
                    |   Output
    '''
    p[0] = SyntaxLeaf('Instruction', None, [p[1]])


# Reglas que definen al elemento [Conditional]
def p_conditional(p):
    ''' Conditional :   TkIf Expression TkArrow Content TkFi
                    |   TkIf Expression TkArrow Content Guard TkFi
    '''
    if (len(p)==6):
        p[0] = SyntaxLeaf('Conditional', None, [p[2],p[4]])
    else:
        p[0] = SyntaxLeaf('Conditional', None, [p[2],p[4],p[5]])


# Reglas que definen al elemento [Guard]
def p_guard(p):
    ''' Guard   :   TkGuard Expression TkArrow Content
                |   TkGuard Expression TkArrow Content Guard
    '''
    if (len(p)==5):
        p[0] = SyntaxLeaf('Guard', None, [p[2],p[4]])
    else:
        p[0] = SyntaxLeaf('Guard', None, [p[2],p[4],p[5]])


# Reglas que definen al elemento [Asign]
def p_asign(p):
    ''' Asign    :   TkId TkAsig Expression
    '''
    p[0] = SyntaxLeaf('Asign', p[1], [p[3]])


# Reglas que definen al elemento [Asign]
def p_input(p):
    ''' Input   :   TkRead TkId
    '''
    p[0] = SyntaxLeaf('Input', p[1], [p[2]])


# Reglas que definen al elemento [Output]
def p_output(p):
    '''Output   :   TkPrint Expression
                |   TkPrint Expression ConcatExpression
                |   TkPrintln Expression
                |   TkPrintln Expression ConcatExpression
    '''
    if(len(p)==4):
        p[0] = SyntaxLeaf('Output', p[1], [p[2],p[3]])
    else:
        p[0] = SyntaxLeaf('Output', p[1], [p[2]])


# Reglas que definen al elemento [ConcatExpression]
def p_concatexp(p):
    ''' ConcatExpression : TkConcat Expression
                        |   TkConcat Expression ConcatExpression
    '''
    if(len(p)==4):
        p[0] = SyntaxLeaf('ConcatExpression', None, [p[2],p[3]])
    else:
        p[0] = SyntaxLeaf('ConcatExpression', None, [p[2]])


# Reglas que definen al elemento [Doloop]
def p_doloop(p):
    ''' Doloop :   TkDo Expression TkArrow Content TkOd
                |   TkDo Expression TkArrow Content Guard TkOd 
    '''
    if(len(p)== 6):
        p[0] = SyntaxLeaf('Doloop', None, [p[2], p[4]])
    else:
        p[0] = SyntaxLeaf('Doloop', None, [p[2], p[4], p[5]])


# Reglas que definen al elemento [Forloop]
def p_forloop(p):
    ''' Forloop : TkFor TkId TkIn Expression TkTo Expression TkArrow Content TkRof
    ''' 
    p[0] = SyntaxLeaf('Forloop', p[2], [p[4],p[6],p[8]])


# Reglas que definen al elemento [Forloop]
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


# Reglas que definen al elemento [ArrayExpression]
def p_arrayexpres(p):
    ''' ArrayExpression :   ArrayExpression TkOpenPar Terminal TkTwoPoints Terminal TkClosePar
                        |   TkId TkOpenPar Terminal TkTwoPoints Terminal TkClosePar
                        |   ArrayExpression TkOBracket Terminal TkCBracket
                        |   TkId TkOBracket Terminal TkCBracket
    '''
    if (len(p)==7):
        p[0] = SyntaxLeaf('ArrayExpression', p[1], [p[3],p[5]])
    else:
        p[0] = SyntaxLeaf('ArrayExpression', p[1], [p[3]])


# Reglas que definen al elemento [AritmeticOperator]
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
	
		
# Reglas que definen al elemento [StrOperator]
def p_Stroper(p):
    ''' StrOperator : TkId TkConcat TkId
        | TkOpenPar TkId TkConcat TkId TkClosePar
    '''
    if (len(p)==6):
        p[0] = SyntaxLeaf('StrOperator',[p[3],p[5]])
    else:
        p[0] = SyntaxLeaf('StrOperator',[p[1],p[3]])


# Reglas que definen al elemento [ArrayOperator]
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
    p[0] = SyntaxLeaf('ArrayOperator', p[1], [p[3]])


# Reglas que definen al elemento [RelationalOperator]
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


# Reglas que definen al elemento [Variables]
def p_variables(p):
    ''' Variables : TkId TkComma Variables
                | TkId 
    '''
    if (len(p)==4):
        p[0] = SyntaxLeaf('Variable', p[1], [p[3]])
    else:
        p[0] = SyntaxLeaf('Variable', p[1])    


# Reglas que definen al elemento [BooleanOperator]
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


# Reglas que definen al elemento [Datatype]
def p_datatype(p):
    ''' Datatype : TkInt
                |   Array
                |   TkBool
                |   TkInt TkComma Datatype
                |   TkBool TkComma Datatype
                |   Array TkComma Datatype
    '''
    if (len(p)==4):
        p[0] = SyntaxLeaf('Datatype', p[1], [p[3]])
    else:
        p[0] = SyntaxLeaf('Datatype', p[1])    


# Reglas que definen el formato de impresion del error
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