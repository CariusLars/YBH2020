"""Utility functions"""
from difflib import SequenceMatcher
import itertools
import math
import re


def str_to_words(in_string):
    words = re.split(' |\n|\\.|/', in_string)
    # Split the words, delete punctiation and delete words that are actually only punctuation
    # We ignore upper/lower case
    words = [t.strip().lower() for t in words if not re.fullmatch('[ ,.]*', t)]
    return words


def words_to_frequency(list_of_words, w_dict=None, add_total=True):
    if w_dict is None:
        w_dict = {}
    for w in list_of_words:
        if w not in w_dict:
            w_dict[w] = 1
        else:
            w_dict[w] += 1
    if add_total:
        if -1 in w_dict:
            w_dict[-1] += len(list_of_words)
        else:
            w_dict[-1] = len(list_of_words)

    return w_dict


def basically_same(list1, list2, ret_tuples=False):
    """Returns a list of words that are contained in both lists (or that are veeery similar in both lists)"""
    def samesame(words):
        w1, w2 = words
        if w1 == w2:
            if ret_tuples:
                return (w1, w2)
            return w1
        if len(w1+w2) >= 10:
            if (w1 + 'r' == w2) or (w1 + 's' == w2) or (w1 + '-' == w2):
                print(w1, w2)
                return (w1, w2)
            if (w2 + 'r' == w1) or (w2 + 's' == w1) or (w2 + '-' == w1):
                print(w1, w2)
                return (w1, w2)
        if ret_tuples:
            return ('', '')
        return ''
    ret = list(map(samesame, itertools.product(list1, list2)))
    return ret
