#######################################
# CI3715 Traductores e Interpretadores
# Entrega 4. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################

import sys
from g_context import *

#   En este file reposan la clase InterpretedTreeEval
# el cual se encarga de hacer las evaluaciones 
# respectivas de nuestro programa.

class InterpretedTreeEvaluator():
    """ Definicion del objeto [InterpretedTreeEval], cuyos metodos se encargaran
    de hacer el recorrido del arbol contrastando con las tablas de simbolos creadas
    en el contexto y haciendo los calculos pertinentes para la interpretacion.

    inicializa con: 
            SymbolsTable : pila de scopes producidos en el SyntaxTreeContext
    """
    def __init__(self, SymbolsTable):
        self. SymbolsTable = SymbolsTable

    def SyntaxTreeContextEvaluator(self, SyntaxTreeStructure):
        """ Definicion del metodo [SyntaxTreeContextEvaluator], el cual se encarga de hacer 
        el recorrido del arbol contrastando con las tablas de simbolos creadas
        en el contexto y haciendo los calculos pertinentes para la interpretacion.

        
        recibe: SyntaxTreeStructure : Estructura completa del arbol sintactico a analizar.
        """
        if SyntaxTreeStructure:
            if (len(SyntaxTreeStructure.childs) > 0):
                for leaf in SyntaxTreeStructure.childs:

                    if (leaf.p_type == 'Asign'):
                        #almaceno el nombre de la variable
                        var_name = leaf.p_value
                        #almaceno el valor a asignar
                        var_value = self.ExpressionEvaluator(leaf.childs[0])

                        #la variable puede ser de tipo int, bool, sino arreglo
                        if (isinstance(var_name,str)):
                            self.setValue(var_name, var_value)
                        else:
                            #########################por definir idea
                            pass
                            array_index = self.ExpressionEvaluator(leaf.childs[0])
                            self.setValue(var_name.p_value, var_value, array_index) 

                    elif (leaf.p_type == 'Variable'):
                        for child in leaf.childs:
                            self.SyntaxTreeContextEvaluator(child)

                    elif (leaf.p_type == 'Declare'):
                        self.SyntaxTreeContextEvaluator(leaf)

                    elif (leaf.p_type== 'Output'):
                        value = self.ExpressionEvaluator(leaf.childs[0])
                        print(value)

                    elif (leaf.p_type == 'ENTRADA'):
                        val = input()
                        var = leaf.p_value
                        if (val == 'false'):
                            val = False
                        elif (val == 'true'):
                            val = True
                        if (val.isdigit()):
                            val = int(val)

                        # Revisando tipaje con la tabla, si es correcto,
                        # se asigna.
                        for i in self.SymbolsTable:
                            if var in i:
                                s_table_type = i[var].s_type
                                if(isinstance(val,bool) and s_table_type!='bool'):
                                    print("Error. Tipo incorrecto")
                                    sys.exit(0)
                                elif(isinstance(val, int) and s_table_type!= 'int'):
                                    print("Error. Tipo incorrecto")
                                    sys.exit(0)
                        self.setValor(var, val)

        else:
            print('[Interpreter Error]: No SyntaxTreeStructure')


    def ExpressionEvaluator(self, expression):

        if (expression.p_type == 'Terminal'):
            if (len(expression.childs)>0):
                t = self.ExpressionEvaluator(expression.childs[0])
                return t
            else:
                if (expression.c_type == 'var'):
                    pass
                    #t = self.getValor(expression.lexeme)
                    return t
                else:
                    if (expression.lexeme == 'true'):
                        return True
                    elif (expression.lexeme == 'false'):
                        return False
                    else:
                        return expression.lexeme

        elif (expression.p_type  == 'BooleanOperator'):
            operator_tok = expression.p_value
            op1 = self.ExpressionEvaluator(expression.childs[0])
            op2 = self.ExpressionEvaluator(expression.childs[1])
            if (operator_tok == '\\/'):
                res = op1 or op2
            elif (operator_tok == '/\\'):
                res = op1 and op2
            return res

        elif (expression.p_type  == 'UnaryBooleanOperator'):
            op = self.ExpressionEvaluator(expression.childs[0])
            return not op

        elif (expression.p_type == 'RelationalOperator'):
            operator_tok = expression.p_value
            op1 = self.ExpressionEvaluator(expression.childs[0])
            op2 = self.ExpressionEvaluator(expression.childs[1])

            if (operator_tok == '<'):
                res = op1 < op2
            elif (operator_tok == '>'):
                res = op1 > op2
            elif (operator_tok == '<='):
                res = op1 <= op2
            elif (operator_tok == '>='):
                res = op1 >= op2
            elif (operator_tok == '='):
                res = op1 == op2
            elif (operator_tok == '!='):
                res = op1 != op2
            return res

        elif (expression.p_type == 'AritmeticOperator'):
            operator_tok = expression.p_value
            op1 = self.ExpressionEvaluator(expression.childs[0])
            op2 = self.ExpressionEvaluator(expression.childs[1])

            if (operator_tok == '+'):
                res = op1 + op2
            elif (operator_tok == '-'):
                res = op1 - op2
            elif (operator_tok == '*'):
                res = op1 * op2
            elif (operator_tok == '/'):
                if (op2 == 0):
                    print("[Interpreter Error]: Zero div not allowed")
                    sys.exit(0)
                else:
                    res = op1 / op2
            elif (operator_tok == '%'):
                res = op1 % op2
            # se redondea el entero puesto a que no existe float
            return int(res)

        elif (expression.p_type == 'UnaryAritmeticOperator'):
            op = self.ExpressionEvaluator(expression.childs[0])
            return -op

        elif(expression.p_type == 'Expression'):
            t = self.ExpressionEvaluator(expression.childs[0])


    def setValor(self, var, val, index=None):
        #Aqui recibira la tabla e ira asignando e imprimiendo errores
        pass
