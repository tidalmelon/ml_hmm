#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Date: 2017/06/20 17:43:11
"""

class State(object):
    """
    B: begin
    S: single
    E: end
    M: middle
    """
    B = 0
    S = 1
    E = 2
    M = 3

    NAMES = ['b', 's', 'e', 'm']

    @classmethod
    def getName(cls, idx):
        return cls.NAMES[idx]

    @classmethod
    def getSize(cls):
        return len(cls.NAMES)


class Token(object):

    def __init__(self, word, state):
        self.word = word
        self.state = state


if __name__ == '__main__':

    print State.getName(State.B)
    print State.getSize()

