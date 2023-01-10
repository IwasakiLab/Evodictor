<h2>Evodictor and User Manual</h2>


### Overview of Evodictor

**Evodictor** is a software package for learning patterns and predicting the future of evolution by gain/losses of given binary traits (e.g., gene presence/absence). Evodictor takes a phylogenetic tree and presence/absence profiles of every trait for all the extant and the ancestral species in the tree as input, then predicts the gain/loss probability of a target trait from a given trait repertoire of a species (e.g., presence/absence of every gene in the genome of the species). To predict trait gain/loss, Evodictor learns what traits tend to be present/absent prior to gain/losses of the target trait from past gain/loss evolution across diverse species. Evodictor was established in a study (XXXXXX), and was demonstrated to predict gene gain/loss evolution of bacterial metabolic systems.

<img src=image/Fig1.png >

**Figure 1. Overview of Evodictor for gene gain/loss prediction.** 

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

This repository contains an example input file in the `examples` directory so users can quickly try predicting gene gain/loss evolution using Evodictor step-by-step:

**Step 1: Dataset Generation**

Generate a dataset for machine learning from a phylogenetic tree and presence/absence profiles of every trait for all the extant and the ancestral species in the tree to predict gene gain of a target ortholog group ([K00005](https://www.genome.jp/dbget-bin/www_bget?ko:K00005) in this example)

```shell
evodictor generate --target K00005 -X OG_node_state.txt -y OG_node_state.txt -t example.tree --predictor feature_OG.txt --gl gain > branch_X_y.txt
```

Or you can type "xygen" instead of "evodictor generate".

Input:

[`example.tree`](https://github.com/IwasakiLab/Evodictor/tree/main/example/example.tree): A phylogenetic tree in a Newick format.

[`OG_node_state.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/OG_node_state.txt): The presence/absence profile of every ortholog group (OG) for every tip node (extant species) and every internal node (ancestors) of [`example.tree`](https://github.com/IwasakiLab/Evodictor/tree/main/example/example.tree). There is one row for every internal/tip node in this file. The first, second, and third columns of every row indicate the OG name, node name, and the presence/absence state, respectively. The presence/absence state is represented as `0` (absent), `1` (present), or `0.5` (uncertain; for ancestors). Rows for which states are `0` can be omitted in this file (in other words, states of nodes not defined in this file are treated as `0`).

[`feature_OG.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/feature_OG.txt): Correspondence between OGs (e.g., [K00001](https://www.genome.jp/dbget-bin/www_bget?ko:K00001)) and features (defined as groups of OGs; e.g., [M00001](https://www.genome.jp/dbget-bin/www_bget?md:M00001)). The input of the machine learning model in Evodictor is the vector in which every dimension (feature) corresponds to the number of present OGs included in the feature.

Output:

[`branch_X_y.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/branch_X_y.txt): The dataset for machine learning which can be an input file of `evodictor predict`. The first row is the header, and each of the following rows correspond to a branch in the [`example.tree`](https://github.com/IwasakiLab/Evodictor/tree/main/example/example.tree). The first, second, and third column of every row indicate the node name of a parental species of a branch in [`example.tree`](https://github.com/IwasakiLab/Evodictor/tree/main/example/example.tree), the number of present traits of every feature in the parental species (separated by `;`), and the occurrence of gene gain of predicted OG ([K00005](https://www.genome.jp/dbget-bin/www_bget?ko:K00005)) at the branch (`1`: the gene was gained at the branch;  `0`: the gene was not gained at the branch). 

**Step 2: Feature Selection**

Select top-20 important input features based on ANOVA F-value to predict gene gain of an OG ([K00005](https://www.genome.jp/dbget-bin/www_bget?ko:K00005)).

```shell
evodictor select -i branch_X_y.txt --skip_header --o1 feature_importance.txt --o2 selection_result.txt --o3 branch_X_y.selected.txt -k 20
```

Or you can type "selevo" instead of "evodictor select".

Input:

[`branch_X_y.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/branch_X_y.txt): The file generated in **Step 1**

Output:

[`feature_importance.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/feature_importance.txt) : Importance (ANOVA F-value) of every feature

[`selection_result.20.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/selection_result.20.txt) : Binary values indicating whether each feature was included in top-20 important features or not (`1`: selected, `0`: not selected)

[`branch_X_y.selected.20.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/branch_X_y.selected.20.txt) : The dataset for machine learning which can be an input file of `evodictor predict` and contain only selected top-20 important features. 

**Step 3: Cross-validation**

Conduct three-fold cross validation of gene gain prediction by logistic regression for an OG ([K00005](https://www.genome.jp/dbget-bin/www_bget?ko:K00005))

```shell
evodictor predict -i branch_X_y.selected.20.txt -c -k 3 -m LR --header > cross_validated_AUCs.txt
```

Input:

[`branch_X_y.selected.20.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/branch_X_y.selected.20.txt) : The file generated in **Step 3**

Output:

[`cross_validated_AUCs.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/cross_validated_AUCs.txt) : List of the three AUCs (AUROCs) measured by three-fold cross validation

**Step 4: Future gene gain prediction**

Conduct training of logistic regression model and prediction of future gene gain probability of an OG ([K00005](https://www.genome.jp/dbget-bin/www_bget?ko:K00005)) for every species. All the features were used for model training and prediction in this example. You can also conduct prediction with only selected features by changing two of the input files: `feature_OG.txt` and `branch_X_y.txt`.

```shell
evodictor generate --target K00005 -X OG_node_state.txt -y OG_node_state.txt -t example.tree --predictor feature_OG.txt --gl gain --ex > extant_X.txt
evodictor predict -m LR --header -i branch_X_y.txt -t extant_X.txt > species_probability.txt
```

Input:

[`example.tree`](https://github.com/IwasakiLab/Evodictor/tree/main/example/example.tree): The same input file as **Step 1**

[`OG_node_state.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/OG_node_state.txt): The same input file as **Step 1**

[`feature_OG.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/feature_OG.txt): The same input file as **Step 1**

[`branch_X_y.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/branch_X_y.txt): The file generated in **Step 1**

Output: 

[`extant_X.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/extant_X.txt) : List of input feature vectors of extant species (i.e., tip nodes of [`example.tree`](https://github.com/IwasakiLab/Evodictor/tree/main/example/example.tree)). The first row is a header. The first and second columns in each of the following rows indicate a extant species name and the number of present traits for every feature in the extant species (separated by `;`).

[`species_probability.txt`](https://github.com/IwasakiLab/Evodictor/tree/main/example/output/species_probability.txt) : Predicted gene gain probability of ([K00005](https://www.genome.jp/dbget-bin/www_bget?ko:K00005) for every extant species. The first and second columns in each row indicate a extant species name and the predicted gene gain probability.

**Micellaneous**

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
