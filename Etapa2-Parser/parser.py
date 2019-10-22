#!/usr/bin/env python

#######################################
# CI3715 Traductores e Interpretadores
# Entrega 2. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################

# Clases para establecer la inicializacion del objeto que representara
# al token ['__init__'] y un metodo de impresion para el arbol ['ToString'].
class Block:
    """ Definicion del objeto [Bloque], se inicializa con una expresion o
    una declaracion."""

    def __init__(self,declaration,expression):
        self.expression = expression
        self.declaration = declaration

    def toString(self, spacing):
        output = '  '*spacing + 'BLOCK\n'
        if self.declaration != None:
            output += self.declaration.toString(spacing + 2)
        if self.expression != None:
            output += '  '*spacing + 'KCOLB\n'
        return output


class BinaryOperator:
    """ Definicion del objeto [Operador Binario], se inicializa con ambos
    operandos mas el operador."""

    def __init__(self, left_operand, operator, right_operand):
        self.left_operand = left_operand
        self.operator = operator
        self.right_operand = right_operand

    def toString(self,spacing):
        operators ={
            '+'     : 'PLUS',
            '-'     : 'MINUS',
            '*'     : 'MULT',
            '/'     : 'DIV',
            '%'     : 'MODULE',
           r'\/'    : 'OR',
           r'/\\'   : 'AND',
            '<'     : 'LESS',
            '<='    : 'LESS_EQUAL',
            '<'     : 'GREATER',
            '>='    : 'GREATER_EQUAL',
            '=='    : 'EQUALS',
            '!='    : 'NOT_EQUAL',
           r'\|\|'  : 'CONCAT',
        }
        output = '  '*spacing + operators[self.operator] + ' ' + self.operator +'\n'
        if isinstance(self.left_operand,OperandHandler):
            if self.left_operand.data_type == 'id':
                output += '  '*(spacing + 2) + 'Ident:\n'
                output += '  '*(spacing + 4) + self.left_operand + '\n'
            else:
                output += self.left_operand.toString(spacing +2)
        else:
            output += self.left_operand.toString(spacing +2)
        
        if isinstance(self.right_operand,OperandHandler):
            if self.right_operand.data_type == 'id':
                output += '  '*(spacing + 2) + 'Ident:\n'
                output += '  '*(spacing + 4) + self.left_operand + '\n'
            else:
                output += self.right_operand.toString(spacing +2)
        else:
            output += self.right_operand.toString(spacing +2)
        return output

class OperandHandler:
    """Definicion para el objeto [Manejador de Operandos] el cual trata
    las declaraciones los operandos derecho e izquierdo de los operadores 
    binarios."""
    def __init__(self,data_type,data_value):
        self.data_type = data_type
        self.data_value = data_value

    def toString(self,spacing):
        if (self.data_type=='id'):
            output = ' '*spacing + 'Ident:' + '\n'
            output += ' '*(spacing + 2) + str(self.data_value) + '\n'
        elif (self.data_type=='array'):
            output = ' '*spacing + self.data_type + '\n'
            output += self.data_value.toString(spacing + 2)
        else:    
            output = ' '*spacing + self.data_type + '\n'
            output += ' '*(spacing + 2) + str(self.data_value) + '\n'
        return output


#WRITE RULES BELOW



# Variable global del primer error del parser si existe.
global parser_error
parser_error = False