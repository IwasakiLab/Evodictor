<h2>Evodictor and User Manual</h2>


### Overview of Evodictor

**Evodictor** is a software package for predicting gain/loss evolution of given traits from a species-trait table and a phylogenetic tree

### Supported Environment

1. **Evodictor** can be executed on Linux OS / Mac

### Software Dependency

<h4>Required</h4>

1. Python3 (version: 3.7.0 or later) with biopython, scipy, numpy, imblearn, and scikit-learn modules *required*

### Software installation

Each installation step will take less than ~1 min


#### Installation of Evodictor


1. Download Evodictor and move to the directory by

    ```shell
    git clone https://github.com/IwasakiLab/Evodictor.git
    cd Evodictor/
    ```

2. Install dependencies by

    ```shell
    conda install -c conda-forge biopython imbalanced-learn
    conda install -c anaconda scipy scikit-learn
    conda install -c conda-forge conda-forge::numpy
    ```

    or 

    ```shell
    conda create -n evodictor --file evodictor_env.txt
    conda activate evodictor
    ```

3. Add the absolute path of `Evodictor/src` directory to `$PATH`

    ```shell
    export PATH=$(pwd)/src:${PATH}
    ```

4. Make `Evodictor/src/*` executable

   ```shell
   chmod u+x src/*
   ```

### Sample Codes

The evodictor contains an example input file in the `examples` directory so that users can easily try the basic function as follows:

**Example 1**

Generate dataset for machine learning from a ancestral state reconstruction result and a phylogenetic tree to predict gene gain of an ortholog group ("K00005")

```shell
evodictor generate --target K00005 -X OG_node_state.txt -y OG_node_state.txt -t example.tree --predictor feature_OG.txt --gl gain > branch_X_y.txt
```

Or you can type "xygen" instead of "evodictor generate".

Input:

[`OG_node_state.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/OG_node_state.txt): The state of possession of an ortholog group (OG) for tips and internal nodes of `example.tree`. States not written in this file will be treated as 0.

[`example.tree`](https://github.com/IwasakiLab/Evodictor/tree/main/example/example.tree): A phylogenetic tree in a newick format.

[`feature_OG.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/feature_OG.txt): Correspondence of each feature (M00001, M00002, ...) and ortholog groups (K00001, K00002, ...). One feature corresponds to multiple ortholog groups.

Output:

[`branch_X_y.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/branch_X_y.txt): List of input (X) and output (y) for every branch in `example.tree`. Branches are represented by the names of their child node. X is the feature vector representing the gene content of parental species of a branch, and y is the occurrence of gene gain/loss of an ortholog group (K00005). 

**Example 2**

Select top-20 input features based on ANOVA F-value to predict gene gain of an ortholog group ("K00005")

```shell
evodictor select -i branch_X_y.txt --skip_header --o1 feature_importance.txt --o2 selection_result.txt --o3 branch_X_y.selected.txt -k 20
```

Or you can type "selevo" instead of "evodictor select".

Input:

[`branch_X_y.selected.20.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/branch_X_y.selected.20.txt)

Output:

[`feature_importance.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/feature_importance.txt) : Importance of every feature

[`selection_result.20.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/selection_result.20.txt) : Binary values indicating whether each feature was selected or not (1: selected, 0: not selected)

[`branch_X_y.selected.20.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/branch_X_y.selected.20.txt) : Input dataset for "evodictor predict" which includes only selected features  

**Example 3**

Conduct phylogeny-aware downsampling from `branch_X_y.selected.20.txt`. Evodictor randomly extracts rows of `branch_X_y.selected.20.txt` so that the ratio of positive and negative instances is 10%:90% for every phylum.

```shell
evodictor sample -t example.tree -d branch_X_y.selected.20.txt -x ar122_taxonomy.tsv -r phylum > branch_X_y.selected.20.sampled.txt
```

Input:

[`branch_X_y.selected.20.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/branch_X_y.selected.20.txt)

[`example.tree`](https://github.com/IwasakiLab/Evodictor/tree/main/example/example.tree): A phylogenetic tree in a newick format.

[`ar122_taxonomy.tsv`](https://github.com/IwasakiLab/Evodictor/tree/hotfix/example/ar122_taxonomy.tsv): Taxonomic information of every tip of `example.tree`

Output:

[`branch_X_y.selected.20.sampled.txt`](https://github.com/IwasakiLab/Evodictor/tree/hotfix/example/output/branch_X_y.selected.20.sampled.txt)

**Example 4**

Conduct three-fold cross validation of gene gain prediction by logistic regression for an ortholog group ("K00005")

```shell
evodictor predict -i branch_X_y.selected.20.txt -c -k 3 -m LR --header > cross_validated_AUCs.txt
```

[`cross_validated_AUCs.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/cross_validated_AUCs.txt) : List of three AUCs measured by three-fold cross validation

### Usage

**evodictor generate / xygen**

```
usage: evodictor generate [-h] [-v] [-p] [--target TARGET] [-X SPARSE_X] [-y SPARSE_Y]
             [-t TREE] [--predictor PREDICTOR] [--gl GL] [-m MODE] [--ex]

evodictor generate

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print evodictor version (default: False)
  -p, --print           Print all arguments (default: False)
  --target TARGET       [Required] Prediction target (eg. 'R00001')
  -X SPARSE_X, --sparse_X SPARSE_X
                        [Required] Sparse matrix file path for input features
                        X
  -y SPARSE_Y, --sparse_y SPARSE_Y
                        [Required] Sparse matrix file path for output y
  -t TREE, --tree TREE  [Required] Tree file path
  --predictor PREDICTOR
                        [Required] Predictor definition file path
  --gl GL               [Required] Specify 'gain' or 'loss'
  -m MODE, --mode MODE  Mode of dataset generator (default: 'define')
  --ex                  Print only X for extant species (default: False)
```

**evodictor select / selevo**

```
usage: evodictor select [-h] [-v] [-p] [-i INPUT] [-m METHOD] [--scores SCORES]
              [--mask MASK] [--newXygen NEWXYGEN] [-n NORMALIZE] [-k K]
              [--skip_header] [--n_estimators N_ESTIMATORS]
              [--max_depth MAX_DEPTH] [--signed]

evodictor select

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print evodictor version
  -p, --print           Print all arguments
  -i INPUT, --input INPUT
                        [required] Input file path
  -m METHOD, --method METHOD
                        [required] Feature selection method (Permissive
                        values: 'ANOVA', 'RandomForest')
  --scores SCORES, --o1 SCORES
                        Output feature importance file path ('stdout' is also
                        acceptable, 'None' inactivates output) (default:
                        stdout)
  --mask MASK, --o2 MASK
                        Output selected parameters ('0': not selected, '1':
                        selected) (default: stdout)
  --newXygen NEWXYGEN, --o3 NEWXYGEN
                        Output a dataset file with selected features (default:
                        stdout)
  -n NORMALIZE, --normalize NORMALIZE
                        Conduct normalization (Permissive values: 'standard',
                        'minmax', 'skip') (default: 'standard')
  -k K                  Number of selected features (default: 5)
  --skip_header         Skip header row (default: False)
  --n_estimators N_ESTIMATORS
                        This option is active only when '-m RandomForest'.
                        Number of trees for random forest feature selection.
                        (default: 100)
  --max_depth MAX_DEPTH
                        This option is active only when '-m RandomForest'.
                        Maximum tree depth for random forest feature
                        selection. (default: 2)
  --signed              Calculate signed importance value (positive or
                        negative) (default: False)
```

**evodictor sample / evosample**

```
usage: evodictor sample [-h] [-t TREE] [-d DATASET] [-x TAXONOMY] [-p POS_RATIO]
                 [-r RESOLUTION] [-s SEED]

Phylogeny-aware downsampling

optional arguments:
  -h, --help            show this help message and exit
  -t TREE, --tree TREE  [Required] Tree file path
  -d DATASET, --dataset DATASET
                        [Required] Dataset file path: Output of 'evodictor
                        generate'
  -x TAXONOMY, --taxonomy TAXONOMY
                        [Required] Taxonomy file path (tab-separated: '<tip
                        name> <taxonomy info>')
  -p POS_RATIO, --pos_ratio POS_RATIO
                        Positive instance ratio (Default: 0.10)
  -r RESOLUTION, --resolution RESOLUTION
                        Taxonomic resolution (Default: phylum_or_class;
                        Permissive values: 'phylum', 'class',
                        'phylum_or_class', 'order', 'family', 'genus';
                        'phyum_or_class': Only p__Proteobacteria is broken
                        down into classes)
  -s SEED, --seed SEED  Seed of the random number generator
```

**evodictor predict / predevo**

```
usage: evodictor predict [-h] [-v] [-p] [-i INPUT] [-m MODEL] [-t TEST] [-n NORMALIZE]
               [--pointbiserialr] [-c] [--hv] [-k KFOLD] [-s SAMPLING]
               [--scoring SCORING] [--permutation PERMUTATION] [-r SEED]
               [--header] [--n_estimators N_ESTIMATORS]
               [--max_depth MAX_DEPTH] [--lr_penalty LR_PENALTY]
               [--lr_solver LR_SOLVER]

evodictor predict

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print evodictor version
  -p, --print           Print all arguments
  -i INPUT, --input INPUT
                        [Required] Input file path
  -m MODEL, --model MODEL
                        [Required] Prediction model (Permissive values: 'LR',
                        'RF')
  -t TEST, --test TEST  Test data file path; if this option was specified, the
                        file specified by -i is treated as a training dataset,
                        then conduct prediction for the test data file
                        specified by this option
  -n NORMALIZE, --normalize NORMALIZE
                        Conduct normalization (Permissive values: 'standard',
                        'minmax', 'skip') (default: 'standard')
  --pointbiserialr      Calculates a point biserial correlation coefficient
                        between each feature and y, and the associated p-value
                        (if True, other options will be ignored) (default:
                        False)
  -c, --cv              Conduct stratified cross validation
  --hv                  Conduct stratified hold-out validation (default:
                        False)
  -k KFOLD, --kfold KFOLD
                        K for k-fold stratified cross validation. This option
                        is valid only when -c is specified. (default: 0)
  -s SAMPLING, --sampling SAMPLING
                        Resampling the training dataset in cross validation.
                        Permissive values: 'none', 'under', 'over' (default:
                        'none')
  --scoring SCORING     Scoring of cross validation. Permissive values:
                        'roc_auc', 'roc_auc_pvalue', or 'roc_curve'. This
                        option is valid only when -c is specified. (default:
                        'roc_auc')
  --permutation PERMUTATION
                        Number of permutations for calculating p-value of AUC
                        in cross validation. This option is used only when '--
                        scoring roc_auc_pvalue' is specified. (default:
                        100000)
  -r SEED, --seed SEED  Random seed (default: 0)
  --header              Skip header row (default: False)
  --n_estimators N_ESTIMATORS
                        Number of trees for random forest feature selection.
                        This option is active only when '-m RF'. (default:
                        100)
  --max_depth MAX_DEPTH
                        Maximum tree depth for random forest feature
                        selection. This option is active only when '-m RF'.
                        (default: 2)
  --lr_penalty LR_PENALTY
                        Regularization for logistic regression. This option is
                        active only when '-m LR'. Permissive values: ‘l1’,
                        ‘l2’, ‘elasticnet’, ‘none’ (default: 'l2')
  --lr_solver LR_SOLVER
                        Solver for logistic regression. Permissive values:
                        ‘newton-cg’, ‘lbfgs’, ‘liblinear’, ‘sag’, ‘saga’
                        (default: 'liblinear')
```

### Contact


Naoki Konno (The University of Tokyo) [konno-naoki555@g.ecc.u-tokyo.ac.jp](mailto:konno-naoki555@g.ecc.u-tokyo.ac.jp)
