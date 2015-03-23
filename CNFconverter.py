import sys
import getopt

NOT = "not"; AND = "and"; OR = "or"; IMPL = "implies"; BIMPL = "iff";
UCONN = [NOT]; BCONN = [IMPL,BIMPL]; MCONN = [AND, OR]

def isliteral(sentencelist):
    if(type(sentencelist) is not list):
        return True
    if(len(sentencelist) < 2):
        return True
    return False

def biconditionalelimination(sentencelist):

    # If sentence is a literal then just return it
    if(isliteral(sentencelist)):
        return sentencelist

    # Get the connective of the sentence list
    connective = sentencelist[0]

    # If connective is unary then perform elimination on one clause
    if connective in UCONN:
        sentencelist[1] = biconditionalelimination(sentencelist[1])
        return sentencelist

    # If connective is binary then perform elimination on two clauses
    elif connective in BCONN:
        sentencelist[1] = biconditionalelimination(sentencelist[1])
        sentencelist[2] = biconditionalelimination(sentencelist[2])

        # If connective is biconditional then perform conversion
        if(connective == BIMPL):
            sentencelist[0] = AND
            sentencelist[1] = [IMPL, sentencelist[1], sentencelist[2]]
            sentencelist[2] = [IMPL, sentencelist[2], sentencelist[1]]

        return sentencelist

    # If connective has multiple clauses then perform elimination on all clauses
    elif connective in MCONN:
        clausecount = len(sentencelist)
        for i in range(1, clausecount):
            sentencelist[i] = biconditionalelimination(sentencelist[i])
        return sentencelist

    # Handle unidentified connective
    else:
        print 'Connective \'' + connective + '\' is not defined.'
        sys.exit(2)


def implicationelimination(sentencelist):
    # If sentence is a literal then just return it
    if(isliteral(sentencelist)):
        return sentencelist

    # Get the connective of the sentence list
    connective = sentencelist[0]

    # If connective is unary then perform elimination on one clause
    if connective in UCONN:
        sentencelist[1] = implicationelimination(sentencelist[1])
        return sentencelist

    # If connective is binary then perform elimination on two clauses
    elif connective in BCONN:
        sentencelist[1] = implicationelimination(sentencelist[1])
        sentencelist[2] = implicationelimination(sentencelist[2])

        # If connective is implication then perform conversion
        if(connective == IMPL):
            sentencelist[0] = OR
            sentencelist[1] = [NOT, sentencelist[1]]
            sentencelist[2] = sentencelist[2]

        return sentencelist

    # If connective has multiple clauses then perform elimination on all clauses
    elif connective in MCONN:
        clausecount = len(sentencelist)
        for i in range(1, clausecount):
            sentencelist[i] = implicationelimination(sentencelist[i])
        return sentencelist

    # Handle unidentified connective
    else:
        print 'Connective \'' + connective + '\' is not defined.'
        sys.exit(2)

def demorganslaw(sentencelist):

    # If sentence is a literal then just return it
    if(isliteral(sentencelist)):
        return sentencelist

    # Get the connective of the sentence list
    connective = sentencelist[0]

    # If connective is unary then perform demorgans on one clause
    if connective in UCONN:
        clause1 = demorganslaw(sentencelist[1])
        sentencelist[1] = clause1

        # If connective is NOT then perform demorgan conversion
        if connective == NOT:
            if(type(clause1) is list):
                subconn = clause1[0]
                if(subconn in MCONN):
                    if(subconn is AND):
                        sentencelist[0] = OR
                    elif(subconn is OR):
                        sentencelist[0] = AND
                    sentencelist[1] = [NOT, clause1[1]]
                    sentencelist[1] = demorganslaw(sentencelist[1])
                    for i in range(2,len(clause1)):
                        sentencelist.append([NOT, clause1[i]])
                        sentencelist[i] = demorganslaw(sentencelist[i])

        return sentencelist

    # If connective has multiple clauses then perform demorgans on all clauses
    elif connective in MCONN:
        clausecount = len(sentencelist)
        for i in range(1, clausecount):
            sentencelist[i] = demorganslaw(sentencelist[i])
        return sentencelist

    # Handle unidentified connective
    else:
        print 'Connective \'' + connective + '\' is not defined.'
        sys.exit(2)

def doublenegationelimination(sentencelist):

    # If sentence is a literal then just return it
    if(isliteral(sentencelist)):
        return sentencelist

    # Get the connective of the sentence list
    connective = sentencelist[0]

    # If connective is unary then perform elimination on one clause
    if connective in UCONN:
        clause1 = doublenegationelimination(sentencelist[1])
        sentencelist[1] = clause1

        # If connective is NOT then perform double negation elimination
        if connective == NOT:
            if(type(clause1) is list):
                subconn = clause1[0]
                if(subconn is NOT):
                    sentencelist = clause1[1]
        return sentencelist

    # If connective has multiple clauses then perform elimination on all clauses
    elif connective in MCONN:
        clausecount = len(sentencelist)
        for i in range(1, clausecount):
            sentencelist[i] = doublenegationelimination(sentencelist[i])
        return sentencelist

    # Handle unidentified connective
    else:
        print 'Connective \'' + connective + '\' is not defined.'
        sys.exit(2)

def distributivity(sentencelist):
    # If sentence is a literal then just return it
    if(isliteral(sentencelist)):
        return sentencelist

    # Get the connective of the sentence list
    connective = sentencelist[0]

    # If connective is unary then perform distributivity on one clause
    if connective in UCONN:
        sentencelist[1] = distributivity(sentencelist[1])
        return sentencelist

    # If connective is unary then perform distributivity on multiple clause
    elif connective in MCONN:
        clause1 = distributivity(sentencelist[1])
        clause2 = distributivity(sentencelist[2])
        if(connective == OR):
            if(type(clause1) is list or type(clause2) is list):
                if(type(clause2) is list and clause2[0] is AND):
                    sentencelist[0] = AND
                    sentencelist[1] = [OR, clause1, clause2[1]]
                    sentencelist[2] = [OR, clause1, clause2[2]]
                elif(type(clause1) is list and clause1[0] is AND):
                    sentencelist[0] = AND
                    sentencelist[1] = [OR, clause2, clause1[1]]
                    sentencelist[2] = [OR, clause2, clause1[2]]
        return sentencelist

    # Handle unidentified connective
    else:
        print 'Connective \'' + connective + '\' is not defined.'
        sys.exit(2)


def associativity(sentencelist):
    # If sentence is a literal then just return it
    if(isliteral(sentencelist)):
        return sentencelist

    # Get the connective of the sentence list
    connective = sentencelist[0]

    # If connective is unary then perform reduction on one clause
    if connective in UCONN:
        sentencelist[1] = associativity(sentencelist[1])
        return sentencelist

    elif connective in MCONN:
        clausecount = len(sentencelist)
        i = 1
        while i < clausecount:
            sentencelist[i] = associativity(sentencelist[i])
            clause = sentencelist[i]
            j = 2
            if(clause[0]==connective):
                sentencelist[i] = clause[1]
                clcnt = len(clause)
                for j in range(2, clcnt):
                    sentencelist.insert(i, clause[j])
                clausecount = len(sentencelist)
            i = i + j - 1
        return sentencelist

    # Handle unidentified connective
    else:
        print 'Connective \'' + connective + '\' is not defined.'
        sys.exit(2)

def removeduplicates(sentencelist):
    # If sentence is a literal then just return it
    if(isliteral(sentencelist)):
        return sentencelist

    # Get the connective of the sentence list
    connective = sentencelist[0]

    # If connective is unary, no need to check for duplicates
    if connective in UCONN:
        return sentencelist

    elif connective in MCONN:
        clausecount = len(sentencelist)
        sentencerep = []
        for i in range(1, clausecount):
            sentencelist[i] = removeduplicates(sentencelist[i])
            clause = sentencelist[i]
            if(isliteral(clause)):
                sentencerep.append(set(clause))
            elif(clause[0] == NOT):
                sentencerep.append(set(clause[1].lower()))
            else:
                subset = set()
                connective = clause[0]
                litcount = len(clause)
                for j in range(1, litcount):
                    subcls = clause[j]
                    if(subcls[0] == NOT):
                        subset.add(subcls[1].lower())
                    else:
                        subset.add(subcls[0])
                sentencerep.append(subset)
        remove = []
        for i in range(0,clausecount-1):
            for j in range(i+1, clausecount-1):
                result = sentencerep[i].symmetric_difference(sentencerep[j])
                if(len(result)==0):
                    remove.append(i+1)
                    break
        for i in remove:
            del sentencelist[i]

    return sentencelist

def usage():
    print 'Usage: python CNFConverter.py -i inputfilename'

if __name__ == '__main__':

    # Get Command Line Arguments
    try:
        optlist, args = getopt.gnu_getopt(sys.argv,'i:')
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    # Get Filename from Arguments
    filenamearg = [arg for opt,arg in optlist if opt=='-i']
    if(len(filenamearg) != 1):
        usage()
        sys.exit(2)
    filename = filenamearg[0]

    # Open Input file
    try:
        inputfile = open(filename, 'r')
    except IOError as err:
        print(err)
        sys.exit(2)

    # Open Output file
    outputfile = open('sentences_CNF.txt', 'w')

    # Read N from inputFile (N is the number of input sentences)
    N = int(inputfile.readline())

    # Go through N lines and convert each sentence to CNF
    for i in range(N):

        # Read Line from inputfile
        sentence = inputfile.readline()

        # Convert sentence from string to list
        sentencelist = eval(sentence)

        # Perform CNF conversion operations
        sentencelist = biconditionalelimination(sentencelist)
        sentencelist = implicationelimination(sentencelist)
        sentencelist = demorganslaw(sentencelist)
        sentencelist = doublenegationelimination(sentencelist)
        sentencelist = distributivity(sentencelist)
        sentencelist = distributivity(sentencelist)
        sentencelist = associativity(sentencelist)
        sentencelist = removeduplicates(sentencelist)

        # Write CNF sentence to output file
        outputfile.write(str(sentencelist) + '\n')
