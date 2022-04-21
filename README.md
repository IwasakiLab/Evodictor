<h2>Evodictor and User Manual</h2>


### Overview of Evodictor

**Evodictor** is a software package for predicting evolution of given traits from a species-trait table and a phylogenetic tree

### Supported Environment

1. **Evodictor** can be executed on Linux OS / Mac

### Software Dependency

<h4>Required</h4>

1. Python3 (version: 3.7.0 or later) with biopython, scipy, numpy, imblearn, and scikit-learn modules *required*

### Software installation

Each installation step will take less than ~1 min


#### Installation of Evodictor # Currently Unavailable


1. Download Evolution Prediction Toolkit by

   ```shell
    git clone 
   ```

2. Add the absolute path of `xxx/src` directory to `$PATH`

3. Make `/src/*` executable

   ```shell
   chmod u+x xxx/src/*
   ```

### Sample Codes

The Evolution Prediction Toolkit package contains an example input file in the `examples` directory so that users can easily try the basic function as follows:

**Example 1**

Calculate importane of each feature based on ANOVA

```shell
selevo -i Xy.txt --skip_header --o1 $(pwd)/result.o1.txt --o2 $(pwd)/result.o2.txt --o3 $(pwd)/result.o3.txt -k 5
```


Input:

[`Xy.txt`](https://github.com/IwasakiLab/PredictMetabolicNetworkEvolution/blob/master/python/Pipeline/EvolutionPredictor/example/Xy.txt)

Output:

 [`result.o1.txt`](https://github.com/IwasakiLab/PredictMetabolicNetworkEvolution/blob/master/python/Pipeline/EvolutionPredictor/example/output/result.o1.txt) : Importance of each feature

[`result.o2.5.txt`](https://github.com/IwasakiLab/PredictMetabolicNetworkEvolution/blob/master/python/Pipeline/EvolutionPredictor/example/output/result.o2.5.txt) : Binary values indicating whether each feature was selected or not (1: selected, 0: not selected)

[`result.o3.5.txt`](https://github.com/IwasakiLab/PredictMetabolicNetworkEvolution/blob/master/python/Pipeline/EvolutionPredictor/example/output/result.o3.5.txt) : Input dataset for predevo which includes only selected features  

### Usage

**xygen**

```
usage: xygen [-h] [-v] [-p] [--target TARGET] [-s SPARSEMATRIX] [-t TREE]
             [-m MODE] [--predictor PREDICTOR] [--gl GL]


optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print EvolutionPredictor version
  -p, --print           Print all arguments
  --target TARGET       Target element (eg. 'R00001')
  -s SPARSEMATRIX, --sparsematrix SPARSEMATRIX
                        Sparse matrix file path
  -t TREE, --tree TREE  Tree file path
  -m MODE, --mode MODE  Mode of dataset generator (default: 'define')
  --predictor PREDICTOR
                        Predictor definition file path
  --gl GL               Specify 'gain' or 'loss'
```

**selevo**

```
usage: selevo [-h] [-v] [-p] [-i INPUT] [--scores SCORES] [--mask MASK]
              [--newXygen NEWXYGEN] [-n NORMALIZE] [-m METHOD] [-k K]
              [--skip_header] [--n_estimators N_ESTIMATORS]
              [--max_depth MAX_DEPTH]


optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print SyntrophyDetector version
  -p, --print           Print all arguments
  -i INPUT, --input INPUT
                        Input file path
  --scores SCORES, --o1 SCORES
                        Output model parameter file path ('stdout' is also
                        acceptable, 'None' inactivates output)
  --mask MASK, --o2 MASK
                        Output selected parameters ('0': not selected, '1':
                        selected)
  --newXygen NEWXYGEN, --o3 NEWXYGEN
                        Output renewed dataset file path
  -n NORMALIZE, --normalize NORMALIZE
                        Conduct normalization (Permissive values: 'standard'
                        (default), 'minmax', 'skip')
  -m METHOD, --method METHOD
                        Feature selection method (Permissive values: 'ANOVA',
                        'RandomForest')
  -k K                  Number of selected features (default: '1,2,3,4,5')
  --skip_header         Skip header row
  --n_estimators N_ESTIMATORS
                        This option is active only when '-m RandomForest'.
                        Number of trees for random forest feature selection.
  --max_depth MAX_DEPTH
                        This option is active only when '-m RandomForest'.
                        Maximum tree depth for random forest feature
                        selection.
```

**predevo**

```
usage: predevo [-h] [-v] [-p] [-i INPUT] [-n NORMALIZE] [-m MODEL] [-c]
               [-k KFOLD] [--onecv] [--pointbiserialr] [--header]
               [--n_estimators N_ESTIMATORS] [--max_depth MAX_DEPTH]


optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print SyntrophyDetector version
  -p, --print           Print all arguments
  -i INPUT, --input INPUT
                        Input file path
  -n NORMALIZE, --normalize NORMALIZE
                        Conduct normalization (Permissive values: 'standard'
                        (default), 'minmax', 'skip')
  -m MODEL, --model MODEL
                        Prediction model (Permissive values: 'LR', 'RF')
  -c, --cv              Conduct stratified cross validation
  -k KFOLD, --kfold KFOLD
                        K for k-fold stratified cross validation
  --onecv               Conduct cross validation for each feature one by one.
                        This option is only valid when -c option is specified
  --pointbiserialr      Calculates a point biserial correlation coefficient
                        between each feature and y, and the associated p-value
                        (if True, other options will be ignored)
  --header              Skip header row
  --n_estimators N_ESTIMATORS
                        This option is active only when '-m RandomForest'.
                        Number of trees for random forest feature selection.
  --max_depth MAX_DEPTH
                        This option is active only when '-m RandomForest'.
                        Maximum tree depth for random forest feature
                        selection.
```

### Contact


Naoki Konno (The University of Tokyo) [konno-naoki555@g.ecc.u-tokyo.ac.jp](mailto:konno-naoki555@g.ecc.u-tokyo.ac.jp)
