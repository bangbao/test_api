# coding: utf-8
import unittest
import itertools
from __init__ import BattleField
from __init__ import P1, P3, P5, P6, P7, P9, P11, P12
from __init__ import NEIGHBORS_POS

mapinfo = {'defend': [14, 50, 68, 86, 34, 70, 88], 
           'focus': {'attack': {'y': 0, 'x': 0}, 
                     'defend': {'y': 0, 'x': 20}}, 
           'attack': [2, 38, 56, 74, 18, 54, 72], 
           'useless': 2, 
           'max_pos': 89, 
           'pixel': 80, 
           'size': (18, 7)
}

bf = BattleField(mapinfo)

a = 0
b = 1
c = 18

samples = [
    (a, b, 0, True),
    (a, b, 1, False),
    (b, a, 1, True),
    (b, a, 0, False),
    (a, c, 0, True),
    (c, a, 0, True),
    (a, c, 1, True),
    (c, a, 1, True),
]

fixed = {
    P1: ((0, True), (1, False)),
    P3: ((0, True), (1, False)),
    P5: ((0, True), (1, False)),
    P6: ((0, True), (1, True)),
    P7: ((0, False), (1, True)),
    P9: ((0, False), (1, True)),
    P11: ((0, False), (1, True)),
    P12: ((0, True), (0, True)),
}

class FaceToTest(unittest.TestCase):
    def test_turn(self):
        for i, (pos, goal, current, result) in enumerate(samples):
            self.assertEqual(bf.face_to(pos, goal, current), result, samples[i])

    def test_all(self):
        i = 0
        for pos, (positions, realness) in enumerate(itertools.imap(bf.arounds, 
                                                                   xrange(bf.maxpos))):
            for p, values in fixed.iteritems():
                if not realness[p]: 
                    continue
                for ft, result in values:
                    i += 1
                    self.assertEqual(bf.face_to(pos, positions[p], ft), 
                                     result, (pos, positions[p], ft, result))

        print i

if __name__ == '__main__':
    unittest.main()
