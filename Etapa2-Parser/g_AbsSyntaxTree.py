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
                if (leaf._type == "Declare"):
                    print(identation, leaf._type)
                    identation = identation + TAB
                    PrintVariable(leaf.childs[0], identation)
                elif (leaf._type == "Content"):
                    PrintContent(leaf, identation)


def PrintContent(syntaxLeaf, identation):
    if (len(syntaxLeaf.childs) == 1):
        child = syntaxLeaf.childs[0]

        if (child._type == "Instruction"):
            PrintInstruction(child, identation)
        elif (child._type == "Block"):
            SyntaxTreePrinter(child, identation)
    elif (len(syntaxLeaf.childs) == 2):
        for leaf in syntaxLeaf.childs:
            if(leaf._type == "Instruction"):
                PrintInstruction(child, identation)
            elif(leaf._type == "Block"):
                SyntaxTreePrinter(leaf, identation)
            elif(leaf._type == "Content"):
                PrintContent(leaf, identation)


def PrintInstruction(syntaxLeaf, identation):
    child = syntaxLeaf.childs[0]

    if(child._type == "Conditional"):
        print(identation, "If")
        identation = identation + TAB
        PrintConditional(child, identation)
    #elif(child._type == "Forloop"):
        #PrintForLoop
    #elif(child._type == "DoLoop"):
        #PrintDoLoop
    elif(child._type == "Asign"):
        PrintAsign(child, identation)
    elif(child._type == "Input"):
        PrintInput(child, identation)
    elif(child._type == "Output"):
        PrintOutput(child, identation)


def PrintConditional(syntaxLeaf, identation):
    print(identation, "Guard")
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        if(leaf._type == "RelationalOperator"):
            PrintRelationalOp(leaf, identation)
        elif(leaf._type == "BooleanOperator"):
            PrintBooleanOp(leaf, identation)
        elif(leaf._type == "Content"):
            PrintContent(leaf, identation)
        elif(leaf._type == "Guard"):
            PrintConditional(leaf, identation)


def PrintAsign(syntaxLeaf, identation):
    print(identation, syntaxLeaf.value)
    identation = identation + TAB

    PrintExpression(syntaxLeaf.childs[0], identation)


def PrintInput(syntaxLeaf, identation):
    print(identation, syntaxLeaf.value)
    identation = identation + TAB

    print(identation, "Ident:", syntaxLeaf.childs[0])

def PrintOutput(syntaxLeaf, identation):
    if(syntaxLeaf.value == "Print"):
        print(identation, "Print")
        identation = identation + TAB
    elif(syntaxLeaf.value == "Println"):
        print(identation, "Println")
        identation = identation + TAB
    
    for leaf in syntaxLeaf.childs:
        if(leaf._type == "Expression"):
            PrintExpression(leaf, identation)
        else:
            PrintConcatExp(leaf, identation)

def PrintConcatExp(syntaxLeaf, identation):
    print(identation, "Concat")
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        if(leaf._type == "Expression"):
            PrintExpression(leaf, identation)
        else:
            PrintConcatExp(leaf, identation)

def PrintVariable(syntaxLeaf, identation):
    if(len(syntaxLeaf.childs) > 0):
        print(identation, "Ident:", syntaxLeaf.value)

        PrintVariable(syntaxLeaf.childs[0], identation)
    else:
        print(identation, "Ident:", syntaxLeaf.value)
        identation = identation + TAB


def PrintExpression(syntaxLeaf, identation):
    child = syntaxLeaf.childs[0]

    print(identation, "Exp")
    identation = identation + TAB

    if (child._type == "AritmeticOperator"):
        PrintAritmeticOp(child, identation) 
    elif (child._type == "Terminal"):
        PrintTerminal(child, identation)
    elif (child._type == "RelationalOperator"):
        PrintRelationalOp(child, identation)
    elif (child._type == "BooleanOperator"):
        PrintBooleanOp(child, identation)
    elif (child._type == "StrOperator"):
        PrintStrOp(child, identation)
    #elif (child._type == "ArrayOperator"):
        #PrintArrayOp
    #elif(child._type == "ArrayExpression"):
        #PrintArrayExp

# TO DO: Tal vez unir todas las funciones que son de esta forma en una sola
#        que se llame PrintOperations o algo asi
def PrintAritmeticOp(syntaxLeaf, identation):
    print(identation, syntaxLeaf.value)
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation)


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


def PrintRelationalOp(syntaxLeaf, identation):
    print(identation, syntaxLeaf.value)
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation)


def PrintBooleanOp(syntaxLeaf, identation):
    print(identation, syntaxLeaf.value)
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation)

def PrintStrOp(syntaxLeaf, identation):
    print(identation, "Concat")
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        print(identation, leaf)