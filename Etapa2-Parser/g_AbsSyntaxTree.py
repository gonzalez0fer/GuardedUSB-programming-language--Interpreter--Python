#######################################
# CI3715 Traductores e Interpretadores
# Entrega 2. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################

# Defino una variable global que fija un Tab de
#espacio para la identacion del arbol.
TAB = '\t'

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
    if syntaxLeaf:
        if(len(syntaxLeaf.childs)>0):
            for leaf in syntaxLeaf.childs:
                if leaf._type == 'Block':
                    identation = identation + TAB
                    print('\n', identation, leaf._type)

                elif (leaf._type == "Declare"):
                    print('\n', identation, leaf._type)
                    #DeclareLeafPrinter(i, tabs)

                elif (leaf._type == "Expression"):
                    print("\n")
                    #imprimirExp(i, tabs)