import re
import string

def remove_digits(text):
    return ''.join(filter(lambda c: not c.isdigit(), text))

def reverse_string(text):
    return text[::-1]

def reverse_words(text):
    return ' '.join(text.split()[::-1])

def to_title_case(text):
    return text.title()

def is_palindrome(text):
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]

def is_anagram(s1,s2):
    return sorted(s1.lower()) == sorted(s2.lower())

def char_frequency(text):
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    return freq

def remove_whitespace(text):
    return ''.join(text.split())

def word_count(text):
    return len(text.split())
