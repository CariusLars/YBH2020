"""Utility functions"""
import re


def str_to_words(in_string):
    words = re.split(' |\n|\\.|/', in_string)
    # Split the words, delete punctiation and delete words that are actually only punctuation
    # We ignore upper/lower case
    words = [t.strip().lower() for t in words if not re.fullmatch('[ ,.]*', t)]
    return words
