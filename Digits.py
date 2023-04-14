from enum import Enum

gDebugPrint = False

Ops = Enum('Ops', ['MULTIPLY', 'ADD', 'SUBTRACT', 'DIVIDE'])

class OpNode:
    def __init__(self, l, r, operation, val=None, isLeaf=False):
        self.left = l
        self.right = r
        self.op = operation
        self.val = val
        self.isLeaf = isLeaf

    def opAsString(self):
        if self.val:
            return ''
        elif self.op == Ops.ADD:
            return '+'
        elif self.op == Ops.SUBTRACT:
            return '-'
        elif self.op == Ops.DIVIDE:
            return '/'
        else:
            return '*'

    def value(self):
        if( self.isLeaf ):
            return self.val
        if self.op == Ops.ADD:
            return self.left + self.right
        elif self.op == Ops.SUBTRACT:
            return self.left - self.right
        elif self.op == Ops.DIVIDE:
            #There is probably a bug here!
            return self.left / self.right
        else:
            # self.op == Op.MULTIPLY
            #There is probably a bug here!
            return self.left * self.right

    # adding two objects
    def __add__(self, o):
        return self.value() + o.value()

    # subtracting two objects
    def __sub__(self, o):
        return self.value() - o.value()

    # multiplying two objects
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
        elif self.op == Ops.ADD:
            return f'({str(self.left)} + {str(self.right)})'
        elif self.op == Ops.SUBTRACT:
            return f'({str(self.left)} - {str(self.right)})'
        elif self.op == Ops.DIVIDE:
            return f'({str(self.left)} / {str(self.right)})'
        else:
            # self.op == Op.MULTIPLY
            return f'({str(self.left)} * {str(self.right)})'

def debugPrint( input ):
    if gDebugPrint:
        print(input)

# Make an enum for operations

# Make a class which is a tree node, has an operation, a left, right, and a value.
# value and (operation, left, right) are "nullable" and mutually exclusive
# Has a print method which prints out the full expression
# Should have an alternate print method which provides one operation per line,
# or maybe print as a tree (hard to do in text, take a lot of time?)


# To unit test - alternate format of question:
# Target
# Number-1 ... Number-6
# (Solution) 

# After debugging why it produces a wrong answer, put the numbers in the order of a good answer,
# and figure out what that's not working

# Returns a tree of operations with the provided list of numbers that achieves a total of "target"
# Note: intermediate results along the way must be non-negative whole numbers (is zero accepted?)
# Method should end up memoized for efficiency
def recursiveSolveAlternate(target, numlist):
    #base case
    if( len(numlist) == 2):
        for op in Ops:
            left = OpNode(None, None, None, numlist[0], True)
            right = OpNode(None, None, None, numlist[1], True)
            tree = OpNode(left, right, op, None, False)
            value = tree.value()
            if value == target and isinstance(value, int) and value >= 0:
                return tree
            if op is Ops.DIVIDE or op is Ops.SUBTRACT:
                left = OpNode(None, None, None, numlist[1], True)
                right = OpNode(None, None, None, numlist[0], True)
                tree = OpNode(left, right, op, None, False)
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
                         left = OpNode(None, None, None, num, True)
                         return OpNode(left, node, op.ADD, None, False)
                elif(op == Ops.SUBTRACT):
                        node = recursiveSolveAlternate(target+num, sublist)
                        if node:
                            if target >= num:
                                right = OpNode(None, None, None, num, True)
                                return OpNode(node, right, op.SUBTRACT, None, False)
                            else:
                                left = OpNode(None, None, None, num, True)
                                return OpNode(left, node, op.SUBTRACT, None, False)
                elif(op == Ops.MULTIPLY):
                    if( target % num == 0 ):
                        node = recursiveSolveAlternate(int(target / num), sublist)
                        if node:
                            left = OpNode(None, None, None, num, True)
                            return OpNode(left, node, op.MULTIPLY, None, False)
                #We're dealing with divide
                else:
                    if( num % target == 0):
                        node = recursiveSolveAlternate(int(num / target), sublist)
                        if node:
                            left = OpNode(None, None, None, num, True)
                            return OpNode(left, node, op.DIVIDE, None, False)
                    if( isinstance(target, int)):   
                        node = recursiveSolveAlternate(target * num, sublist)
                        if node:
                            right = OpNode(None, None, None, num, True)
                            return OpNode(node, right, op.DIVIDE, None, False)

            


#To do - find a way to more elegantly handle list sub-setting?
#To do - add additional parameter for depth so that we can know when to print the solution string, and rather than returning, continue on finding other solutions
#To do - clean up the print statements
#To do - parameterize print statements for different debugging levels (just use a darn function)
#To do - Consider outputing the equations as we go along for succesful cases (more difficult!)
#To do - unwind the steps to make it easier to use this tool to solve the puzzles
#To do - allow multiple puzzle entries per file
#To do - unit tests / test file
#To do - represent this as a tree, rather than doing all the string junk, which would make any formatting mechanism a breeze
def recursiveSolveNumbers(target, numlist, equationString):
    if numlist == []:
        return equationString
    if len(numlist) == 1:
        if numlist[0] == target:
            return str(target)
        else:
            return ''
    for item in numlist:
        #sublist = [ele for ele in numlist] #should probably be some duplicate function
        #if item in sublist:
        #    sublist = sublist.remove(item)
        # sublist = [ele for ele in numlist if ele != item]
        sublist = [ele for ele in numlist]
        sublist.remove(item)
        
        # check if the number we've got is larger than our target, so subtraction is a candidate
        if (item >= target): 
            debugPrint( f'Trying to get {int(item - target)} from {sublist} to SUBTR from {item} to achieve {target}') 
            attempt = recursiveSolveNumbers(item - target, sublist, equationString)
            if attempt != '':
                if( equationString == ''):
                    return "(" + str(item) + ") - (" + attempt + ")"
                return "(" + str(item) + ") - (" + equationString + ")"
        
        # check if the number we've got is smaller than our target, so addition is a candidate
        if (item <= target):
            debugPrint( f'Trying to get {int(target - item)} from {sublist} to ADD with {item} to achieve {target}') 
            attempt = recursiveSolveNumbers(target - item, sublist, equationString)
            if attempt != '':
                if( equationString == ''):
                    debugPrint(f'Got {item} + {attempt} = {target}')
                    return "(" + str(item) + ") + (" + attempt + ")"
                debugPrint(f'Got {item} + {equationString} = {target}')
                return "(" + str(item) + ") + (" + equationString + ")"
        
        #check if the number is an even factor of our target (remainder of division is 0), so multiplication is a candidate
        if (target % item == 0):
            debugPrint( f'Trying to get {int(target/item)} from {sublist} to MULT with {item} to achieve {target}')  
            attempt = recursiveSolveNumbers(int(target / item), sublist, equationString)
            if attempt != '':
                debugPrint(f'Got {item} * {attempt} = {target}')
                if( equationString == ''):
                    return "(" + str(item) + ") * (" + attempt + ")"
                debugPrint(f'Got {item} * {equationString} = {target}')
                return "(" + str(item) + ") * (" + equationString + ")"

        #check if the target is an even factor of our item (remainder of division is 0), so division is a candidate
        if target != 0 and (item / target) == 0:
            debugPrint( f'Trying to get {int(item/target)} from {sublist} to DIVIDE INTO {item} to achieve {target}') 
            attempt = recursiveSolveNumbers(int(item / target), sublist, equationString)
            if attempt != '':
                if( equationString == ''):
                    return "(" + str(item) + ") / (" + attempt + ")"
                return "(" + str(item) + ") / (" + equationString + ")"
 
        #check if we could get a multiple of item * target
        debugPrint( f'Trying to get {int(target*item)} from {sublist} to DIVIDE {item} into to achieve {target}') 
        attempt = recursiveSolveNumbers(int(target*item), sublist, equationString)
        if attempt != '':
            if( equationString == ''):
                debugPrint(f"Got {attempt} / {item} = {target}")
                return "(" + attempt + ") / (" + str(item) + ")"
            debugPrint(f"Got {equationString} - {item} = {target}")
            return "(" + equationString + ") / (" + str(item) + ")"

        #check if we could get the sum of target and item, so subtracting item at the end is a target
        debugPrint( f'Trying to get {int(target+item)} from {sublist} to SUBTR {item} FROM to achieve {target}') 
        attempt = recursiveSolveNumbers(target+item, sublist, equationString)
        if attempt != '':
            if( equationString == ''):
                debugPrint(f"Got {attempt} - {item} = {target}")
                return "(" + attempt + ") - (" + str(item) + ")"
            debugPrint(f"Got {equationString} - {item} = {target}")    
            return "(" + equationString + ") - (" + str(item) + ")"
    return equationString

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