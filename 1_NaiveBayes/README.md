# Overview

In this assignment you will write a naive Bayes classifier to identify hotel reviews as either truthful or deceptive, and either positive or negative. You will be using the word tokens as features for classification. The assignment will be graded based on the performance of your classifiers, that is how well they perform on unseen test data compared to the performance of a reference classifier.

# Programs

You will write two programs in Python 3 (Python 2 has been deprecated): `nblearn.py` will learn a naive Bayes model from the training data, and `nbclassify.py` will use the model to classify new data.

The learning program will be invoked in the following way:

> python nblearn.py /path/to/input

The argument is the directory of the training data; the program will learn a naive Bayes model, and write the model parameters to a file called nbmodel.txt. The format of the model is up to you, but it should follow the following guidelines:

The model file should contain sufficient information for nbclassify.py to successfully label new data.

The model file should be human-readable, so that model parameters can be easily understood by visual inspection of the file.

The classification program will be invoked in the following way:

> python nbclassify.py /path/to/input

The argument is the directory of the test data; the program will read the parameters of a naive Bayes model from the file `nbmodel.txt`, classify each file in the test data, and write the results to a text file called `nboutput.txt` in the following format:

```
label_a label_b path1
label_a label_b path2 
⋮
```

In the above format, `label_a` is either “truthful” or “deceptive”, `label_b` is either “positive” or “negative”, and `pathn` is the path of the text file being classified.

Note that in the training data, it is trivial to infer the labels from the directory names in the path. However, directory names in the development and test data on Vocareum will be masked, so the labels cannot be inferred this way.

# Notes

**Development data.** While developing your programs, you should reserve some of the data as development data in order to test the performance of your programs. The submission script on Vocareum will use folds 2, 3, and 4 as training data, and fold 1 as development data: that is, it will run nblearn.py on a directory containing only folds 2, 3, and 4, and it will run nbclassify.py on a directory with a modified version of fold 1, where directory and file names are masked. In your own development you may use different splits of the data (but to get the same results as the submission script, you'll need to use the same split). The grading script will use all 4 folds for training, and unseen data for testing.

**Problem formulation.** You may treat the problem as two binary classification problems (truthful/deceptive and positive/negative), or as a 4-class single classification problem. Choose whichever works better.

**Smoothing and unknown tokens.** You should implement some method of smoothing for the training data and a way to handle unknown vocabulary in the test data, otherwise your programs won’t work. For example, you can use add-one smoothing on the training data, and simply ignore unknown tokens in the test data. You may use more sophisticated methods which you implement yourselves.

**Tokenization.** You’d need to develop some reasonable method of identifying tokens in the text (since these are the features for the naive Bayes classifier). Some common options are removing certain punctuation, or lowercasing all the letters. You may also find it useful to ignore certain high-frequency or low-frequency tokens. You may use any tokenization method which you implement yourselves. Experiment, and choose whichever works best.

**Location of data.** As mentioned above, the training and test data are read from a central directory on Vocareum. Do not make assumptions about the location of the data. For example, you may find that the submission data are located a certain depth from the root, and be tempted to read directory names (for training) using the depth from the root, for example using something like path[8]; but then the grading data could be located at a different depth, and this will break your program. Calculating the depth of a directory from the bottom will solve this problem, for example path[-3].
