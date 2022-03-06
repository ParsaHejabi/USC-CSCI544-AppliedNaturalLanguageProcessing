# Overview

Privacy-preservation is an important issue in machine learning. In quite a few application scenarios (e.g., healthcare,
banking, legal fields, private message processing), real data may not be shown to the developer of a data-driven machine
learning model (for NLU or other tasks).

In this assignment, you will experiment with a simple scenario for privacy-preserving NLU: developing a text
classification model based on ciphertext. You will be provided with a training set and a development set of (binary)
labeled ciphertext, as well as an unlabeled test set. All the sentences in the dataset are encrypted on the word level
(hence, words in a sentence are still separated by white spaces).

You are free to experiment with any methods of representation, encoding and classifying the ciphertext using the
training and dev data, and submit your prediction on the unlabeled test set. We will compare your prediction with the
ground-truth labels of the test set on our side. Grading will be based on the ranking of your submitted prediction among
all of those in the class.

(Please make sure to read the Q&A part)

# Data and Jupyter Notebook

A compressed `ZIP` file is to be released on Blackboard when the assignment is available. The uncompressed archive
contain the following files:

- `main.ipynb`: The Python 3 Jupyter notebook you will need to fill in with your training and inference code, and
predict the results.
- **Dataset**:
  - `train_enc.tsv`: labeled training data. Each line a `'\t'` separated tuple in the form of (label, ciphertext
  sentence).
  - `dev_enc.tsv`: labeled dev data.
  - `test_enc_unlabeled.tsv`: unlabeled test data. Every line is a ciphertext sentence. 
- `upload_document.txt`: the documentation file where you need to fill in the blanks to describe your method.

# Programs

The provided Jupyter notebook already contains the beginning part of code for reading the data, and the end part to
generate `"upload_predictions.txt"`. You need to fill in the `"Main Code Body"`, and put the `2028 predicted labels`
into the results list.

*Restrictions.* Your method needs to be implemented using `python 3`, and should be executable on a single personal
machine (e.g., your own laptop). Other than those, you are free to use any python package
(e.g., pytorch, gensim, sklearn, fasttext, etc.).

# Submission

This assignment requests submitting three files (DO NOT CHANGE the filenames!):
- `upload_predictions.txt`: The predictions of your model on the 2028 unlabeled test set ciphertext sentences.
This file should have **exactly 2028 lines, every line is either 0 or 1**. (submit this on Vocareum)
- `upload_document.txt`: Fill in the blanks of that file to accordingly describe how your model represents, encodes
and classifies the ciphertext, and how you have developed the model. (submit this on Blackboard)
- `main.ipynb`: This Jupyter notebook already contains the beginning part to read the data, and the end part to
generate `"upload_predictions.txt"`. You need to fill in the "Main Code Body" (submit this on Blackboard). 

Multiple submissions are allowed; only the final submission will be graded. Do not include any other files in your
submission.  You are encouraged to submit early and often in order to iron out any problems, especially issues with the
format of the final output.

We will grade using a **leaderboard protocol**: the ground-truth labels on the test set are not released to you, and we
will compare your prediction with them to calculate the accuracy of your prediction.

The prediction of your predictions will be measured automatically; failure to format your output correctly may result
in very low scores, which will not be changed.

For full credit, make sure to submit your assignment well before the deadline. The time of submission recorded by the
system is the time used for determining late penalties. If your submission is received late, whatever the reason
(including equipment failure and network latencies or outages), it will incur a late penalty.

# Grading

We will grade using a leaderboard protocol. After the due date, we will calculate the accuracy of your submitted
prediction. Then your grade will be decided based on the standing of your submission among all valid ones. Specifically,
the top 20% valid submissions will get a score of 10, then the next 20% will get a score of 9, etc. The bottomline score
of a valid submission will be 6. However, your submission will be considered invalid and will result in a score lower
than the bottomline or of zero if one of the following happens:

- The accuracy of your submission is very much close to a trivial baseline performance (e.g., random guessing).

- The code in your submitted jupyter notebook obviously cannot reproduce your predictions.

- You haven't submitted the documentation file, so we don't know how your results can be reproduced; or, based on the
submitted document, we find factual mistakes of your method that should cause it to not work
(e.g., giving random or nonsensical predictions).

- Your submission has been redflagged by plagiarism checking.

# Q&A

> **How is the ciphertext encrypted?** Some encryption algorithm that was much more complicated than a Caesar Cipher was applied to encrypt every word in the
original text (punctuations were not encrypted). Words are still separated with whitespaces after the encryption.
Labels were unchanged.

> **How many labels are there?**
>This is a binary classification task. Only two labels are used: 0 and 1.

> **Does the ciphertext contain non-ascii characters:** 
> Yes. So make sure you read file using `encoding='utf-8'`, as it has been written in the Jupyter notebook.

> **Is there a pre-trained word embedding for this ciphertext?**
> No.

> **Are the test data from the same distribution of the training/dev data?**
> Yes, they were splits from the same dataset.

> **Is the dataset balanced?**
> Almost balanced.

> **How do I know if my method is well-performing or not?**
> You can try to tell it by the dev set performance.

> **What's the evaluation metric?**
> Accuracy.

> **Can I use bag-of-words + a simple FFNN classifier?**
> This could be a meaningful baseline method. But you want to try other representation techniques and classifiers to
> get better performance.

> **Can I try to decipher the ciphertext?**
> We do not forbid you to do so. But that is most likely going to be a waste of time (the encryption algorithm is not
> that easy to hack, and that is also not going to provide you a huge advantage in getting accurate predictions).

> **Is there a single best solution?**
> This assignment is an open-ended problem. So there is hardly a single best solution (don't ever try to ask TAs about
> it: they do not know it either).