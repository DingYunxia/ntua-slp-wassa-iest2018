**Overview**

This repository contains the source code of the models submitted by NTUA-SLP team in WASSA 2018 
http://implicitemotions.wassa2018.com/

**Documentation**

In order to make our codebase more accessible and easier to extend, we provide an overview of the structure of our project. 

`datasets` : contains the datasets for the pretraining(2 options, one for LM and one for classifier training)

`embeddings`: the word embedding files used should be put here (i.e. word2vec)

`model`: scripts for running wassa classifier (wassa.py) and SemEval2017 Task4 classifier (sentiment.py), language model (lm.py)

`modules`: the source code of the PyTorch deep-learning models and the baseline models.

`submissions`: contains the script to test trained model and create submission file for Wassa

`utils`: contains helper functions