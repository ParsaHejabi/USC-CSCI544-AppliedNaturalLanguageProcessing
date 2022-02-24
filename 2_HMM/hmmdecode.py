import math
import sys

from hmmlearn import word_preprocess


def get_open_class_tags(emission_dictionary, use_frequency_of_tags=False, divider_number=5):
    open_class_tags = {}
    if use_frequency_of_tags:
        open_class_tags = sorted(tags_dict.items(), key=lambda x: x[1] if x[0] != 'START' and x[0] != 'END' else 0,
                                 reverse=True)[:divider_number]
    else:
        for tag, word in emission_dictionary:
            if tag not in open_class_tags.keys():
                open_class_tags[tag] = set(word.lower())
            else:
                open_class_tags[tag].add(word.lower())

        open_class_tags = {tag: len(open_class_tags[tag]) for tag in open_class_tags}

        # TODO: Change the number 5
        open_class_tags = sorted(open_class_tags.items(), key=lambda x: x[1], reverse=True)[:divider_number]
    return open_class_tags


if __name__ == "__main__":
    DATA_ADDRESS = sys.argv[1]
    MODEL_ADDRESS = 'hmmmodel.txt'

    with open(MODEL_ADDRESS, 'r', encoding='utf-8') as model_file:
        model = model_file.readlines()
        words_set = eval(model[0])
        tags_dict = eval(model[1])
        transition_dict = eval(model[2])
        emission_dict = eval(model[3])

    open_class_tags = get_open_class_tags(emission_dict)
    predictions = []
    # TODO: Skip zero probability tags
    # TODO: Use numpy vectorization to speed up and use max()
    with open(DATA_ADDRESS, encoding='utf-8') as input_file:
        lines = input_file.readlines()
        for line in lines:
            words = line.split()
            tag_sequence = ['START']
            prob = 0
            prediction = ''
            for word in words:
                word = word_preprocess(word)
                best_new_prob = -math.inf
                for transition in transition_dict.keys():
                    if transition[0] == tag_sequence[-1]:
                        if word in words_set:
                            if (transition[1], word) in emission_dict.keys():
                                new_prob = prob + math.log(transition_dict[transition]) + math.log(
                                    emission_dict[(transition[1], word)])
                                if new_prob > best_new_prob:
                                    best_new_prob = new_prob
                                    best_tag = transition[1]
                        else:
                            if transition[1] in open_class_tags:
                                # Emission probability is zero for unseen words
                                new_prob = prob + math.log(transition_dict[transition])
                                if new_prob > best_new_prob:
                                    best_new_prob = new_prob
                                    best_tag = transition[1]
                tag_sequence.append(best_tag)
                prob += best_new_prob
                prediction += '{}/{} '.format(word, best_tag)
            predictions.append(prediction)

    with open('hmmoutput.txt', 'w', encoding='utf-8') as output_file:
        output_file.truncate(0)
        for prediction in predictions:
            output_file.write(f'{prediction.strip()}\n')
