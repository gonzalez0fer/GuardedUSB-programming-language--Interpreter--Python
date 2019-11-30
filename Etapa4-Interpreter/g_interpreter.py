#######################################
# CI3715 Traductores e Interpretadores
# Entrega 4. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################

import sys
from g_context import *
from g_AbsSyntaxTree import *

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
                    if(leaf != ';'):
                        if(leaf.p_type == 'Block' or leaf.p_type == 'Content'):
                            for child in leaf.childs:
                                if(child != ';'):
                                    self.SyntaxTreeContextEvaluator(child)
                            
                        elif (leaf.p_type == 'Asign'):
                            #almaceno el nombre de la variable
                            var_name = leaf.p_value
                            #almaceno el valor a asignar
                            assignation = leaf.childs[0]

                            if(len(assignation.childs) > 1):
                                var_value = []
                                var_value.append(self.ExpressionEvaluator(assignation.childs[0]))
                                
                                assignation = assignation.childs[1]
                                numberChilds = len(assignation.childs)
                                while(numberChilds == 2):
                                    var_value.append(self.ExpressionEvaluator(assignation.childs[0]))
                                    assignation = assignation.childs[1]
                                    numberChilds = len(assignation.childs)
                                
                                var_value.append(self.ExpressionEvaluator(assignation.childs[0]))
                            else:
                                var_value = self.ExpressionEvaluator(assignation.childs[0])

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

                        elif (leaf.p_type == 'Declare' or leaf.p_type == 'Instruction'):
                            self.SyntaxTreeContextEvaluator(leaf)

                        elif (leaf.p_type== 'Output'):
                            value = self.ExpressionEvaluator(leaf.childs[0])
                            print(value)

                        elif (leaf.p_type == 'Input'):
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
                                        print("[Interpreter Error] line " + str(leaf.p_line) + ' column '+str(leaf.p_column)+ \
                                        '. Trying to asign list of expressions of different types.')
                                        sys.exit(0)
                                    elif(isinstance(val, int) and s_table_type!= 'int'):
                                        print("[Interpreter Error] line " + str(leaf.p_line) + ' column '+str(leaf.p_column)+ \
                                        '. Trying to asign list of expressions of different types.')
                                        sys.exit(0)
                            self.setValue(var, val)
                        
                        elif(leaf.p_type == 'Conditional'):
                            self.ConditionalEvaluator(leaf)

                        elif (leaf.p_type == 'Forloop'):
                            control_var = self.getValue(leaf.p_value, None, True)

                            if control_var!= False:

                                for scope in self.SymbolsTable:
                                    if control_var in scope:
                                        #si esta en la tabla y no es entero, retorna error
                                        s_table_type = scope[control_var].s_type
                                        if(isinstance(control_var,int) and s_table_type!='int'):
                                            print("[Interpreter Error] line " + str(leaf.p_line) + ' column '+str(leaf.p_column)+ \
                                                '. Variable ' + control_var.s_value + ' is not type integer to be used as control variable')
                                            sys.exit(0)

                            #creo simbolo de la variable y scope y le asigno el simbolo que cree.
                            cont_symbol = ContextSymbol(self.getValue(leaf.p_value,None,True),'int')
                            self.SymbolsTable.insert(0,{})
                            self.SymbolsTable[0][leaf.p_value] = cont_symbol

                            min_limit = self.ExpressionEvaluator(leaf.childs[0])
                            self.setValue(leaf.p_value, min_limit)
                            max_limit = self.ExpressionEvaluator(leaf.childs[1])

                            for i in range(min_limit, max_limit):
                                # actualizar valor del contador en cada iteracion
                                self.setValue(leaf.p_value, i)
                                self.SyntaxTreeContextEvaluator(leaf.childs[0])
                            # guardar valor original
                            #self.setValue(leaf.valor[0], val)
                            self.SymbolsTable.pop(0)


                        elif (leaf.p_type == 'DoLoop'):
                            exp = self.ExpressionEvaluator(leaf.p_value)
                            while (exp):
                                self.SyntaxTreeContextEvaluator(leaf.childs[0])
                                # evaluar guardia en cada iteracion
                                comprobarexp = self.ExpressionEvaluator(leaf.p_value)
                                if (comprobarexp):
                                    continue
                                else:
                                    break

                        else:
                            self.SyntaxTreeContextEvaluator(leaf)

        else:
            print('[Interpreter Error]: No SyntaxTreeStructure')

    def ConditionalEvaluator(self, leaf):
        exp = self.ExpressionEvaluator(leaf.childs[0])
        
        if(exp):
            self.SyntaxTreeContextEvaluator(leaf.childs[1])
        
        if(len(leaf.childs) > 2):
            self.ConditionalEvaluator(leaf.childs[2])

    def ExpressionEvaluator(self, expression):

        if (expression.p_type == 'Terminal'):
            if (len(expression.childs)>0):
                t = self.ExpressionEvaluator(expression.childs[0])
                return t
            else:
                if (expression.c_type == 'var'):
                    t = self.getValue(expression.c_lexeme)
                    return t.s_asignvalue
                else:
                    if (expression.c_lexeme == 'true'):
                        return True
                    elif (expression.c_lexeme == 'false'):
                        return False
                    else:
                        return expression.c_lexeme

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
            elif (operator_tok == '=='):
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
                    print("[Interpreter Error]: " + str(expression.p_line) + \
                        ' column '+str(expression.p_column)+' division by zero not allowed ')
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

        elif(expression.p_type == 'ArrayOperator'):
            # POR AHORA NADA MAS EL CASO QUE SE LE PASE EL ID DE LA VARIABLE DE UNA VEZ
            var = self.getValue(expression.child[0])

            if(expression.p_value == 'max'):
                return max(var.s_asignvalue)
            elif(expression.p_value == 'min'):
                return min(var.s_asignvalue)
            elif(expression.p_value == 'atoi'):
                if(var.array_indexes[0] == var.array_indexes[1]):
                    return var.s_asignvalue[0]
                else:
                    print("[Context Error] line " + str(expression.p_line) + ' column '+\
                            str(expression.p_column)+ '. Array ' + var.s_value + ' has not length 1.')
                    sys.exit(0)
            elif(expression.p_value == 'size'):
                return len(var.s_asignvalue)

        elif(expression.p_type == 'ArrayExpression'):
            if(len(expression.childs) == 1):
                index = self.ExpressionEvaluator(expression.childs[0])

                if(isinstance(expression.p_value, SyntaxLeaf)):
                    t = self.ExpressionEvaluator(expression.p_value)
                else:
                    t = self.getValue(expression.p_value, None, None)
                
                if(index > t.array_indexes[1] or index < t.array_indexes[0]):
                        print("[Context Error] line " + str(expression.p_line) + ' column '+\
                            str(expression.p_column)+ '. Array expression out of boundaries.')
                        sys.exit(0)
                
                return t.s_asignvalue[index]
            else:
                index = self.ExpressionEvaluator(expression.childs[0])
                val = self.ExpressionEvaluator(expression.childs[1])

                if(isinstance(expression.p_value, SyntaxLeaf)):
                    t = self.ExpressionEvaluator(expression.p_value)
                else:
                    t = self.getValue(expression.p_value, None, None)
                
                if(index > t.array_indexes[1] or index < t.array_indexes[0]):
                        print("[Context Error] line " + str(expression.p_line) + ' column '+\
                            str(expression.p_column)+ '. Array expression out of boundaries.')
                        sys.exit(0)
                
                t.s_asignvalue[index] = val

                return t.s_asignvalue

        elif(expression.p_type == 'Expression'):
            t = self.ExpressionEvaluator(expression.childs[0])
            return t


    def setValue(self, var, val, index=None):
        #Aqui recibira la tabla e ira asignando e imprimiendo errores
        if (len(self.SymbolsTable) > 0):
            for i in range(len(self.SymbolsTable)):
                if var in self.SymbolsTable[i]:
                    self.SymbolsTable[i][var].s_asignvalue = val
        
        # Sino impresion de errores

    def getValue(self, var, isIndex=None, isControl=None):
        if (len(self.SymbolsTable) > 0):
            for i in range(len(self.SymbolsTable)):
                if var in self.SymbolsTable[i]:
                    
                    if(isControl != None):
                        return self.SymbolsTable[i][var]
                    
                    if(isIndex != None):
                        if(self.SymbolsTable[i][var].is_array):
                            if(isIndex < self.SymbolsTable[i][var].array_indexes[0] or isIndex > self.SymbolsTable[i][var].array_indexes[1]):
                                print('[Interpreter Error] Index ' + isIndex + ' is out of boundaries')
                    
                    return self.SymbolsTable[i][var]

        return False