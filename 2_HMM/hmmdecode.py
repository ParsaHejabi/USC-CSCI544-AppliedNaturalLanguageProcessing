import math
import sys


def get_open_class_tags(emission_dictionary, use_frequency_of_tags=False, divider_number=5):
    open_class_tags = {}
    if use_frequency_of_tags == True:
        open_class_tags = sorted(tags_dict.items(), key=lambda x: x[1] if x[0] != 'START' and x[0] != 'END' else 0,
                                 reverse=True)[:divider_number]
    else:
        for tag, word in emission_dictionary:
            if tag not in open_class_tags.keys():
                open_class_tags[tag] = set()
                open_class_tags[tag].add(word)
            else:
                open_class_tags[tag].add(word)

        open_class_tags = {tag: len(open_class_tags[tag]) for tag in open_class_tags}
        open_class_tags = sorted(open_class_tags.items(), key=lambda x: x[1], reverse=True)[:divider_number]
    return open_class_tags


if __name__ == "__main__":
    DATA_ADDRESS = sys.argv[1]
    MODEL_ADDRESS = 'hmmmodel.txt'

    with open(MODEL_ADDRESS, 'r', encoding='utf-8') as model_file:
        model = model_file.readlines()
        words_set = eval(model[0])
        tags_dict = eval(model[1])
        tags_set = tags_dict.keys() - {'START', 'END'}
        transition_dict = eval(model[2])
        emission_dict = eval(model[3])

    open_class_tags = get_open_class_tags(emission_dict)
    predictions = []

    with open(DATA_ADDRESS, encoding='utf-8') as input_file:
        lines = input_file.readlines()
        for line in lines:
            words = line.split()

            matrix = {}
            father_tags = {}
            for index, word in enumerate(words):
                word_tuple = (word, index)
                matrix[word_tuple] = {}
                father_tags[word_tuple] = {}
                for tag in tags_dict:
                    if tag == 'START' or tag == 'END':
                        continue
                    else:
                        matrix[word_tuple][tag] = -math.inf
                        father_tags[word_tuple][tag] = ''

            # First column initialization
            first_word = (words[0], 0)
            for tag in tags_set:
                if first_word[0] in words_set:
                    transition_tuple = ('START', tag)
                    emission_tuple = (tag, first_word[0])
                    if emission_tuple in emission_dict.keys():
                        matrix[first_word][tag] = math.log(transition_dict[transition_tuple]) + math.log(
                            emission_dict[emission_tuple])
                        father_tags[first_word][tag] = 'START'
                else:
                    matrix[first_word][tag] = math.log(transition_dict[transition_tuple])
                    father_tags[first_word][tag] = 'START'

            # Other columns
            for index, word in enumerate(words[1:]):
                index += 1
                word_tuple = (word, index)
                for tag in tags_set:
                    if word_tuple[0] in words_set:
                        emission_tuple = (tag, word_tuple[0])
                        if emission_tuple in emission_dict.keys():
                            for prev_tag in tags_set:
                                if matrix[(words[index - 1], index - 1)][prev_tag] != -math.inf:
                                    transition_tuple = (prev_tag, tag)
                                    probability = matrix[(words[index - 1], index - 1)][prev_tag] + math.log(
                                        transition_dict[transition_tuple]) + math.log(emission_dict[emission_tuple])
                                    if probability > matrix[word_tuple][tag]:
                                        matrix[word_tuple][tag] = probability
                                        father_tags[word_tuple][tag] = prev_tag
                    else:
                        for prev_tag in tags_set:
                            if matrix[(words[index - 1], index - 1)][prev_tag] != -math.inf:
                                transition_tuple = (prev_tag, tag)
                                probability = matrix[(words[index - 1], index - 1)][prev_tag] + math.log(
                                    transition_dict[transition_tuple])
                                if probability > matrix[word_tuple][tag]:
                                    matrix[word_tuple][tag] = probability
                                    father_tags[word_tuple][tag] = prev_tag

            # Last column
            best_probability = -math.inf
            best_tag = ''
            last_word = (words[-1], len(words) - 1)
            for tag in tags_set:
                if matrix[last_word][tag] != -math.inf:
                    transition_tuple = (tag, 'END')
                    probability = matrix[last_word][tag] + math.log(transition_dict[transition_tuple])
                    if probability > best_probability:
                        best_probability = probability
                        best_tag = tag

            # Backtracking
            tags = []
            current_word = last_word[0]
            current_index = len(words) - 1
            current_tag = best_tag

            while current_tag != 'START':
                tags.append(current_tag)
                current_tag = father_tags[(current_word, current_index)][current_tag]
                current_word = words[current_index - 1]
                current_index -= 1

            tags.reverse()
            prediction = ''
            for index, word in enumerate(words):
                prediction += '{}/{} '.format(word, tags[index])

            predictions.append(prediction.strip())

    with open('hmmoutput.txt', 'w', encoding='utf-8') as output_file:
        output_file.truncate(0)
        for prediction in predictions:
            output_file.write(f'{prediction}\n')
