#!/usr/bin/env python

#######################################
# CI3715 Traductores e Interpretadores
# Entrega 2. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################

# Defino una variable global que fija un Tab de 2
#espacios para la identacion del arbol.
TAB = '  '

# Clases para establecer la inicializacion del objeto que representara
# al token ['__init__'] y un metodo de impresion para el arbol ['ToString'].
class Block:
    """ Definicion del objeto [Bloque], se inicializa con una expresion o
    una declaracion."""

    def __init__(self,declaration,expression):
        self.expression = expression
        self.declaration = declaration

    def toString(self, identation):
        output = TAB*identation + 'Block\n'
        if self.declaration != None:
            output += self.declaration.toString(identation + 2)
        if self.expression != None:
            output += TAB*identation + 'kcolB\n'
        return output

class Declare:
    """ Definicion del objeto [Declaracion], se inicializa con una lista 
    de variables(Id's)"""
    def __init__(self,_list):
        self._list = _list

    def toString(self,identation):
        output = TAB*identation + 'Declare\n'
        output += self._list.toString(identation + 2) 
        output += TAB*identation + 'eralceD\n'

        return output

class ConditionalStatements:
    """ Definicion del objeto [Declaracion Condicional], se inicializa con
    una lista de tuplas de la forma [(conditional, instruction)] para hacer
    la analogia del ELIF planteado en GuardedUSB"""
    def __init__(self, _list):
        self._list = _list

    def toString(self, identation):
        output = TAB*identation + 'IF\n'
        for statement in self._list:
            output += TAB*(identation+2) + 'Guard\n'
            output += statement[0].toString(identation+4)
        #debo definir de manera recursiva la impresion

class BinaryOperator:
    """ Definicion del objeto [Operador Binario], se inicializa con ambos
    operandos mas el operador."""

    def __init__(self, left_operand, operator, right_operand):
        self.left_operand = left_operand
        self.operator = operator
        self.right_operand = right_operand

    def toString(self,identation):
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
            '>'     : 'GREATER',
            '>='    : 'GREATER_EQUAL',
            '=='    : 'EQUALS',
            '!='    : 'NOT_EQUAL',
           r'\|\|'  : 'CONCAT',
        }
        output = TAB*identation + operators[self.operator] + ' ' + self.operator +'\n'
        if isinstance(self.left_operand,OperandHandler):
            if self.left_operand.data_type == 'id':
                output += TAB*(identation + 2) + 'Ident:\n'
                output += TAB*(identation + 4) + self.left_operand + '\n'
            else:
                output += self.left_operand.toString(identation +2)
        else:
            output += self.left_operand.toString(identation +2)
        
        if isinstance(self.right_operand,OperandHandler):
            if self.right_operand.data_type == 'id':
                output += TAB*(identation + 2) + 'Ident:\n'
                output += TAB*(identation + 4) + self.left_operand + '\n'
            else:
                output += self.right_operand.toString(identation +2)
        else:
            output += self.right_operand.toString(identation +2)
        return output

class OperandHandler:
    """Definicion para el objeto [Manejador de Operandos] el cual trata
    las declaraciones los operandos derecho e izquierdo de los operadores 
    binarios."""
    def __init__(self,data_type,data_value):
        self.data_type = data_type
        self.data_value = data_value

    def toString(self,identation):
        if (self.data_type=='id'):
            output = ' '*identation + 'Ident:' + '\n'
            output += ' '*(identation + 2) + str(self.data_value) + '\n'
        elif (self.data_type=='array'):
            output = ' '*identation + self.data_type + '\n'
            output += self.data_value.toString(identation + 2)
        else:    
            output = ' '*identation + self.data_type + '\n'
            output += ' '*(identation + 2) + str(self.data_value) + '\n'
        return output


#WRITE RULES BELOW



# Variable global del primer error del parser si existe.
global parser_error
parser_error = False