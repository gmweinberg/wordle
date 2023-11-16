#!/usr/bin/env python
"""Find remaining words"""

import sys
import re
from collections import defaultdict

verbose = True
class WordsLeft:
    def __init__(self):
        self.history = [] # guesses and results. each elm is a 10 char string, first 5 are guess, second 5 are results, yellow lowercase, green upercase, grey dot
        patternelm = '['
        self.counts = {} # key = char, value = (min, max)
        for ii in range(ord('a'), ord('z') + 1):
            char = chr(ii)
            self.counts[char] = [0, 5]
            patternelm += char
        patternelm += ']'
        self.pattern = [patternelm] * 5
        with open('words', 'r') as f:
            self.words = set([aline.strip() for aline in f.readlines()])

    def addGuess(self, guess):
        self.history.append(guess)
        hits = defaultdict(int) # green + yellow
        ghits = defaultdict(int) # green only

        for ii in range(5):
            char = guess[ii]
            if guess[ii + 5] == '.':
                if hits.get(char, 0) == 0: # this letter is not in the word at all
                    self.counts[char][1] = 0
                    for ii in range(len(self.pattern)):
                        self.pattern[ii] = self.pattern[ii].replace(char, '')
                else:
                    self.counts[char][1] = hits[char]
            elif guess[ii + 5] == guess[ii + 5].lower(): # yellow
                hits[char] += 1
                if self.counts[char][0] < hits[char]:
                    self.counts[char][0] = hits[char]
                self.pattern[ii] = self.pattern[ii].replace(char, '')
            else:
                hits[char] += 1
                ghits[char] += 1
                if self.counts[char][0] < hits[char]:
                    self.counts[char][0] = hits[char]
                self.pattern[ii] = char
        for char in ghits.keys():
            if ghits[char] == self.counts[char][1]: # we found all of them:
                for ii in range(len(self.pattern)):
                    if self.pattern[ii] != char:
                        self.pattern[ii] = self.pattern[ii].replace(char, '')
        if verbose:
            print('pattern', self.pattern, 'counts', self.counts)
        self.parewords()

    def parewords(self):
        """Eliminate any words which do not fit our pattern."""
        pattern = ''.join(self.pattern)
        delwords = []
        for word in self.words:
            if not re.match(pattern, word):
                delwords.append(word)
        for word in delwords:
            self.words.remove(word)
        if verbose:
            print('after pattern check delwords {}'.format(len(delwords)))
        delwords = set()
        for char in self.counts:
            if self.counts[char][0] == self.counts[char][1]:
                continue
            if self.counts[char][0] == 0 and self.counts[char][1] == 5:
                continue
            for word in self.words:
                count = word.count(char)
                if count < self.counts[char][0] or count > self.counts[char][1]:
                    delwords.add(word)
        if verbose:
            print('after counts check delwords {}'.format(len(delwords)))
        for word in delwords:
            self.words.remove(word)
        print(len(self.words), 'remaining words')
        if len(self.words) < 20:
            print(self.words)

    def doGuesses(self):
        for line in sys.stdin:
            guess = line.strip()
            if verbose:
                print('guess', guess)
            self.addGuess(guess)
            if len(self.words) == 1:
                break

    def doDebug(self):
        for guess in ['penispE...', 'delayDE...', 'depotDEP.t']:
            self.addGuess(guess)


if __name__ == '__main__':
    wl = WordsLeft()
    #wl.doDebug()
    wl.doGuesses()



