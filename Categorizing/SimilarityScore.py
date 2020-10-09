"""
Takes a string (usually customer request), and calculates a similrity score for every FAQ question in our dataset.
"""

import math
import pandas as pd
import pickle
import Utils

WORDCOUNTS = 'wordcounts_faq.p'
IGNOREWORDS = 'ignore_words.p'
FAQ = 'faq.p'  # TODO: Include links


def calculate(customer_request):

    def take_frequent_word(word_tuple, counts):
        if isinstance(word_tuple, str):
            return word_tuple
        w1, w2 = word_tuple
        if w1 == '':
            return w2
        try:
            c1 = counts[w1]
            c2 = counts[w2]
            if c2 > c1:
                return w2
        except KeyError:
            return w1
        return w1

    wordcounts = pickle.load(open(WORDCOUNTS, 'rb'))
    top_frequent = pickle.load(open(IGNOREWORDS, 'rb'))
    faq = pickle.load(open(FAQ, 'rb'))
    sims = {}
    for q, a in faq.items():
        q_aslist = Utils.str_to_words(q)
        overlap_t = Utils.basically_same(q_aslist, customer_request, ret_tuples=True)  # Get overlapping words between request and question
        overlap = [take_frequent_word(wt, wordcounts) for wt in overlap_t]
        if not overlap:
            continue
        sims[q] = calc_speciality(wordcounts, overlap, top_frequent)
    ordered_faqs = sorted([(count, q) for q, count in sims.items()], reverse=True)
    # tok_to_count = {t: wordcounts[tokens[t]] for t in tokens}
    return ordered_faqs


def calc_speciality(alphabet, words_for_h, tops):
    """
    Calculates the entropy of a single word based on our ground truth (FAQ data)
    :param alphabet: Actually a dictionary of the for 'word':frequency.
    :param words_for_h: List of words to calculate the entropy over
    :return: the entropy of that word
    """
    tot_count = 0
    if -1 in alphabet:  # Special key reserved for that purpose
        tot_count = alphabet[-1]
    else:
        for _, count in alphabet.items():
            tot_count += count
    h = 0
    for word in words_for_h:
        if word not in alphabet or word == '':
            continue
        if word in tops:
            continue  # Ignore most common words
        p = alphabet[word] / tot_count
        # h -= p * math.log2(p)
        h -= math.log2(p)
        if h / len(words_for_h):
            return h / len(words_for_h)
    return h / len(words_for_h)


def str2alphabet(str_in):
    list_of_words = Utils.str_to_words(str_in)
    return Utils.words_to_frequency(list_of_words)


if __name__ == '__main__':
    myrequest = 'guten Tag, ich möchte gerne meine Strom Energie Zähler zerstören'
    test = calculate(Utils.str_to_words(myrequest))
    req = ['hallo', 'ich', 'habe', 'ein', 'problem', 'mit', 'meinem', 'internet', 'tv', 'glasfaser', 'router']
