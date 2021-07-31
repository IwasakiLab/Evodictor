import numpy as np
import sys

def create_dataset(
    targetelem,
    sp2xelem2xweight,
    sp2yelem2yweight,
    tree, 
    predictor2elemlist, 
    predictor_list,
    mode, 
    gain_or_loss
    ):

    zero = 0.00000001

    SpXylist = []

    stack = [tree.clade]
    
    while (len(stack) > 0):

        node = stack.pop()

        #elemset_before = set([elem for elem, xweight in sp2xelem2xweight[node.name].items() if abs(xweight - 1) <= zero ])

        elem2weight = {elem:xweight for elem, xweight in sp2xelem2xweight[node.name].items()} if node.name in sp2xelem2xweight.keys() else {}

        if node.name not in sp2xelem2xweight.keys(): 
            print("Warning:", node.name, "does not have any elements!", sep = " ", file = sys.stderr)
            #sys.exit(1)

        yweight_before  = (sp2yelem2yweight[node.name][targetelem] if targetelem in sp2yelem2yweight[node.name].keys() else 0) if node.name in sp2yelem2yweight.keys() else 0
        for child in node.clades:

            if node.name not in sp2xelem2xweight.keys(): 
                print("Warning:", child.name, "does not have any elements!", sep = " ", file = sys.stderr)
                #sys.exit(1)

            yweight_after  = (sp2yelem2yweight[child.name][targetelem] if targetelem in sp2yelem2yweight[child.name].keys() else 0) if child.name in sp2yelem2yweight.keys() else 0

            if   ( gain_or_loss == 'gain' ):
                to_be_learned = ( abs(yweight_before - 0) <= zero ) and ( abs(yweight_after - 0.5) > zero )
            elif ( gain_or_loss == 'loss' ):
                to_be_learned = ( abs(yweight_before - 1) <= zero ) and ( abs(yweight_after - 0.5) > zero )
            
            stack.append(child)

            if (to_be_learned):

                X = elem_weight2vec(
                    targetelem         = targetelem        ,
                    elem2weight        = elem2weight       ,
                    predictor2elemlist = predictor2elemlist,
                    predictor_list     = predictor_list    ,
                    mode               = mode
                    )
                
                if ( abs(abs(yweight_after - yweight_before) - 1) <= zero ):
                    y = 1
                else:
                    y = 0
                
                SpXylist.append((node.name, X, y))

    return SpXylist

def elem_weight2vec(
    targetelem,
    elem2weight, 
    predictor2elemlist, 
    predictor_list,
    mode
    ):

    if ( mode == "define" ):

        X = []

        for predictor in predictor_list:

            weight_sum = 0

            for elem in predictor2elemlist[predictor]:

                weight_sum += (elem2weight[elem] if elem in elem2weight.keys() else 0)

            X.append( weight_sum )
    
    return X


def elemset2vec(
    targetelem,
    elemset, 
    predictor2elemlist, 
    predictor_list,
    mode
    ):

    if ( mode == "define" ):

        X = []

        for predictor in predictor_list:

            predictor_elemset = set(predictor2elemlist[predictor])

            X.append( len(elemset & predictor_elemset) )
    
    return X

def listup_extant_X( # ExSpX_list = [(name, [float, float, ...]), (), (), ...]
    targetelem,
    sp2xelem2xweight, 
    tree, 
    predictor2elemlist, 
    predictor_list,
    mode, 
    ):

    zero = 0.00000001

    ExSpXlist = []

    for node in tree.get_terminals():

        elemset = set([elem for elem, xweight in sp2xelem2xweight[node.name].items() if abs(xweight - 1) <= zero ])

        X = elemset2vec(
            targetelem         = targetelem        ,
            elemset            = elemset           ,
            predictor2elemlist = predictor2elemlist,
            predictor_list     = predictor_list    ,
            mode               = mode
            )
            
        ExSpXlist.append((node.name, X))
    
    return ExSpXlist