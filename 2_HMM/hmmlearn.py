import sys


def word_preprocess(word):
    return word


if __name__ == '__main__':
    words_set = set()
    tags_dict = {'START': 0, 'END': 0}
    emission_dict = {}
    transition_dict = {}
    DATA_ADDRESS = sys.argv[1]
    with open(DATA_ADDRESS, encoding='utf-8') as input_file:
        lines = input_file.readlines()
        for line in lines:
            tokens = line.split()
            last_tag = 'START'

            for token in tokens:
                token_split = token.rsplit('/', 1)
                tag = token_split[1]
                word = word_preprocess(token_split[0])
                if tag not in tags_dict.keys():
                    tags_dict[tag] = 1
                else:
                    tags_dict[tag] += 1

                transition_tuple = (last_tag, tag)
                if transition_tuple not in transition_dict.keys():
                    transition_dict[transition_tuple] = 1
                else:
                    transition_dict[transition_tuple] += 1

                last_tag = tag

                emission_tuple = (tag, word)
                if emission_tuple not in emission_dict.keys():
                    emission_dict[emission_tuple] = 1
                else:
                    emission_dict[emission_tuple] += 1

                words_set.add(word)

            if (tag, 'END') not in transition_dict.keys():
                transition_dict[(tag, 'END')] = 1
            else:
                transition_dict[(tag, 'END')] += 1

            tags_dict['START'] += 1
            tags_dict['END'] += 1

    # Smoothing for transitions
    for tag in tags_dict.keys():
        for tag2 in tags_dict.keys():
            if tag == 'END':
                continue
            if tag2 == 'START':
                continue
            if tag == 'START' and tag2 == 'END':
                continue
            if (tag, tag2) not in transition_dict.keys():
                transition_dict[(tag, tag2)] = 1
                # Smoothing!
                tags_dict[tag] += 1
    assert ('START', 'END') not in transition_dict.keys()

    # Transition dictionary length = number of tags ^ 2 + ('START', tags) + (tass, 'END')
    assert len(transition_dict) == (len(tags_dict) - 2) ** 2 + 2 * (len(tags_dict) - 2)

    for transition in transition_dict.keys():
        transition_dict[transition] = transition_dict[transition] / tags_dict[transition[0]]
        assert transition_dict[transition] <= 1, 'Something wrong with smoothing transition probabilities'

    for emission in emission_dict.keys():
        tag = emission[0]
        emission_dict[emission] = emission_dict[emission] / tags_dict[tag]
        assert emission_dict[emission] <= 1, 'Something wrong with emission probabilities'

    with open('hmmmodel.txt', 'w', encoding='utf-8') as f:
        f.truncate(0)
        f.write(f'{words_set}\n')
        f.write(f'{tags_dict}\n')
        f.write(f'{transition_dict}\n')
        f.write(f'{emission_dict}\n')
