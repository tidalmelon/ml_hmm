#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Date: 2017/06/19 17:40:18
"""
import math

from util import State


class HMMTrain(object):


    def __init__(self, input='RenMinData.input', mname='hmm.model'):
        self.fin = input

        self.transDic = 'hmm.model'
        self.original = [0 for i in range(State.getSize())]
        self.transFreq = [[0 for i in range(State.getSize())] for j in range(State.getSize())]
        self.stateFreq = [0 for i in range(State.getSize())]
        self.emisFreq = {}

        self.origProb = [0.0 for i in range(State.getSize())]
        self.emisProb = {}
        self.transProb = [[0.0 for i in range(State.getSize())] for j in range(State.getSize())]

    def train(self):
        with open(self.fin) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                sen = line.strip()
                tokens = self.__split(sen)
                self.__statisitcs(tokens)

    def calcOriginProb(self):
        total = sum(self.original)
        for s, c in enumerate(self.original):
            prob = math.log(float(c) / total)
            self.origProb[s] = prob


    def calcEmisProb(self):
        for w, c_arr in self.emisFreq.iteritems():
            self.emisProb[w] = [0.0 for i in range(State.getSize())]

            for s, c in enumerate(c_arr):
                if c == 0:
                    c = 0.0000001

                prob = math.log(float(c) / self.stateFreq[s])

                self.emisProb[w][s] = prob

    def calcTransProb(self):
        for c_s, c_arr in enumerate(self.transFreq):
            for n_s, c in enumerate(c_arr):
                # 加1平滑
                prob = math.log((float(c) + 1) / (self.stateFreq[c_s] + State.getSize()))
                self.transProb[c_s][n_s] = prob

    def __split(self, sen):
        tokens = []
        
        words = sen.split(' ')
        size = len(words)
        for word in words:
            if len(word) == 1:
                tokens.append((word, State.S))
            else:
                for i in range(size):
                    w = word[i]
                    if i == 0:
                        tokens.append((w, State.B))
                    elif i == (size-1):
                        tokens.append((w, State.E))
                    else:
                        tokens.append((w, State.M))
        return tokens

    def __statisitcs(self, tokens):
        w, s = tokens[0]
        self.original[s] += 1

        size = len(tokens)

        for i, (w, s) in enumerate(tokens):
            self.stateFreq[s] += 1

            if w not in self.emisFreq:
                arr = [0 for i in range(State.getSize())]
                arr[s] += 1
                self.emisFreq[w] = arr
            else:
                self.emisFreq[w][s] += 1

            if i <= (size-2):
                _, next_s = tokens[i+1]
                self.transFreq[s][next_s] += 1


















