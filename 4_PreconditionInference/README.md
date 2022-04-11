# Overview

In this assignment, you will be given a set of sentence pairs. For each pair of sentence, the first one is considered as a precondition, while the second one is a statement. The goal is to develop a natural language reasoner to decide whether the precondition will enable or disable the statement.

For example: given the statement "A glass can be used to drink water", then the precondition "water is clean" enables this statement, while the precondition "the glass is completely broken" disables this statement.

You are free to experiment with any methods of representation, encoding , including any pre-trained models. Submit your prediction on the unlabeled test set. We will compare your prediction with the ground-truth labels of the test set on our side. Grading will be based on the ranking of your submitted prediction among all of those in the class.

# Data and Jupyter Notebook

A compressed ZIP file is to be released on Blackboard when the assignment is available. The uncompressed archive contain the following files:

- `main.ipynb`: The Python 3 Jupyter notebook you will need to fill in with your training and inference code, and predict the results.

- data folder:
  - `pnli_train.tsv`: labeled training data in csv format. Each line is tuple in the form of `(precondition, statement, label)`. `label=1` means `"enable"` and `label=0` means `"disable"`. 
  - `pnli_dev.tsv`: labeled dev data. 
  - `pnli_test_unlabeled.tsv`: unlabled test data. Each line is a pair of precondition and statement.

- `upload_document.txt`: the documentation file where you need to fill in the blanks to describe your method.

# Programs and Models

We again provide a jupyter notebook which provides the starting code for reading the data, and the end part to generate `"upload_predictions.txt"`. You need to fill in the "Main Code Body", and put the 4850 predictioned labels into the results list.

**Restrictions**:

Your method needs to be implemented using `python 3`. You are free to use any python package (e.g., pytorch, Huggingface, AllenNLP, etc.).

You are free to include any pre-trained models (any versions of Transformer language models, pre-trained NLI models, pre-trained QA models, etc.). However, only free models are allowed (hence, you cannot prompt GPT-3).

You can consider doing your experiment on Google Colab (which provides a free student membership), your own machine, or any computating resources that are available to you.

# Submission

This assignment requests submitting three files (DO NOT CHANGE the filenames):

1. `upload_predictions.txt`: The predictions of your model on the 4850 unlabeled test set of sentence pairs. This file should have exactly 4850 lines, every line is either 0 or 1. (submit this on Vocareum)
2. `upload_document.txt`: Fill in the blanks of that file to accordingly describe how your model is developed. (submit this on Blackboard)
3. `main.ipynb`: This Jupyter notebook already contains the beginning part to read the data, and the end part to generate "upload_predictions.txt". You need to fill in the "Main Code Body"  (submit this on Blackboard).

Multiple submissions are allowed; only the final submission will be graded. Do not include any other files in your submission.  You are encouraged to submit early and often in order to iron out any problems, especially issues with the format of the final output.

We will again use a leaderboard protocol: the ground-truth labels on the test set are not released to you, and we will compare your prediction with them to calculate the accuracy of your prediction.

# Q&A

> **How many labels are there?** This is a binary classification task. Only two labels are used: 0 and 1, meaning "disabling" and "enabling".

> **Are the test data from the same distribution of the training/dev data?** Yes, they were splits from the same dataset.

> **Is the dataset balanced?** Almost balanced.

> **How do I know if my method is well-performing or not?** You can try to tell it by the dev set performance. However, we have to put this note at here due to what we have observed in HW3: dev set performance evaluation means the model is trained using the training set and evaluated on the dev set, but NOT training using training + dev sets then test on the dev set.

> **What's the evaluation metric?** Accuracy.

> **Can you suggest some methods to try out?** The most well-aligned formulation of this task is NLI. You can definitely train an NLI model from scratch using the training data. Besides, those are some directions you can consider: 
> - Fine-tuning a pre-trained NLI model. 
> - Fine-tuning a QA model (and treat this task as a binary QA task).
> - Fine-tuning a pre-trained LM as Next Sentence Prediction (NSP).
> - Generative data augmentation.
> - Incorporating external knowledge (e.g., from a knowledge base like conceptnet).
> - etc.

> **Is there a single best solution?** Again, this assignment is an open-ended problem. So there is hardly a single best solution (don't ever try to ask TAs about it: they do not know it either). 