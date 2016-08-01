import time
from copy import copy
from logical_exp import *

def main(argv):
    model_dict = dict()
    if len(argv) != 4:
        print('Usage: %s [wumpus-rules-file] [additional-knowledge-file] [input_file]' % argv[0])
        sys.exit(0)
    try:
        input_file = open(argv[1], 'rb')
    except:
        print('failed to open file %s' % argv[1])
        sys.exit(0)
    print '\nLoading wumpus rules...'
    knowledge_base = logical_exp()
    knowledge_base.connective = ['and']
    for line in input_file:
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()
    try:
        input_file = open(argv[2], 'rb')
    except:
        print('failed to open file %s' % argv[2])
        sys.exit(0)
    print 'Loading additional knowledge...'
    for line in input_file:
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()
    if not valid_expression(knowledge_base):
        sys.exit('invalid knowledge base')
    try:
        input_file = open(argv[3], 'rb')
    except:
        print('failed to open file %s' % argv[3])
        sys.exit(0)
    print 'Loading statement...'
    input_statement = input_file.readline().rstrip('\r\n')
    input_file.close()
    counter = [0]
    statement = read_expression(input_statement, counter)
    if not valid_expression(statement):
        sys.exit('invalid statement')
################################################################## Above code is as per given in the sample program
################################################################## Below is the continuations for checking the entailment of the statement with KB.
    negative_statement = '(not %s)' %(input_statement) ########### Negation of statement, to check the 'definately false' condition
    counter = [0]
    neg_statement = read_expression(negative_statement, counter)
    if not valid_expression(neg_statement):
        sys.exit('Negative of the statment is invalid')
    demo=get_symbols(knowledge_base)    ########################## Getting all the symbols included in KB and statement
    demo=demo+get_symbols(statement)
    symbols=set(demo)

    for subexp in knowledge_base.subexpressions:    ############## Updating model with the truth values
        if subexp.connective[0] == '':
            symbol = subexp.symbol
            model_dict[symbol[0]] = True
            symbols.discard(symbol[0])
        elif subexp.connective[0] == 'not':
            symbol = subexp.subexpressions[0].symbol
            model_dict[symbol[0]] = False
            symbols.discard(symbol[0])

    print '\nChecking emtailement of the statement with KB: ',
    print_expression(statement, '')
    time1 = time.time()
    if_true  = tt_check_all(knowledge_base,statement,list(symbols),model_dict)  ### TT_entail for given statement
    if_false = tt_check_all(knowledge_base,neg_statement,list(symbols),model_dict) ## TT_entail for negation of the statement
    time2 = time.time()
    print '\ntime required to check entailment:', (time2-time1)
    file_writer = open('result.txt','w')
    if if_true:
        print_expression(statement,'')
        print " is definitely true"
        file_writer.write('definitely true')
    if if_false:
        print_expression(statement,'')
        print " is definitely false"
        file_writer.write('definitely false')
    if (not if_true) and (not if_false):
        print_expression(statement,'')
        print " is possibly true possibly false"
        file_writer.write('possibly true, possibly false')
    if if_true and if_false:
        print_expression(statement,'')
        print " is true as well as false"
        file_writer.write('both true and false')
    file_writer.close()

def get_symbols(smt):
    templist = []
    if smt.symbol[0]:
        templist.append(smt.symbol[0])
    else:
        for subexp in smt.subexpressions:
            templist = templist + get_symbols(subexp)
    return templist

def tt_check_all(knowledge_base, statement, symbols, model):    ##### check entailment against the model i.e kb + additional kb provided
    if len(symbols) == 0:
        if pl_true(knowledge_base, model):
            return pl_true(statement, model)
        else:
            return True
    else:
        firstsym = symbols.pop()
        temp = tt_check_all(knowledge_base, statement, copy(symbols), extend(firstsym,True, copy(model))) and \
               tt_check_all(knowledge_base, statement, copy(symbols), extend(firstsym,False, copy(model)))
        return temp

def pl_true(smt, model_dict):       ############################ Checking truth value of statements
    bool = None
    if smt.symbol[0] != '' and smt.connective[0] == '':
        bool = model_dict[smt.symbol[0]]

    elif smt.connective[0] == 'not':
        bool = not (pl_true(smt.subexpressions[0], model_dict))

    elif smt.connective[0] == 'if':
        bool = (not pl_true(smt.subexpressions[0],model_dict)) or pl_true(smt.subexpressions[1],model_dict)

    elif smt.connective[0] == 'iff':
        bool = pl_true(smt.subexpressions[0],model_dict) == pl_true(smt.subexpressions[1],model_dict)

    elif smt.connective[0] == 'or':
        bool = False
        templist = []
        for sub in smt.subexpressions:
            templist.append(pl_true(sub,model_dict))
        for tlist in templist:
            bool = bool or tlist

    elif smt.connective[0] == 'xor':
        bool = False
        templist = []
        for sub in smt.subexpressions:
            templist.append(pl_true(sub,model_dict))
        for r in templist:
            bool = bool != r
    elif smt.connective[0] == 'and':
        bool = True
        templist = []
        for sub in smt.subexpressions:
            templist.append(pl_true(sub,model_dict))
        for tlist in templist:
            bool = bool and tlist

    return bool

def extend(symbol, value, model):
    model[symbol] = value
    return model

if __name__ == '__main__':
    main(sys.argv)