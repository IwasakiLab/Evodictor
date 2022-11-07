import numpy as np
from scipy.stats import rankdata
from statistics import mean
import sys


def FeatureSelection(
    X_array, 
    y_array, 
    method, 
    k,
    # anova args
    signed,
    # random forest args
    n_estimators = 100,
    max_depth = 2,
    class_weight = "balanced"
    ):

    if class_weight == "none": class_weight = None

    if (method == "ANOVA"):
        from sklearn.feature_selection import SelectKBest
        from sklearn.feature_selection import f_classif
        
        selector = SelectKBest(score_func=f_classif, k=k) 
        selector.fit(X_array, y_array)
        scores   = selector.scores_

        # judge mean({x | y(x) = 1}) > mean({x | y(x) = 0}) or not
        for j in range(len(X_array[0])):
            xlist_one = []
            xlist_zero = []
            for i in range(len(X_array)):
                if(y_array[i] == 1):
                    xlist_one.append(X_array[i][j])
                elif(y_array[i] == 0):
                    xlist_zero.append(X_array[i][j])
                else:
                    print("Warning: X_array["+str(i)+"]["+str(j)+"] = "+str(X_array[i][j]), file = sys.stderr)

            if (signed):
                if (mean(xlist_one) >= mean(xlist_zero)):
                    scores[j] = scores[j]
                else:
                    scores[j] = -1 * scores[j]
    
    elif (method == "RF"):

        from sklearn.feature_selection import SelectFromModel
        from sklearn.ensemble import RandomForestClassifier

        print ("RandomForestClassifier papameters:", file=sys.stderr)
        print ("n_estimators:", n_estimators, file=sys.stderr)
        print ("max_depth:", max_depth, file=sys.stderr)
        print ("random_state:", 0, file=sys.stderr)
        print ("class_weight:", class_weight, file=sys.stderr)

        selector = SelectFromModel(
            RandomForestClassifier(n_estimators = n_estimators, max_depth = max_depth, random_state=0, class_weight = class_weight),  # n_estimators = 100 is the default
            threshold=-np.inf, 
            max_features=k
            )  
        
        selector.fit(X_array, y_array)
        scores = selector.estimator_.feature_importances_

    elif (method == "MI"):

        from sklearn.feature_selection import SelectKBest
        from sklearn.feature_selection import mutual_info_classif
        
        selector = SelectKBest(score_func=mutual_info_classif, k=k, random_state=0, ) 
        selector.fit(X_array, y_array)
        scores   = selector.scores_

    # convert nan into 0
    for i in range(len(scores)):
        if np.isnan(scores[i]):
            scores[i] = 0
    return scores#, mask