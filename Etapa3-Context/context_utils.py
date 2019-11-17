import sys

def getArrayType(self,arr):
    if (arr.array == None):
        print("[Context Error] line " + str(self.c_currentline) +'. not an array type.')
        sys.exit(0)
    t = self.getTipoId(arr.array)
    if (t != 'int'):
        print("[Context Error] line " + str(self.c_currentline) +'. Incorrect Index type.')
        sys.exit(0)
    if (len(arr.childs)>0):
        for i in arr.childs:
            self.getArrayType(i)


def getType(self, arr):
    if (len(arr.childs) > 0):
        for i in arr.childs:
            p_type = self.getType(i)
            return p_type
    else:
        return arr.p_value