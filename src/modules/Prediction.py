# import modules
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve
import random
import numpy as np
import sys

def fitting(
    X_array, 
    y_array, 
    model,
    random_seed,
    # logistic regression args
    lr_penalty,
    lr_solver,
    # random forest args
    n_estimators = 100,
    max_depth = 2,
    class_weight = "balanced"
    ):

    if class_weight == "none": class_weight = None

    if (model == "LR"):
        
        discr = LogisticRegression(penalty = lr_penalty, solver = lr_solver)
        discr.fit(X_array,y_array)

        intercept = discr.intercept_[0]
        coef      = discr.coef_[0]

        return coef, intercept, discr
    
    elif (model == "RF"):

        print ("RandomForestClassifier papameters:", file=sys.stderr)
        print ("n_estimators:", n_estimators, file=sys.stderr)
        print ("max_depth:", max_depth, file=sys.stderr)
        print ("random_state:", 0, file=sys.stderr)
        print ("class_weight:", class_weight, file=sys.stderr)
        
        discr = RandomForestClassifier(n_estimators = n_estimators, max_depth = max_depth, random_state=random_seed, class_weight = class_weight)
        discr.fit(X_array, y_array)

        feature_importance = discr.feature_importances_

        return feature_importance, None, discr

def calc_auc(one_rank_list, N_total): # to accelerate calculation of null distribution of AUC

    N_one  = len(one_rank_list)
    N_zero = N_total - N_one
    height = 0
    auc    = 0
    for i in range(len(one_rank_list[:-1])):
        height += 1 / N_one
        width  =  (one_rank_list[i+1] - one_rank_list[i] - 1) / N_zero
        auc    += height * width
    height += 1 / N_one
    width  =  (N_total - one_rank_list[-1] - 1) / N_zero 
    auc    += height * width
    return auc

def crossvalidation(
    X_array, 
    y_array, 
    model  ,
    k      ,
    sampling,
    random_seed,
    # logistic regression args
    lr_penalty,
    lr_solver,
    # random forest args
    n_estimators = 100,
    max_depth = 2,
    # others
    scoring = "roc_auc",
    n_permutation = 100000,
    class_weight = "balanced"
    ):

    if class_weight == "none": class_weight = None

    if (model == "LR"):
        
        discr = LogisticRegression(penalty = lr_penalty, solver = lr_solver)
        
    
    elif (model == "RF"):

        print ("RandomForestClassifier papameters:", file=sys.stderr)
        print ("n_estimators:", n_estimators, file=sys.stderr)
        print ("max_depth:", max_depth, file=sys.stderr)
        print ("random_state:", 0, file=sys.stderr)
        print ("class_weight:", class_weight, file=sys.stderr)
        
        discr = RandomForestClassifier(n_estimators = n_estimators, max_depth = max_depth, random_state=random_seed, class_weight = class_weight)
        
    stratifiedkfold = StratifiedKFold(n_splits=k, shuffle = True, random_state=random_seed) # This is quite important because the order of X and y is not arbitrary

    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=random_seed)
    value_list = []
    
    i = 0
    for train_index, test_index in skf.split(X_array, y_array):
        i += 1

        X_train, X_test = X_array[train_index], X_array[test_index]
        y_train, y_test = y_array[train_index], y_array[test_index]
        if (sampling == 'under'):
            Nsample = min(X_train.sum(), y_train.sum())
            sampler = RandomUnderSampler(sampling_strategy={0: Nsample, 1: Nsample}, random_state=random_seed) # adjust to # of positive samples
            X_train_sampled, y_train_sampled = sampler.fit_sample(X_train, y_train)
            alpha = Nsample / len(X_train)
            beta  = Nsample / len(y_train)
            def calibration(y_prob, alpha, beta):
                return y_prob / (alpha * y_prob + (1 - y_prob) * alpha / beta)
            _ = discr.fit(X_train_sampled, y_train_sampled)  # no echo back
            y_prob = discr.predict_proba(X_test)
            y_prob_calib = calibration(y_prob[:, 1], alpha, beta)
            y_prob = y_prob_calib
        elif (sampling == 'over'):
            Nsample = max(len(y_train) - y_train.sum(), y_train.sum())
            sampler = RandomOverSampler(ratio={0: Nsample, 1: Nsample}, random_state=random_seed)
            X_train_sampled, y_train_sampled = sampler.fit_sample(X_train, y_train)
            _ = discr.fit(X_train_sampled, y_train_sampled)  # no echo back
            y_prob = discr.predict_proba(X_test)
            y_prob = y_prob[:, 1] # Notice!: This is still uncalibrated
        elif (sampling == 'none'):
            _ = discr.fit(X_train, y_train)  # no echo back
            y_prob = discr.predict_proba(X_test)
            y_prob = y_prob[:, 1] # Notice!: This is still uncalibrated
        
        # calculate AUC
        
        if scoring == "roc_auc":
            AUC=roc_auc_score(y_test,y_prob)
            value_list.append(AUC)

        elif scoring == "roc_auc_pvalue":

            N_total= len(y_prob)
            y_prob_rank = np.argsort(np.argsort(y_prob))
            one_rank_list = []
            for i in range(len(y_prob)):
                if (y_test[i] == 1):
                    one_rank_list.append(N_total - 1 - y_prob_rank[i])
            N_one = len(one_rank_list)
            
            AUC=calc_auc(one_rank_list, N_total)
            #AUC_test=roc_auc_score(y_test,y_prob)
            #print(AUC, AUC_test)

            random.seed(random_seed)
            count = 0
            y_prob = list(y_prob)
            for _ in range(n_permutation):
                random_one_rank_list = random.sample(list(range(N_total)), N_one)
                random_one_rank_list.sort()
                random_AUC           = calc_auc(random_one_rank_list, N_total)
                if (random_AUC >= AUC):
                    count += 1
            pvalue = count / n_permutation
            value_list.append(pvalue)
        
        elif scoring == "roc_curve":
            fpr, tpr, thresholds = roc_curve(y_test,y_prob)
            for f, t in zip(fpr, tpr):
                value_list.append([i, f, t])

    return list(value_list)