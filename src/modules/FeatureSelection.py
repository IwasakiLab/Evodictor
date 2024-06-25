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

        def mutual_info_classif_zero(X, y):
            return mutual_info_classif(X, y, random_state=0) # fix random_state as 0
        
        selector = SelectKBest(score_func=mutual_info_classif_zero, k=k, ) 
        selector.fit(X_array, y_array)
        scores   = selector.scores_

    elif (method == "Odds"): # Log odds ratio based on a contingency table of "possess OG X (feature) in the branch's parent or not" vs "gain/lose OG Y (predicted OG) at the branch or not"

        # feasibility check (all values in X are required to be 0, 1, or 0.5)
        X_unique_list = np.unique(X_array.flatten())
        if len(set(X_unique_list) - set([0,1,0.5])) != 0:
            print("Error: all values in X are required to be 0, 1, or 0.5 when you specify -m Odds")
            print("X contained ", X_unique_list)
            sys.exit()
        
        # convert 0.5
        X_floor = np.floor(X_array) # 0.5 -> 0
        X_ceil  = np.ceil(X_array)  # 0.5 -> 1

        # count branches with Haldane Correction
        count_1_1 = np.dot(X_floor.T, y_array)      + 0.5 # pre-exist: True, acquire: True
        count_1_0 = np.dot(X_floor.T, 1-y_array)    + 0.5 # pre-exist: True, acquire: False
        count_0_1 = np.dot((1-X_ceil).T, y_array)   + 0.5 # pre-exist: False, acquire: True
        count_0_0 = np.dot((1-X_ceil).T, 1-y_array) + 0.5 # pre-exist: False, acquire: False

        # conduct fisher_exact test + odds ratio calculation
        logoddsratio_list = [np.log10((nTT*nFF)/(nFT*nTF)) for nFF, nFT, nTF, nTT in zip(count_0_0, count_0_1, count_1_0, count_1_1)]
        
        if (method == "Odds"): 
            scores = logoddsratio_list
            signed = False # because the scores are signed by default

        # statistical tests with multiple test correction
        #df_count["p"] = [fisher_exact([[nFF, nFT], [nTF, nTT]], alternative='two-sided').pvalue for nFF, nFT, nTF, nTT in zip(df_count["FF"], df_count["FT"], df_count["TF"], df_count["TT"])]
        #df_count["q"] = multipletests(df_count["p"], method="fdr_bh")[1]


    # get sign information: judge mean({x | y(x) = 1}) > mean({x | y(x) = 0}) or not
    if (signed):
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
            
            if (mean(xlist_one) >= mean(xlist_zero)):
                scores[j] = scores[j]
            else:
                scores[j] = -1 * scores[j]

    # convert nan into 0
    for i in range(len(scores)):
        if np.isnan(scores[i]):
            scores[i] = 0
    return scores#, mask