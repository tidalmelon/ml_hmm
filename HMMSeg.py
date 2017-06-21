#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Date: 2017/06/21 15:51:00
"""
from util import State

class HMMSeg(object):

    def __init__(self, mname='hmm.model'):
        self.origProb = None
        self.emisProb = {}
        self.transProb = []

        self.mname = mname
        self.__loadDict()

    def __loadDict(self):

        with open(self.mname) as f:
            # 初始概率
            arr = f.readline().strip().split()
            arr = [float(e) for e in arr]
            self.origProb = arr
            
            # 转移概率
            arr = f.readline().strip().split()
            arr = [float(e) for e in arr]
            self.transProb.append(arr)
            
            arr = f.readline().strip().split()
            arr = [float(e) for e in arr]
            self.transProb.append(arr)

            arr = f.readline().strip().split()
            arr = [float(e) for e in arr]
            self.transProb.append(arr)

            arr = f.readline().strip().split()
            arr = [float(e) for e in arr]
            self.transProb.append(arr)

            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip().decode('utf-8')
                arr = line.split()
                w = arr[0]
                arr_state = [float(e) for e in arr[1:]]

                self.emisProb[w] = arr_state

    def split(self, sen):
        if not sen:
            return None

        if not isinstance(sen, unicode):
            raise Exception('encode err')

        stageLength = len(sen)

        probMatrix = [[0.0 for e in range(State.getSize())] for _ in range(stageLength)]
        bestPre = [[0 for e in range(State.getSize())] for _ in range(stageLength)]

        for s in range(State.getSize()):
            probMatrix[0][s] = self.origProb[s]

        for stage in range(stageLength)[1:]:
            key = sen[stage-1]

            emis = self.emisProb.get(key)
            print key, 'emis', emis
            preProb = probMatrix[stage-1]

            for cur in range(State.getSize()):
                mx = float('-inf')
                bestpre = 0
                for pre in range(State.getSize()):
                    res = preProb[pre] + emis[pre] + self.transProb[pre][cur]
                    if res > mx:
                        bestpre = pre
                        mx = res

                bestPre[stage][cur] = bestpre
                probMatrix[stage][cur] = mx
        
        max_last = float('-inf')
        best_last = -1
        for i in range(State.getSize()):
            if probMatrix[stageLength-1][i] > max_last:
                best_last = i
                max_last = probMatrix[stageLength-1][i]

        marks = [0 for _ in range(stageLength)]
        marks[stageLength-1] = best_last
        for stage in range(stageLength)[1:][::-1]:
            marks[stage-1] = bestPre[stage][marks[stage]]

        for i in range(stageLength):
            print sen[i], State.getName(marks[i])


if __name__ == '__main__':
    seg = HMMSeg()
    sen = u'在建设有中国特色的社会主义道路上'
    sen = u'也是为了批判地吸取和概括各门科学发展的最新成果'
    seg.split(sen)

