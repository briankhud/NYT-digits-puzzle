from enum import Enum

gDebugPrint = False
gOptimize = True

class Ops(Enum):
    MULTIPLY = "*"
    ADD = "+"
    SUBTRACT = "-"
    DIVIDE = "/"

    def __str__(self):
        return self.value

    def eval(self, left, right):
        if self.value == "+":
            return left + right
        elif self.value == "-":
            return left - right
        elif self.value == "/":
            #There is probably a bug here regarding int vs float!
            return left / right
        else:
            # self.op == Op.MULTIPLY
            #There is probably a bug here regarding int vs float!
            return left * right        

class OpNode:
    def __init__(self, l, r, operation, val, isLeaf):
        self.left = l
        self.right = r
        self.operation = operation
        self.val = val
        self.isLeaf = isLeaf
        self.cacheval = None

    @classmethod
    def leaf(cls, val):
        return cls(None, None, None, val, True)

    @classmethod
    def op(cls, l, r, operation):
        return cls(l, r, operation, None, False)

    def opAsString(self):
        if self.isLeaf:
            return ''
        return str(self.operation)

    def value(self):
        if( self.isLeaf ):
            return self.val
        else:
            if gOptimize:
                if not self.cacheval:
                    self.cacheval = self.operation.eval(self.left, self.right)
                return self.cacheval

            return self.operation.eval(self.left, self.right)

    def __add__(self, o):
        return self.value() + o.value()

    def __sub__(self, o):
        return self.value() - o.value()

    def __mul__(self, o):
        return self.value() * o.value()

    # dividing two objects (note we *will* return float values)
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
        else:
            return f'({str(self.left)} {self.opAsString()} {str(self.right)})'


def debugPrint( input ):
    if gDebugPrint:
        print(input)


# Returns a tree of operations with the provided list of numbers that achieves a total of "target"
# Note: intermediate results along the way must be non-negative whole numbers, but zero is
# Method should end up memoized for efficiency

def recursiveSolve(target, numlist):
    #base case
    if( len(numlist) == 2):
        for op in Ops:
            left = OpNode.leaf(numlist[0])  # A on left
            right = OpNode.leaf(numlist[1]) # B on right
            tree = OpNode.op(left, right, op)
            value = tree.value()
            if value == target and isinstance(value, int) and value >= 0:
                return tree

            # If A / B or A - B didn't work, let's reverse
            # it and try B / A or B - A
            if op is Ops.DIVIDE or op is Ops.SUBTRACT:
                left = OpNode.leaf(numlist[1])  #B on left
                right = OpNode.leaf(numlist[0]) #A on right
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
                        node = recursiveSolve(target - num, sublist)
                        if node:
                         left = OpNode.leaf(num)
                         return OpNode.op(left, node, op.ADD)
                elif(op == Ops.SUBTRACT):
                        node = recursiveSolve(target+num, sublist)
                        if node:
                            if target >= num:
                                right = OpNode.leaf(num)
                                return OpNode.op(node, right, op.SUBTRACT)
                            else:
                                left = OpNode.leaf(num)
                                return OpNode.op(left, node, op.SUBTRACT)
                elif(op == Ops.MULTIPLY):
                    if( target % num == 0 ):
                        node = recursiveSolve(int(target / num), sublist)
                        if node:
                            left = OpNode.leaf(num)
                            return OpNode.op(left, node, op.MULTIPLY)
                #We're dealing with divide
                else:
                    if( num % target == 0):
                        node = recursiveSolve(int(num / target), sublist)
                        if node:
                            left = OpNode.leaf(num)
                            return OpNode.op(left, node, op.DIVIDE)
                    if( isinstance(target, int)):   
                        node = recursiveSolve(target * num, sublist)
                        if node:
                            right = OpNode.leaf(num)
                            return OpNode.op(node, right, op.DIVIDE)

#Todo - unit tests / test file
#Todo - execution parameters for file name and display output options

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
        result = recursiveSolve(target, numberList)
        print( f'{result} = {result.value()}' )
        for step in result.getEquationSteps():
            print(step)
        print()

if __name__ == "__main__":
    main()