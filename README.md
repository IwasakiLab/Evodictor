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

The evodictor contains an example input file in the `examples` directory so that users can easily try the basic function as follows:

**Example 1**

Generate dataset for machine learning from a ancestral state reconstruction result and a phylogenetic tree

```shell
evodictor generate --target K00005 -X OG_node_state.txt -y OG_node_state.txt -t example.tree --predictor feature_OG.txt --gl gain > branch_X_y.txt
```

Or you can type "xygen" instead of "evodictor generate".

Input:

[`OG_node_state.txt`](): The state of possession of an ortholog group (OG) for tips and internal nodes of `example.tree`. States not written in this file will be treated as 0.

[`example.tree`](): A phylogenetic tree in a newick format.

[`feature_OG.txt`](): Correspondence of each feature (M00001, M00002, ...) and ortholog groups (K00001, K00002, ...). One feature corresponds to multiple ortholog groups.

Output:

[`branch_X_y.txt`](): List of input (X) and output (y) for every branch in `example.tree` represented by the name of its child node. X is the feature vector representing the gene content of parental species of a branch, and y is the occurrence of gene gain/loss of an ortholog group (K00005). 

**Example 2**

Select input features based on ANOVA F-value

```shell
selevo -i Xy.txt --skip_header --o1 $(pwd)/result.o1.txt --o2 $(pwd)/result.o2.txt --o3 $(pwd)/result.o3.txt -k 5
```

Input:

[`Xy.txt`](https://github.com/IwasakiLab/PredictMetabolicNetworkEvolution/blob/master/python/Pipeline/EvolutionPredictor/example/Xy.txt)

Output:

[`result.o1.txt`](https://github.com/IwasakiLab/PredictMetabolicNetworkEvolution/blob/master/python/Pipeline/EvolutionPredictor/example/output/result.o1.txt) : Importance of each feature

[`result.o2.5.txt`](https://github.com/IwasakiLab/PredictMetabolicNetworkEvolution/blob/master/python/Pipeline/EvolutionPredictor/example/output/result.o2.5.txt) : Binary values indicating whether each feature was selected or not (1: selected, 0: not selected)

[`result.o3.5.txt`](https://github.com/IwasakiLab/PredictMetabolicNetworkEvolution/blob/master/python/Pipeline/EvolutionPredictor/example/output/result.o3.5.txt) : Input dataset for predevo which includes only selected features  

**Example 3**

Conduct five-fold cross validation of gene gain prediction for an ortholog group (K00005)

```shell
```

**Example 4**

Predict gene gain probability of every extant species for an ortholog group (K00005)

```shell
```

### Usage

**evodictor generate / xygen**

```
usage: evodictor generate [-h] [-v] [-p] [--target TARGET] [-X SPARSE_X] [-y SPARSE_Y]
             [-t TREE] [-m MODE] [--predictor PREDICTOR] [--gl GL] [--ex]

evodictor generate

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print EvolutionPredictor version
  -p, --print           Print all arguments
  --target TARGET       Prediction target (eg. 'R00001')
  -X SPARSE_X, --sparse_X SPARSE_X
                        [Required] Sparse matrix file path for input features
                        X
  -y SPARSE_Y, --sparse_y SPARSE_Y
                        [Required] Sparse matrix file path for output y
  -t TREE, --tree TREE  Tree file path
  -m MODE, --mode MODE  Mode of dataset generator (default: 'define')
  --predictor PREDICTOR
                        Predictor definition file path
  --gl GL               Specify 'gain' or 'loss'
  --ex                  Print only X for extant species
```

**evodictor select / selevo**

```
usage: evodictor select [-h] [-v] [-p] [-i INPUT] [--scores SCORES] [--mask MASK]
              [--newXygen NEWXYGEN] [-n NORMALIZE] [-m METHOD] [-k K]
              [--skip_header] [--n_estimators N_ESTIMATORS]
              [--max_depth MAX_DEPTH] [--signed]

evodictor select

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
  -k K                  Number of selected features (default: '5')
  --skip_header         Skip header row
  --n_estimators N_ESTIMATORS
                        This option is active only when '-m RandomForest'.
                        Number of trees for random forest feature selection.
  --max_depth MAX_DEPTH
                        This option is active only when '-m RandomForest'.
                        Maximum tree depth for random forest feature
                        selection.
  --signed              Calculate signed importance value (positive or
                        negative)
```

**evodictor predict / predevo**

```
usage: evodictor predict [-h] [-v] [-p] [-i INPUT] [-t TEST] [-n NORMALIZE] [-m MODEL]
               [--pointbiserialr] [-c] [--hv] [-k KFOLD] [-s SAMPLING]
               [--scoring SCORING] [--permutation PERMUTATION] [-r SEED]
               [--header] [--n_estimators N_ESTIMATORS]
               [--max_depth MAX_DEPTH] [--lr_penalty LR_PENALTY]
               [--lr_solver LR_SOLVER]

evodictor predict

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print SyntrophyDetector version
  -p, --print           Print all arguments
  -i INPUT, --input INPUT
                        [Required] Input file path
  -t TEST, --test TEST  Test data file path; if this option was specified, the
                        file specified by -i is treated as a training dataset,
                        then conduct prediction for the test data file
                        specified by this option
  -n NORMALIZE, --normalize NORMALIZE
                        Conduct normalization (Permissive values: 'standard'
                        (default), 'minmax', 'skip')
  -m MODEL, --model MODEL
                        [Required] Prediction model (Permissive values: 'LR',
                        'RF')
  --pointbiserialr      Calculates a point biserial correlation coefficient
                        between each feature and y, and the associated p-value
                        (if True, other options will be ignored)
  -c, --cv              Conduct stratified cross validation
  --hv                  Conduct stratified hold-out validation
  -k KFOLD, --kfold KFOLD
                        K for k-fold stratified cross validation
  -s SAMPLING, --sampling SAMPLING
                        Resampling the training dataset in cross validation.
                        Permissive values: 'none' (default), 'under', 'over'
  --scoring SCORING     Scoring of cross validation. Permissive values:
                        'roc_auc', 'roc_auc_pvalue', or 'roc_curve' (only with
                        --cv)
  --permutation PERMUTATION
                        Number of permutations for calculating p-value of AUC
                        in cross validation. This option is used only when '--
                        scoring roc_auc_pvalue' is specified.
  -r SEED, --seed SEED  Random seed
  --header              Skip header row
  --n_estimators N_ESTIMATORS
                        This option is active only when '-m RandomForest'.
                        Number of trees for random forest feature selection.
  --max_depth MAX_DEPTH
                        This option is active only when '-m RandomForest'.
                        Maximum tree depth for random forest feature
                        selection.
  --lr_penalty LR_PENALTY
                        Regularization for logistic regression. Permissive
                        values: ‘l1’, ‘l2’, ‘elasticnet’, ‘none’
  --lr_solver LR_SOLVER
                        Solver for logistic regression. Permissive values:
                        ‘newton-cg’, ‘lbfgs’, ‘liblinear’, ‘sag’, ‘saga’
```

### Contact


Naoki Konno (The University of Tokyo) [konno-naoki555@g.ecc.u-tokyo.ac.jp](mailto:konno-naoki555@g.ecc.u-tokyo.ac.jp)
