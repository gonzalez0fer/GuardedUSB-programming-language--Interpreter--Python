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

def p_expressions(p):
	'''expression : expression TkPlus expression
				| expression TkMinus expression
				| expression TkMult expression
				| expression TkDiv expression
				| expression TkMod expression
                | TkOpenPar expression TkClosePar 
                | TkOBracket expression TkCBracket
    '''
	if len(p) == 4 :
		# Definicion de la regla para Operadores aritmeticos binarios.
		if (p[2]=='+' or p[2]=='-' or p[2]=='*' or p[2]=='/' or p[2]=='%') :
			p[0] = BinaryOperator(p[1],p[2],p[3])

        # Definicion de la regla para Delimitadores de la expresion.
		# elif ((p[1] == '(') and (p[3] == ')')):
		# 	p[0] = ParentisedExpression(p[1], p[2], p[3])
		# elif ((p[1] == '[') and (p[3] == ']')):
		# 	p[0] = BracketedExpression(p[1], p[2], p[3])


# Regla para poder encontrar los errores sintácticos.
def p_error(p):
    global parser_error
    if (p is not None):
        msg = "Error de sintaxis. Se encontró token " + str(p.value) + " en la linea "
        msg += str(p.lineno) + ", columna " + str(find_column(p.lexer.lexdata,p))
    else:
        msg = "Error de sintaxis al final del archivo"
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