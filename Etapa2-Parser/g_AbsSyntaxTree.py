#######################################
# CI3715 Traductores e Interpretadores
# Entrega 2. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################

# Defino una variable global que fija un Tab de
#espacio para la identacion del arbol.
TAB = '  '

class SyntaxLeaf:

    def __init__(self, _type, value = None, childs = None):
        self._type = _type
        self.value = value
        self.visited = False
        if childs:
            self.childs = childs
        else:
            self.childs = []


def SyntaxTreePrinter(syntaxLeaf, identation):
    if (syntaxLeaf):
        if(len(syntaxLeaf.childs) > 0):
            print(syntaxLeaf._type)
            identation = identation + TAB

            for leaf in syntaxLeaf.childs:
                if (leaf._type == "Block"):
                    identation = identation + TAB
                    print(identation, leaf._type)

                if (leaf._type == "Declare"):
                    print(identation, leaf._type)
                    identation = identation + TAB
                    PrintVariable(leaf.childs[0], identation)
                elif (leaf._type == "Expression"):
                    print(identation, leaf._type)
                    identation = identation + TAB
                    PrintExpression(leaf.childs[0], identation)
                else:
                    SyntaxTreePrinter(leaf, identation)

def PrintVariable(syntaxLeaf, identation):
    if(len(syntaxLeaf.childs) > 0):
        print(identation, "Ident:", syntaxLeaf.value)

        PrintVariable(syntaxLeaf.childs[0], identation)
    else:
        print(identation, "Ident:", syntaxLeaf.value)
        identation = identation + TAB

def PrintExpression(syntaxLeaf, identation):
    child = syntaxLeaf.childs[0]

    if (child._type == "AritmeticOperator"):
        PrintAritmeticOp(child, identation) 
    elif (child._type == "Terminal"):
        PrintTerminal(child, identation)
    #elif (child._type == "RelationalOperator"):
        #PrintRelationalOp
    #elif (child._type == "BooleanOperator"):
        #PrintBooleanOp
    #elif (child._type == "StrOperator"):
        #PrintStrOp
    #elif (child._type == "ArrayOperator"):
        #PrintArrayOp
    #elif(child._type == "ArrayExpression"):
        #PrintArrayExp

def PrintAritmeticOp(syntaxLeaf, identation):
    print(identation, syntaxLeaf._type)

    if syntaxLeaf:
        if(len(syntaxLeaf.childs) > 0):
            if(syntaxLeaf._type == "AritmeticOperator"):
                leftChild = syntaxLeaf.childs[0]
                rightChild = syntaxLeaf.childs[1]

                identation = identation + TAB
                
                PrintExpression(leftChild, identation)
                PrintExpression(rightChild, identation)

            elif(syntaxLeaf._type == "UnaryAritmeticOperator"):
                child = syntaxLeaf.childs[0]

                identation = identation + TAB
                
                PrintExpression(child, identation)

def PrintTerminal(syntaxLeaf, identation):
    if (len(syntaxLeaf.childs) == 0):
        if(syntaxLeaf.value is chr):
            print(identation, "Ident:", syntaxLeaf.value)
            identation = identation + TAB
        elif(syntaxLeaf.value is int):
            print(identation, "Literal:", syntaxLeaf.value)
            identation = identation + TAB
        else:
            print(identation, syntaxLeaf.value)
            identation = identation + TAB
    else:
        PrintTerminal(syntaxLeaf.childs[0], identation)
