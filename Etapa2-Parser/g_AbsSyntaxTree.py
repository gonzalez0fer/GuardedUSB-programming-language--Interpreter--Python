#######################################
# CI3715 Traductores e Interpretadores
# Entrega 2. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################

# Defino una variable global que fija un Tab de
#espacio para la identacion del arbol.
TAB = '  '

# Diccionario de simbolos
symbols = {
    "+": "Plus",
    "-": "Minus",
    "*": "Mult",
    "/": "Div",
    "%": "Mod",
    "\\/": "Or",
    "/\\": "And",
    "!": "Not",
    "<": "Less",
    "<=": "Leq",
    ">=": "Geq",
    ">": "Greater",
    "==": "Equal",
    "!=": "NotEqual"
}

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
                    PrintDeclaration(leaf, identation)
                elif (leaf._type == "Content"):
                    PrintContent(leaf, identation)

def PrintDeclaration(syntaxLeaf, identation):
    for leaf in syntaxLeaf.childs:
        if(leaf._type == "Variable"):
            PrintVariable(leaf, identation)
        elif(leaf._type == "Declare"):
            PrintDeclaration(leaf, identation)

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
                PrintInstruction(leaf, identation)
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
        if(leaf._type == "Expression"):
            PrintExpression(leaf, identation)
        elif(leaf._type == "Content"):
            PrintContent(leaf, identation)
        elif(leaf._type == "Guard"):
            PrintConditional(leaf, identation)


def PrintAsign(syntaxLeaf, identation):
    print(identation, "Asig")
    identation = identation + TAB
    print(identation, "Ident:", syntaxLeaf.value)
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

    if (child._type == "AritmeticOperator"):
        print(identation, "Exp")
        identation = identation + TAB
        PrintAritmeticOp(child, identation) 
    elif (child._type == "Terminal"):
        PrintTerminal(child, identation)
    elif (child._type == "RelationalOperator"):
        print(identation, "Exp")
        identation = identation + TAB
        PrintRelationalOp(child, identation)
    elif (child._type == "BooleanOperator"):
        print(identation, "Exp")
        identation = identation + TAB
        PrintBooleanOp(child, identation)
    elif (child._type == "StrOperator"):
        print(identation, "Exp")
        identation = identation + TAB
        PrintStrOp(child, identation)
    #elif (child._type == "ArrayOperator"):
        #PrintArrayOp
    #elif(child._type == "ArrayExpression"):
        #PrintArrayExp

# TO DO: Tal vez unir todas las funciones que son de esta forma en una sola
#        que se llame PrintOperations o algo asi
def PrintAritmeticOp(syntaxLeaf, identation):
    print(identation, symbols[syntaxLeaf.value])
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation)


def PrintTerminal(syntaxLeaf, identation):
    if (len(syntaxLeaf.childs) == 0):
        if(isinstance(syntaxLeaf.value, int)):
            print(identation, "Literal:", syntaxLeaf.value)
            identation = identation + TAB
        elif(syntaxLeaf.value.isalpha() and len(syntaxLeaf.value) == 1):
            print(identation, "Ident:", syntaxLeaf.value)
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