import sys
import getopt
import copy

AND = "and"; OR = "or"; NOT = "not";

def sortsets(sos):
    # Sorting sets based on number of elements in set
    sos.sort(lambda x,y: cmp(len(x), len(y)))

def isliteral(sentencelist):
    # If its not a list it shud be a literal
    if(type(sentencelist) is not list):
        return True
    # If it is a list and num of elements is 1 or 0 return true
    if(len(sentencelist) < 2):
        return True

    return False

def isnot(clause):
    # Check if the connective is a 'not'
    if(clause[0] == NOT):
        return True
    else:
        return False

def isunitclause(clause):
    # If length of clause is one then it is a unit clause
    if(len(clause) == 1):
        return True
    else:
        return False

# To check if any unit clauses remain after unit clause cleanup
def hasunitclause(sos):
    # Sets are sorted, so first set will have least number of literals
    if(len(sos[0]) == 1):
        return True
    else:
        return False

# To check if the the entire set of sets is empty
def isempty(sos):
    if(len(sos) == 0):
        return True
    else:
        return False

# If empty set is present, then no assignment exists
# This function is used to end Unit Clause cleanup when an empty set is present
def emptysetpresent(sos):
    for clause in sos:
        if(len(clause)==0):
            return True
    return False

def createsetofsets(sentencelist):
    sets = []

    # Get the first connective
    connective = sentencelist[0]
    # If connective is AND create sets from all its clauses
    if(connective == AND):
        clausecount = len(sentencelist)
        for i in range(1,clausecount):
            clauseset = createsetfromclause(sentencelist[i])
            sets.append(clauseset)
    # First connective is not AND, so just one clause to create set from
    else:
        clauseset = createsetfromclause(sentencelist)
        sets.append(clauseset)

    return sets

def createsetfromclause(clause):
    clauseset = []

    # Get the connective
    connective = clause[0]

    # If connective is OR
    if(connective == OR):
        clausecount = len(clause)
        # Go through all the clauses
        for i in range(1, clausecount):
            # Get the literal associated with the subclause
            subcls = clause[i]
            # If it is a negation represent it with an _
            if(isnot(subcls)):
                lit = "_" + subcls[1]
            else:
                lit = subcls[0]
            # Append the literal to the clause set
            clauseset.append(lit)

    # If connective is NOT
    elif(isnot(clause)):
        # Its a negation, so represent it with an _
        lit = "_" + clause[1]
        # Append the literal to the clause set
        clauseset.append(lit)

    # If just a literal then create a unit clause with one literal
    elif(isliteral(clause)):
        clauseset.append(clause)

    return clauseset

# This function checks if the literal in unitclause is present in any other
# clauses
def ispresent(unitclause, clause):
    clauselen = len(clause)
    for lit in clause:
        if unitclause == lit:
            return True
    return False

# For Unit Clause cleanup we remove opposite literals from clauses
def removenegifpresent(unitclause, clause):
    clauselen = len(clause)
    for lit in clause:
        if unitclause == "_" + lit or "_" + unitclause == lit:
            clause.remove(lit)

# The main unit clause cleanup method that removes unit clauses and clauses that
# are related to the literal in the unit clause.
# If literal is present in a clause then remove the clause.
# If opposite of literal is present in clause then just remove that literal from
# clause.
def removeunitclause(sos):
    firstclause = sos[0]
    if(isunitclause(firstclause)):
        unitclause = sos.pop(0)[0]
        setcount = len(sos)
        i = 0
        while i < setcount:
            clause = sos[i]
            if(ispresent(unitclause, clause)):
                sos.pop(i)
                setcount = setcount - 1
            removenegifpresent(unitclause, clause)
            i = i + 1

        return unitclause
    return ""

def UnitClauseCleanup(sos, assignment):

    # Keep doing unit clause cleanup as long as there is a unit clause
    while(hasunitclause(sos)):
        # Remove one unit clause and process remaining clauses
        var = removeunitclause(sos)
        # Set the variable in unit clause to true, false if it is a negation
        if(var[0]=="_"):
            assignment.append(var[1] + "=false")
        else:
            assignment.append(var[0] + "=true")

        # After unitclause removal if there exists an empty set, then end it
        if(emptysetpresent(sos)):
            del assignment[:]
            assignment.append("false")
            return True

        # If the set of sets is empty, then DPLL is done
        if(isempty(sos)):
            assignment.insert(0,"true")
            return True

        # Sort the sets for next iteration
        sortsets(sos)

    return False

# This method checks where any pureclause literal exists in the set of sets
def findpureliteral(sos):
    checkedlist = []
    setcount = len(sos)
    if(setcount == 1):
        clause = sos[0]
        if(len(clause) > 0):
            return clause[0]
    for k in range(setcount):
        clause = sos[k]
        litcount = len(clause)
        for l in range(litcount):
            lit = clause[l]
            if(lit in checkedlist):
                continue
            for i in range(k+1,setcount):
                subcls = sos[i]
                subcount = len(subcls)
                for j in range(subcount):
                    if(subcls[j] == "_" + lit):
                        checkedlist.append(lit)
                        checkedlist.append("_"+lit)
                        break
                    if("_" + subcls[j] == lit):
                        checkedlist.append(lit)
                        checkedlist.append(subcls[j])
                        break
                if(lit in checkedlist):
                    break
            if(lit not in checkedlist):
                return lit
    return None

# This method removes all sets that contain the pure literal passed as argument
def removefromsos(lit, sos):
    setcount = len(sos)
    unassignedset = set()
    i = 0
    while i < setcount:
        clause = sos[i]
        if(ispresent(lit, clause)):
            unassignedset.update([x for x in clause if x!=lit])
            del sos[i]
            i = i - 1
        setcount = len(sos)
        i = i + 1
    return unassignedset

def EliminatePureClause(sos, assignment):

    assigned = set()
    # Find a pure clause literal
    lit = findpureliteral(sos)
    # Keep going until there are no more pure clause literals
    while (lit is not None):
        # Remove sets that contain the pure clause literal
        unassignedset = removefromsos(lit, sos)
        # Make valid assignment to pure clause literal
        if(lit[0]=="_"):
            assignment.append(lit[1] + "=false")
            assigned.add(lit[1])
        else:
            assignment.append(lit[0] + "=true")
            assigned.add(lit[0])

        # For the remaining variables in sets that were removed make assignments
        for var in unassignedset:
            if(var[0]=="_"):
                if(var[1] not in assigned):
                    assignment.append(var[1] + "=true")
                    assigned.add(var[1])
            else:
                if(var[0] not in assigned):
                    assignment.append(var[0] + "=false")
                    assigned.add(var[0])

        # After unitclause removal if there exists an empty set, then end it
        if(emptysetpresent(sos)):
            del assignment[:]
            assignment.append("false")
            return True

        # If the set of sets is empty, then DPLL is done
        if(isempty(sos)):
            assignment.insert(0,"true")
            return True

        # Continue pure clause removal process by finding next pureclause literal
        lit = findpureliteral(sos)


def DPLL(sos):
    # Sorting sets so that unit clauses are at beginning
    sortsets(sos)

    # Initialize assignment list
    assignment = []

    # UNIT CLAUSE CLEANUP STEP
    assignmentfound = UnitClauseCleanup(sos, assignment)
    if(assignmentfound):
        return assignment

    # PURE CLAUSE ELIMINATION STEP
    assignmentfound = EliminatePureClause(sos, assignment)
    if(assignmentfound):
        return assignment

    # Get first literal of first clause
    firstclause = sos[0]
    lit = firstclause[0]
    if(lit[0]=="_"):
        var = lit[1]
    else:
        var = lit[0]

    # Make copy of set of sets - we are going to modify it
    copylist = copy.deepcopy(sos)
    # Append unitclause with one literal
    sos.append([var])
    # Perform DPLL operations and check wheter it gives a valid assignment
    assignment = DPLL(sos)
    if(assignment == false):
        # Still no valid assignment so just with negation of literal
        copylist.append(["_"+var])
        assignment = DPLL(copylist)

    return assignment

def usage():
    print 'Usage: python DPLL.py -i inputfilename'

if __name__ == '__main__':

    # Get command line arguments
    try:
        optlist, args = getopt.gnu_getopt(sys.argv,'i:')
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    # Get filename argument
    filenamearg = [arg for opt, arg in optlist if opt=='-i']
    if(len(filenamearg)!=1):
        usage()
        sys.exit(2)

    # Open input file
    filename = filenamearg[0]
    try:
        inputfile = open(filename, 'r')
    except IOError as err:
        print(err)
        sys.exit(2)

    # Open Output file
    outputfile = open('CNF_satisfiability.txt', 'w')

    # Get N - number of sentences in input
    N = int(inputfile.readline())

    # Go throught all sentences and perform DPLL algorithm
    for i in range(N):
        # Read sentence from inputfile
        sentence = inputfile.readline()
        # Convert sentence to List
        sentencelist = eval(sentence)
        # Create Set of sets representation of CNF statement
        sos = createsetofsets(sentencelist)
        # Perform DPLL algorithm to get valid assignments
        assignment = DPLL(sos)
        # Write assignment to output file
        outputfile.write(str(assignment) + '\n')
