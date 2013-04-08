"""
Author: Sam Thomson (sthomson@cs.cmu.edu)
"""
from unittest import TestCase
from mock import Mock
from semviz.services import MstClient, PosTagger, UnicodeSocketClient

SENTENCES = u"""My kitchen no longer smells.
0.2 miles later the trail and the creek run nearly level with each other and the sound of Minnehaha Falls fills the air."""
POS_TAGGED = u"""My_PRP$ kitchen_NN no_RB longer_RB smells_VBZ ._.
0.2_CD miles_NNS later_RB the_DT trail_NN and_CC the_DT creek_NN run_NN nearly_RB level_NN with_IN each_DT other_JJ and_CC the_DT sound_NN of_IN Minnehaha_NNP Falls_NNP fills_VBZ the_DT air_NN ._."""
MST_RESPONSE = u"""1	my	my	PRP$	PRP$	-	2	NMOD	-	-	2	kitchen	kitchen	NN	NN	-	5	SUB	-	-	3	no	no	RB	RB	-	5	VMOD	-	-	4	longer	longer	RB	RB	-		AMOD	-	-	5	smells	smells	VBZ	VBZ	-	0	ROOT	-	-	6	.	.	.	.	-	5	P	-	-
1	<num>	<num>	CD	CD	-	2	NMOD	-	-	2	miles	miles	NNS	NNS	-	11	NMOD	-	-	3	later	later	RB	RB	-	11	NMOD	-	-	4	the	the	DT	DT	-	11	NMOD	-	-	5	trail	trail	NN	NN	-	11	NMOD		-	6	and	and	CC	CC	-	11	NMOD	-	-	7	the	the	DT	DT	-	11	NMOD	-	-	8	creek	creek	NN	NN	-	11	NMOD	-	-	9	run	run	NN	NN		11	NMOD	-	-	10	nearly	nearly	RB	RB	-	11	NMOD		-	11	level	level	NN	NN	-	17	NMOD	-	-	12	with	with	IN	IN	-	11	NMOD	-	-	13	each	each	DT	DT	-	14	NMOD	-	-	14	other	other	JJ	JJ		12	PMOD	-	-	15	and	and	CC	CC	-	17	NMOD		-	16	the	the	DT	DT	-	17	NMOD	-	-	17	sound	sound	NN	NN	-	21	SUB	-	-	18	of	of	IN	IN	-	17	NMOD	-	-	19	minnehaha	minnehaha	NNP	NNP	-	20	NMOD	-	-	20	falls	falls	NNP	NNP		18	PMOD	-	-	21	fills	fills	VBZ	VBZ	-	0	ROOT		-	22	the	the	DT	DT	-	23	NMOD	-	-	23	air	air	NN	NN	-	21	OBJ	-	-	24	.	.		.	-	21	P	-	-"""
CONLL = u"""1	My	My	PRP$	PRP$	-	2	NMOD	-	-
2	kitchen	kitchen	NN	NN	-	5	SUB	-	-
3	no	no	RB	RB	-	5	VMOD	-	-
4	longer	longer	RB	RB	-		AMOD	-	-
5	smells	smells	VBZ	VBZ	-	0	ROOT	-	-
6	.	.	.	.	-	5	P	-	-

1	0.2	0.2	CD	CD	-	2	NMOD	-	-
2	miles	miles	NNS	NNS	-	11	NMOD	-	-
3	later	later	RB	RB	-	11	NMOD	-	-
4	the	the	DT	DT	-	11	NMOD	-	-
5	trail	trail	NN	NN	-	11	NMOD		-
6	and	and	CC	CC	-	11	NMOD	-	-
7	the	the	DT	DT	-	11	NMOD	-	-
8	creek	creek	NN	NN	-	11	NMOD	-	-
9	run	run	NN	NN		11	NMOD	-	-
10	nearly	nearly	RB	RB	-	11	NMOD		-
11	level	level	NN	NN	-	17	NMOD	-	-
12	with	with	IN	IN	-	11	NMOD	-	-
13	each	each	DT	DT	-	14	NMOD	-	-
14	other	other	JJ	JJ		12	PMOD	-	-
15	and	and	CC	CC	-	17	NMOD		-
16	the	the	DT	DT	-	17	NMOD	-	-
17	sound	sound	NN	NN	-	21	SUB	-	-
18	of	of	IN	IN	-	17	NMOD	-	-
19	Minnehaha	Minnehaha	NNP	NNP	-	20	NMOD	-	-
20	Falls	Falls	NNP	NNP		18	PMOD	-	-
21	fills	fills	VBZ	VBZ	-	0	ROOT		-
22	the	the	DT	DT	-	23	NMOD	-	-
23	air	air	NN	NN	-	21	OBJ	-	-
24	.	.		.	-	21	P	-	-"""


class TestMstClient(TestCase):
    maxDiff = None

    def test_get_parses(self):
        # set up a mocked MST server
        pos_tagger = Mock(spec=PosTagger)
        pos_tagger.tag_sentences = Mock(return_value=POS_TAGGED)
        socket_client = Mock(spec=UnicodeSocketClient)
        socket_client.make_request = Mock(return_value=MST_RESPONSE)
        mst = MstClient(pos_tagger, socket_client)
        # exercise the MstClient
        output = mst.get_parses(SENTENCES)
        # verify that it called the server and reformatted the output correctly
        # this includes putting each token row on its own line, and
        # reverting any changes MST made to the token.
        pos_tagger.tag_sentences.assert_called_once_with(SENTENCES)
        socket_client.make_request.assert_called_once_with(POS_TAGGED)
        self.assertEqual(CONLL, output)
