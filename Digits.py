from enum import Enum

gDebugPrint = False

class Ops(Enum):
    MULTIPLY = "*"
    ADD = "+"
    SUBTRACT = "-"
    DIVIDE = "/"

    def __str__(self):
        if self.value == Ops.ADD:
            return '+'
        elif self.value == Ops.SUBTRACT:
            return '-'
        elif self.value == Ops.DIVIDE:
            return '/'
        else:
            return '*'

class OpNode:
    def __init__(self, l, r, operation, val, isLeaf):
        self.left = l
        self.right = r
        self.operation = operation
        self.val = val
        self.isLeaf = isLeaf

    @classmethod
    def leaf(cls, val):
        return cls(None, None, None, val, True)

    @classmethod
    def op(cls, l, r, operation):
        return cls(l, r, operation, None, False)

    def opAsString(self):
        if self.val:
            return ''
        return str(self.operation)

    def value(self):
        if( self.isLeaf ):
            return self.val
        if self.operation == Ops.ADD:
            return self.left + self.right
        elif self.operation == Ops.SUBTRACT:
            return self.left - self.right
        elif self.operation == Ops.DIVIDE:
            #There is probably a bug here!
            return self.left / self.right
        else:
            # self.op == Op.MULTIPLY
            #There is probably a bug here!
            return self.left * self.right

    def __add__(self, o):
        return self.value() + o.value()

    def __sub__(self, o):
        return self.value() - o.value()

    def __mul__(self, o):
        return self.value() * o.value()

    # dividing two objects (note we will return float values)
    def __truediv__(self, o):
        return 1.0*self.value() / o.value()

    def getEquationSteps(self):
        if self.isLeaf:
            return []
        else:
            leftSteps = self.left.getEquationSteps()
            rightSteps = self.right.getEquationSteps()
            left = self.left.value()
            op = self.opAsString()
            right = self.right.value()
            result = self.value()
            selfEquation = [f'{left} {op} {right} = {result}']

            return leftSteps + rightSteps + selfEquation

    def __str__(self):
        if( self.isLeaf ):
            return str(self.value())
        return f'({str(self.left)} {self.opAsString()} {str(self.right)})'


def debugPrint( input ):
    if gDebugPrint:
        print(input)


# Returns a tree of operations with the provided list of numbers that achieves a total of "target"
# Note: intermediate results along the way must be non-negative whole numbers, but zero is allowed
# Method should end up memoized for efficiency
def recursiveSolveAlternate(target, numlist):
    #base case
    if( len(numlist) == 2):
        for op in Ops:
            left = OpNode.leaf(numlist[0])
            right = OpNode.leaf(numlist[1])
            tree = OpNode.op(left, right, op)
            value = tree.value()
            if value == target and isinstance(value, int) and value >= 0:
                return tree
            if op is Ops.DIVIDE or op is Ops.SUBTRACT:
                left = OpNode.leaf(numlist[1])
                right = OpNode.leaf(numlist[0])
                tree = OpNode.op(left, right, op)
                value = tree.value()
                if value == target and isinstance(value, int) and value >= 0:
                    return tree
    else:
        for num in numlist:
            sublist = [ele for ele in numlist]
            sublist.remove(num)
            scratch = sublist
            for op in Ops:
                node = []
                if(op == Ops.ADD):
                    if( target - num >= 0):
                        node = recursiveSolveAlternate(target - num, sublist)
                        if node:
                         left = OpNode.leaf(num)
                         return OpNode.op(left, node, op.ADD)
                elif(op == Ops.SUBTRACT):
                        node = recursiveSolveAlternate(target+num, sublist)
                        if node:
                            if target >= num:
                                right = OpNode.leaf(num)
                                return OpNode.op(node, right, op.SUBTRACT)
                            else:
                                left = OpNode.leaf(num)
                                return OpNode.op(left, node, op.SUBTRACT)
                elif(op == Ops.MULTIPLY):
                    if( target % num == 0 ):
                        node = recursiveSolveAlternate(int(target / num), sublist)
                        if node:
                            left = OpNode.leaf(num)
                            return OpNode.op(left, node, op.MULTIPLY)
                #We're dealing with divide
                else:
                    if( num % target == 0):
                        node = recursiveSolveAlternate(int(num / target), sublist)
                        if node:
                            left = OpNode.leaf(num)
                            return OpNode.op(left, node, op.DIVIDE)
                    if( isinstance(target, int)):   
                        node = recursiveSolveAlternate(target * num, sublist)
                        if node:
                            right = OpNode.leaf(num)
                            return OpNode.op(node, right, op.DIVIDE)

#To do - unit tests / test file

def main():
    fname = "problem.txt"
    target = 0
    problemFile = open(fname, "r")
    problemLines = problemFile.readlines()
    for currentLine in problemLines:
        if not currentLine:
            break
        if currentLine[0] == '\n':
            continue

        # Lines of a problem to skip are marked with # symbol.
        # Skip the following line and the newline after it
        if currentLine[0] == '#':
            continue
        data = currentLine.split(':')
        target = int(data[0])
        numberList = list(map(int,data[1].split()))

        print(f'{target}: {numberList}')

        #result = recursiveSolveNumbers(target, numberList, "")
        result = recursiveSolveAlternate(target, numberList)
        print( f'{result} = {result.value()}' )
        for step in result.getEquationSteps():
            print(step)
        print()

if __name__ == "__main__":
    main()