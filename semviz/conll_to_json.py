"""
Converts a dependency parse in conll format into json suitable for visualizing
with brat (brat.nlplab.org).

Author: Lingpeng Kong, Sam Thomson
"""
from semviz.pos_to_conll import ConllToken


def get_char_offsets(tokens):
    """ Calculates character offsets of tokens """
    start = 0
    offsets = []
    for token in tokens:
        end = start + len(token.form)
        offsets.append([start, end])
        start = end + 1
    return offsets


def encode_conll(conll_data):
    """
    Converts a dependency parse in conll format into json suitable for
    visualizing with brat (brat.nlplab.org).
    """
    rows = [row.split('\t')
            for row in conll_data.splitlines() if row.strip()]
    tokens = [ConllToken(*row) for row in rows]

    text = ' '.join(token.form for token in tokens)

    # tokens
    entities = [["T%s" % token.id, token.postag, [offset]]
                for token, offset in zip(tokens, get_char_offsets(tokens))]

    # dependency arcs
    non_roots = [token for token in tokens if int(token.head) != 0]
    relations = [['R%s' % (i + 1),
                  tok.deprel,
                  [['Arg1', 'T' + tok.head],
                   ['Arg2', 'T' + tok.id]]]
                 for i, tok in enumerate(non_roots)]

    return {
        "text": text,
        "entities": entities,
        "relations": relations
    }
