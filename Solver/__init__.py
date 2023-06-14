from collections import namedtuple


alphabet = list('abcdefghijklmnopqrstuvwxyz')
parameters = ['parent', 'letter', 'wordToHere', 'terminatingWord']+alphabet
defaults = [None, '', '', False]+[None for _ in alphabet]
LetterNode = namedtuple('LetterNode', parameters, defaults=defaults)

from .Tree import *
