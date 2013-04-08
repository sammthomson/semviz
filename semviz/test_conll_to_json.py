"""
Author: Sam Thomson (sthomson@cs.cmu.edu)
"""
from unittest import TestCase, main
from semviz.conll_to_json import encode_conll

CONLL_DATA = """1	We	_	PRP	PRP	_	3	nsubj	_	_
2	're	_	VB	VBP	_	3	aux	_	_
3	about	_	IN	IN	_	0	null	_	_
4	to	_	TO	TO	_	5	aux	_	_
5	see	_	VB	VB	_	3	xcomp	_	_
6	if	_	IN	IN	_	8	mark	_	_
7	advertising	_	NN	NN	_	8	nn	_	_
8	works	_	NN	NNS	_	5	dobj	_	_
9	.	_	.	.	_	3	punct	_	_
"""
EXPECTED = {
    'entities': [
        ['T1', 'PRP', [[0, 2]]],
        ['T2', 'VBP', [[3, 6]]],
        ['T3', 'IN', [[7, 12]]],
        ['T4', 'TO', [[13, 15]]],
        ['T5', 'VB', [[16, 19]]],
        ['T6', 'IN', [[20, 22]]],
        ['T7', 'NN', [[23, 34]]],
        ['T8', 'NNS', [[35, 40]]],
        ['T9', '.', [[41, 42]]]],
    'relations': [
        ['R1', 'nsubj', [['Arg1', 'T3'], ['Arg2', 'T1']]],
        ['R2', 'aux', [['Arg1', 'T3'], ['Arg2', 'T2']]],
        ['R3', 'aux', [['Arg1', 'T5'], ['Arg2', 'T4']]],
        ['R4', 'xcomp', [['Arg1', 'T3'], ['Arg2', 'T5']]],
        ['R5', 'mark', [['Arg1', 'T8'], ['Arg2', 'T6']]],
        ['R6', 'nn', [['Arg1', 'T8'], ['Arg2', 'T7']]],
        ['R7', 'dobj', [['Arg1', 'T5'], ['Arg2', 'T8']]],
        ['R8', 'punct', [['Arg1', 'T3'], ['Arg2', 'T9']]]],
    'text': "We 're about to see if advertising works ."}


class TestConllToJson(TestCase):
    maxDiff = None

    def test_encode_conll(self):
        output = encode_conll(CONLL_DATA)
        self.assertEqual(EXPECTED, output)

    def test_encode_empty_sentence(self):
        output = encode_conll("")
        self.assertEqual({'entities': [], 'relations': [], 'text': ""}, output)


if __name__ == "__main__":
    main()
