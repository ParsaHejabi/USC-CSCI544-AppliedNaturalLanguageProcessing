import math
import os
import sys
from glob import glob

from nblearn import preprocess

def get_max_variable(truthful_positive, truthful_negative, deceptive_positive, deceptive_negative):
    """
    a function that gets truthful_positive, truthful_negative, deceptive_positive, deceptive_negative and returns
    the name of the maximum variable
    """
    if truthful_positive > deceptive_positive:
        if truthful_positive > truthful_negative:
            if truthful_positive > deceptive_negative:
                return 'truthful_positive'
            else:
                return 'deceptive_negative'
        else:
            if truthful_negative > deceptive_negative:
                return 'truthful_negative'
            else:
                return 'deceptive_negative'
    else:
        if deceptive_positive > deceptive_negative:
            if deceptive_positive > truthful_negative:
                return 'deceptive_positive'
            else:
                return 'truthful_negative'
        else:
            if deceptive_negative > truthful_negative:
                return 'deceptive_negative'
            else:
                return 'truthful_negative'


if __name__ == "__main__":
    DATA_ADDRESS = sys.argv[1]
    MODEL_ADDRESS = 'nbmodel.txt'

    # extract the data from nbmodel.txt
    with open(MODEL_ADDRESS, 'r') as review_file:
        model = review_file.readlines()
        b_classifier_priors_1 = eval(model[0])
        b_classifier_priors_2 = eval(model[1])
        f_classifier_priors = eval(model[2])
        vocab = eval(model[3])
        probs = eval(model[4])

    for review_address in glob(os.path.join(DATA_ADDRESS, '*', '*', '*', '*.txt')):
        with open(review_address, 'r') as review_file:
            review = review_file.readlines()
            review = review[0]
            review = preprocess(review)
            truthful_prob = math.log(b_classifier_priors_1['truthful'])
            deceptive_prob = math.log(b_classifier_priors_1['deceptive'])
            positive_prob = math.log(b_classifier_priors_2['positive'])
            negative_prob = math.log(b_classifier_priors_2['negative'])
            truthful_positive_prob = math.log(f_classifier_priors['truthful_positive'])
            truthful_negative_prob = math.log(f_classifier_priors['truthful_negative'])
            deceptive_positive_prob = math.log(f_classifier_priors['deceptive_positive'])
            deceptive_negative_prob = math.log(f_classifier_priors['deceptive_negative'])
            for word in review.split():
                if word in vocab:
                    truthful_prob += math.log(probs[(word, 'truthful')])
                    deceptive_prob += math.log(probs[(word, 'deceptive')])
                    positive_prob += math.log(probs[(word, 'positive')])
                    negative_prob += math.log(probs[(word, 'negative')])
                    truthful_positive_prob += math.log(probs[(word, 'truthful_positive')])
                    truthful_negative_prob += math.log(probs[(word, 'truthful_negative')])
                    deceptive_positive_prob += math.log(probs[(word, 'deceptive_positive')])
                    deceptive_negative_prob += math.log(probs[(word, 'deceptive_negative')])

            b_classifier_1_result = 'truthful' if truthful_prob > deceptive_prob else 'deceptive'
            b_classifier_2_result = 'positive' if positive_prob > negative_prob else 'negative'
            f_classifier_result = get_max_variable(truthful_positive_prob, truthful_negative_prob,
                                                   deceptive_positive_prob, deceptive_negative_prob)

            # append b_classifier_1 and b_classifier_2 results to the nboutput.txt file in the format of
            # 'b_classifier_1_result b_classifier_2_result' and path of review_file
            with open('nboutput.txt', 'a') as output_file:
                output_file.write(
                    f"{b_classifier_1_result} {b_classifier_2_result} {os.path.abspath(review_address)}\n")
