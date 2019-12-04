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
                            self.SyntaxTreeContextEvaluator(leaf)
                            
                        elif (leaf.p_type == 'Asign'):
                            #almaceno el nombre de la variable
                            var_name = leaf.p_value

                            var = self.getValue(var_name)
                            
                            if var_name in self.SymbolsTable[0]:
                                print("[Interpreter Error] line " + str(leaf.p_line) + ' column '+\
                                    str(leaf.p_column)+  ". Trying to modify variable " + leaf.p_value + " of iteration.")
                                sys.exit(0)
                            
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
                        
                        elif(leaf.p_type == 'Instruction'):
                            self.SyntaxTreeContextEvaluator(leaf)

                        elif (leaf.p_type == 'Declare'):
                            var = leaf.childs[0].p_value

                            if var in self.SymbolsTable[0]:
                                print("[Interpreter Error] line " + str(leaf.p_line) + ' column '+\
                                    str(leaf.p_column)+  ". Redeclare control variable is not allowed.")
                                sys.exit(0)
                            
                            self.SyntaxTreeContextEvaluator(leaf)

                        elif (leaf.p_type== 'Output'):
                            value = self.ConcatEvaluator(leaf)
                            if(leaf.p_value == "print"):
                                print(value, end = '')
                            else:
                                print(value)

                        elif (leaf.p_type == 'Input'):
                            var = self.getValue(leaf.childs[0])
                            s_table_type = var.s_type
                            
                            if(var.is_array):
                                input_v = input()
                                val = input_v.split(",")

                                len_var = var.array_indexes[1] - var.array_indexes[0]

                                if(len(val) != len_var):
                                    print("[Interpreter Error] line " + str(leaf.p_line) + ' column '+str(leaf.p_column)+ \
                                    '. Number of elements inserted are different from array size.')
                                    sys.exit(0)
                            else:
                                val = input()
                
                                if (val == 'false'):
                                    val = False
                                elif (val == 'true'):
                                    val = True
                                elif (val.isdigit()):
                                    val = int(val)

                            # Revisando tipaje con la tabla, si es correcto,
                            # se asigna.
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

                            if (control_var != False):
                                s_table_type = control_var.s_type
                                if(s_table_type != 'int'):
                                    print("[Interpreter Error] line " + str(leaf.p_line) + ' column '+str(leaf.p_column)+ \
                                        '. Variable ' + control_var.s_value + ' is not type integer to be used as control variable')
                                    sys.exit(0)

                            #creo simbolo de la variable y scope y le asigno el simbolo que cree.
                            cont_symbol = ContextSymbol(self.getValue(leaf.p_value,None,True),'int')
                            cont_symbol.is_index = True
                            self.SymbolsTable[0][leaf.p_value] = cont_symbol

                            min_limit = self.ExpressionEvaluator(leaf.childs[0])
                            self.setValue(leaf.p_value, min_limit)
                            max_limit = self.ExpressionEvaluator(leaf.childs[1])

                            for i in range(min_limit, max_limit + 1):
                                # actualizar valor del contador en cada iteracion
                                self.setValue(leaf.p_value, i)
                                self.SyntaxTreeContextEvaluator(leaf.childs[2])
                            # guardar valor original
                            #self.setValue(leaf.p_value, val)
                            self.SymbolsTable[0].pop(leaf.p_value)

                        elif (leaf.p_type == 'Doloop'):
                            exp = self.ExpressionEvaluator(leaf.childs[0])
                            if(len(leaf.childs) == 2):
                                while (exp):
                                    self.SyntaxTreeContextEvaluator(leaf.childs[1])
                                    # evaluar guardia en cada iteracion
                                    check_exp = self.ExpressionEvaluator(leaf.childs[0])
                                    if (check_exp):
                                        continue
                                    else:
                                        break
                            else:
                                guard = leaf.childs[2]
                                expressions = []
                                while(len(guard.childs) > 2):
                                    expressions.append(guard.childs[0])
                                    guard = leaf.childs[2]
                                
                                expressions.append(guard.childs[0])

                                for exp_b in expressions:
                                    exp = exp or self.ExpressionEvaluator(exp_b)
                                
                                while (exp):
                                    self.ConditionalEvaluator(leaf)
                                    # evaluar guardia en cada iteracion
                                    check_exp = self.ExpressionEvaluator(leaf.childs[0])
                                    
                                    for exp_b in expressions:
                                        check_exp = check_exp or self.ExpressionEvaluator(exp_b)
                                    if (check_exp):
                                        continue
                                    else:
                                        break
                        else:
                            self.SyntaxTreeContextEvaluator(leaf)
        else:
            print('[Interpreter Error]: No SyntaxTreeStructure')


    def ConcatEvaluator(self, exp):
        """ Definicion del metodo [ConcatEvaluator], el cual se encarga de hacer 
        el tratamiento a las expresiones que seran utilizadas para la concatenacion.

        recibe: exp : Expresion a Evaluar.
        """
        c_exp = str(self.ExpressionEvaluator(exp.childs[0]))
        if(c_exp[0] == "\""):
            c_exp = c_exp[1:-1]
        elif(c_exp[0] == "["):
            t = self.getValue(exp.childs[0].childs[0].c_lexeme)

            aux_list = [x for x in range(t.array_indexes[0], t.array_indexes[1]+1)]

            val = c_exp.split(",")
            c_exp = str(aux_list[0]) + ':' + val[0][1] + ', '
            
            for num in range(1, len(aux_list) - 1):
                c_exp += str(aux_list[num]) + ':' + val[num][1] + ', '
            
            c_exp += str(aux_list[len(aux_list) - 1]) + ':' + val[len(aux_list) - 1][1]
            
        if(len(exp.childs) > 1):
            c_exp = c_exp + self.ConcatEvaluator(exp.childs[1])
        
        return c_exp


    def ConditionalEvaluator(self, leaf):
        """ Definicion del metodo [ConditionalEvaluator], el cual se encarga de hacer 
        el tratamiento a las hojas del tipo Condicional.

        recibe: leaf : hoja a Evaluar.
        """
        exp = self.ExpressionEvaluator(leaf.childs[0])
        if(exp):
            self.SyntaxTreeContextEvaluator(leaf.childs[1])
            return
        if(len(leaf.childs) > 2):
            self.ConditionalEvaluator(leaf.childs[2])


    def ExpressionEvaluator(self, expression):
        """ Definicion del metodo [ExpressionEvaluator], el cual se encarga de hacer 
        el tratamiento a toda hoja del tipo expresion.

        recibe: expression : hoja a Evaluar.
        """
        if (expression.p_type == 'Terminal'):
            if (len(expression.childs)>0):
                t = self.ExpressionEvaluator(expression.childs[0])
                return t
            else:
                if (expression.c_type == 'var'):
                    t = self.getValue(expression.c_lexeme)
                    
                    if(t == False):
                        if expression.c_lexeme in self.SymbolsTable[0]:
                            t = self.SymbolsTable[0][expression.c_lexeme]
                    
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
            var = self.getValue(expression.childs[0])

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
                
                return t.array_toList[index]

            else:
                index = self.ExpressionEvaluator(expression.childs[0])
                val = self.ExpressionEvaluator(expression.childs[1])

                exp_val = expression
                if(isinstance(expression.p_value, SyntaxLeaf)):
                    exp_to_evaluate = []
                    while(isinstance(exp_val.p_value, SyntaxLeaf)):
                        exp_to_evaluate.append(exp_val.p_value)
                        exp_val = exp_val.p_value
                    
                    t = self.getValue(exp_val.p_value, None, None)

                    aux_list = [x for x in range(t.array_indexes[0], t.array_indexes[1]+1)]

                    for exp in exp_to_evaluate[::-1]:
                        exp_index = self.ExpressionEvaluator(exp.childs[0])
                        exp_val = self.ExpressionEvaluator(exp.childs[1])
                
                        if(exp_index > t.array_indexes[1] or exp_index < t.array_indexes[0]):
                            print("[Context Error] line " + str(expression.p_line) + ' column '+\
                            str(expression.p_column)+ '. Array expression out of boundaries.')
                            sys.exit(0)
                
                        t.array_toList[aux_list.index(exp_index)] = exp_val
                else:
                    t = self.getValue(expression.p_value, None, None)
                
                aux_list = [x for x in range(t.array_indexes[0], t.array_indexes[1]+1)]
                
                if(index > t.array_indexes[1] or index < t.array_indexes[0]):
                        print("[Context Error] line " + str(expression.p_line) + ' column '+\
                            str(expression.p_column)+ '. Array expression out of boundaries.')
                        sys.exit(0)
                
                t.array_toList[aux_list.index(index)] = val
                return t.array_toList

        elif(expression.p_type == 'Expression'):
            t = self.ExpressionEvaluator(expression.childs[0])
            return t


    def setValue(self, var, val, index=None, is_array=False):
        #Aqui recibira la tabla e ira asignando e imprimiendo errores
        if (len(self.SymbolsTable) > 0):
            for i in range(len(self.SymbolsTable)):
                if var in self.SymbolsTable[i]:
                    self.SymbolsTable[i][var].s_asignvalue = val

                    if(self.SymbolsTable[i][var].is_array):
                        self.SymbolsTable[i][var].array_toList = val
        
        # Sino impresion de errores

    def getValue(self, var, isIndex=None, isControl=None):
        if (len(self.SymbolsTable) > 0):
            for i in range(1, len(self.SymbolsTable)):
                if var in self.SymbolsTable[i]:
                    
                    if(isControl != None):
                        return self.SymbolsTable[i][var]
                    
                    if(isIndex != None):
                        if(self.SymbolsTable[i][var].is_array):
                            if(isIndex < self.SymbolsTable[i][var].array_indexes[0] or isIndex > self.SymbolsTable[i][var].array_indexes[1]):
                                print('[Interpreter Error] Index ' + isIndex + ' is out of boundaries')
                    
                    return self.SymbolsTable[i][var]

        return False