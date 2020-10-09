"""
Takes a string (usually customer request), and calculates a similrity score for every FAQ question in our dataset.
"""

import pandas as pd
import pickle


def calculate():
    wordcounts = pickle.load(read('wordcounts_faw.p', 'rb'))
    tokens = {i: word for i, word in enumerate(wordcounts)}
    tok_to_count = {t: wordcounts[tokens[t]] for t in tokens}


def entropy(alphabet)