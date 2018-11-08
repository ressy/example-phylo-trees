#!/usr/bin/env python

"""
Quick and simple sequence cluster generator.

drift() will randomly change (insert/delete/subsitute) individual bases in a
sequence with a given probability.  By copying and then drift()ing sets of
sequences we can make clusters of more or less similar sequences.
"""

import sys
from random import choice, random
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna

BASES = ["A", "C", "T", "G"]

def random_seq(length=100):
    s = [choice(BASES) for i in range(length)]
    s = ''.join(s)
    return(s)

def drift(seq, prob=0.1):
    seq = list(seq)
    for i in range(len(seq)):
        if random() < prob:
            new = choice(BASES + ['', '-'])
            if new == "-":
                new = choice(BASES)
            seq[i] = new
    seq = ''.join(seq)
    return(seq)

def create_clusters():
    # First, one random seq as three copies.
    seq = random_seq()
    seqs = [seq]*3
    # Change a bit.
    seqs = [drift(s, 0.3) for s in seqs]
    # These will be copies, to start.
    children = seqs + seqs
    children = [drift(s) for s in children]
    # Write the whole set.  Give sequence IDs that show the grouping.
    combo = seqs + children
    combo = [Seq(''.join(s), generic_dna) for s in combo]
    prefix = ["A", "B", "C"]
    suffix = ["a", "b", "c"]
    labels = ["%s_%s" % (prefix[i//3], suffix[i%3]) for i in range(9)]
    recs = [SeqRecord(combo[i], id=labels[i], description='') for i in range(len(combo))]
    SeqIO.write(recs, sys.stdout, "fasta")

if __name__ == '__main__':
    create_clusters()
