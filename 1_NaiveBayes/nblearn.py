import sys
from glob import glob
import os
import re
import string


def preprocess(text):
    """
    Remove punctuation, lowercase, numbers and extra spaces
    :param text:
    :return:
    """
    text = text.strip().lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    if len(text) <= 3:
        return None
    return text


if __name__ == "__main__":
    DATA_ADDRESS = sys.argv[1]
    dataset = []
    probs = {}
    vocab = set()

    for review_address in glob(os.path.join(DATA_ADDRESS, 'negative_polarity', '*', '*', '*.txt')):
        second_label = 'truthful' if os.path.basename(review_address).split('_')[0] == 't' else 'deceptive'
        second_label_negate = 'deceptive' if os.path.basename(review_address).split('_')[0] == 't' else 'truthful'
        with open(review_address) as f:
            lines = f.readlines()
            assert len(lines) == 1, 'Original dataset problem!?'
            review = preprocess(lines[0])
            for word in review.split():
                if word not in vocab:
                    probs[(word, 'negative')] = 1
                    probs[(word, 'positive')] = 0
                    probs[(word, second_label)] = 1
                    probs[(word, second_label_negate)] = 0
                    probs[(word, f'{second_label}_negative')] = 1
                    probs[(word, f'{second_label}_positive')] = 0
                    probs[(word, f'{second_label_negate}_negative')] = 0
                    probs[(word, f'{second_label_negate}_positive')] = 0
                    vocab.add(word)
                else:
                    probs[(word, 'negative')] += 1
                    probs[(word, second_label)] += 1
                    probs[(word, f'{second_label}_negative')] += 1
            dataset.append((lines[0], 'negative', second_label))

    for review_address in glob(os.path.join(DATA_ADDRESS, 'positive_polarity', '*', '*', '*.txt')):
        second_label = 'truthful' if os.path.basename(review_address).split('_')[0] == 't' else 'deceptive'
        second_label_negate = 'deceptive' if os.path.basename(review_address).split('_')[0] == 't' else 'truthful'
        with open(review_address) as f:
            lines = f.readlines()
            assert len(lines) == 1, 'Original dataset problem!?'
            review = preprocess(lines[0])
            for word in review.split():
                if word not in vocab:
                    probs[(word, 'positive')] = 1
                    probs[(word, 'negative')] = 0
                    probs[(word, second_label)] = 1
                    probs[(word, second_label_negate)] = 0
                    probs[(word, f'{second_label}_positive')] = 1
                    probs[(word, f'{second_label}_negative')] = 0
                    probs[(word, f'{second_label_negate}_negative')] = 0
                    probs[(word, f'{second_label_negate}_positive')] = 0
                    vocab.add(word)
                else:
                    probs[(word, 'positive')] += 1
                    probs[(word, second_label)] += 1
                    probs[(word, f'{second_label}_positive')] += 1
            dataset.append((lines[0], 'positive', second_label))

    b_classifier_priors_1 = {'truthful': 0, 'deceptive': 0}
    b_classifier_priors_2 = {'positive': 0, 'negative': 0}
    f_classifier_priors = {'truthful_positive': 0, 'truthful_negative': 0, 'deceptive_positive': 0,
                           'deceptive_negative': 0}

    for row in dataset:
        if row[1] == 'positive' and row[2] == 'truthful':
            b_classifier_priors_1['truthful'] += 1
            b_classifier_priors_2['positive'] += 1
            f_classifier_priors['truthful_positive'] += 1
        elif row[1] == 'negative' and row[2] == 'truthful':
            b_classifier_priors_1['truthful'] += 1
            b_classifier_priors_2['negative'] += 1
            f_classifier_priors['truthful_negative'] += 1
        elif row[1] == 'positive' and row[2] == 'deceptive':
            b_classifier_priors_1['deceptive'] += 1
            b_classifier_priors_2['positive'] += 1
            f_classifier_priors['deceptive_positive'] += 1
        elif row[1] == 'negative' and row[2] == 'deceptive':
            b_classifier_priors_1['deceptive'] += 1
            b_classifier_priors_2['negative'] += 1
            f_classifier_priors['deceptive_negative'] += 1

    b_classifier_priors_1 = {k: v / len(dataset) for k, v in b_classifier_priors_1.items()}
    b_classifier_priors_2 = {k: v / len(dataset) for k, v in b_classifier_priors_2.items()}
    f_classifier_priors = {k: v / len(dataset) for k, v in f_classifier_priors.items()}

    b = len(vocab)

    for word in vocab:
        probs[(word, 'truthful')] = (probs[(word, 'truthful')] + 1) / (b_classifier_priors_1['truthful'] + b)
        probs[(word, 'deceptive')] = (probs[(word, 'deceptive')] + 1) / (b_classifier_priors_1['deceptive'] + b)
        probs[(word, 'positive')] = (probs[(word, 'positive')] + 1) / (b_classifier_priors_2['positive'] + b)
        probs[(word, 'negative')] = (probs[(word, 'negative')] + 1) / (b_classifier_priors_2['negative'] + b)
        probs[(word, 'truthful_positive')] = (probs[(word, 'truthful_positive')] + 1) / (
                f_classifier_priors['truthful_positive'] + b)
        probs[(word, 'truthful_negative')] = (probs[(word, 'truthful_negative')] + 1) / (
                f_classifier_priors['truthful_negative'] + b)
        probs[(word, 'deceptive_positive')] = (probs[(word, 'deceptive_positive')] + 1) / (
                f_classifier_priors['deceptive_positive'] + b)
        probs[(word, 'deceptive_negative')] = (probs[(word, 'deceptive_negative')] + 1) / (
                f_classifier_priors['deceptive_negative'] + b)

    with open('nbmodel.txt', 'w') as f:
        f.truncate(0)
        f.write(f'{b_classifier_priors_1}\n')
        f.write(f'{b_classifier_priors_2}\n')
        f.write(f'{f_classifier_priors}\n')
        f.write(f'{vocab}\n')
        f.write(f'{probs}\n')
