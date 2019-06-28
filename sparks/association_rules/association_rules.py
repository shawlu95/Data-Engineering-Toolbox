import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

# use case
# ../../bin/spark-submit association_rules.py browsing.txt 

# fname = "hw1/q2/data/browsing.txt"
fname = sys.argv[1]
sessions = (sc
    .textFile(fname)
    # .sample(False, 0.1, 0) # uncomment this line to load a small sample only
    .map(lambda x : x.split()))

# --------------------------------------------------------------------------- 
# PART D

# first pass
freq_items_support = (sessions
    .flatMap(lambda x : [(y, 1) for y in x])
    .reduceByKey(lambda n1, n2 : n1 + n2)
    .filter(lambda x : x[1] >= 100)
    .sortByKey()
    )

freq_items = {x[0] : x[1] for x in freq_items_support.collect()}

def build_pairs(basket):
    pairs = []
    if len(basket) < 2: return pairs
    for i, item_1 in enumerate(basket[:-1]):
        for item_2 in basket[i + 1:]:
            if all(item in freq_items for item in [item_1, item_2]):
                key = (item_1, item_2) if item_1 < item_2 else (item_2, item_1)
                val = [freq_items[item] for item in key] + [1]
                pairs.append((key, tuple(val)))
    return pairs

# second pass
pair_support = (sessions
    .flatMap(build_pairs)
    .reduceByKey(lambda x, y: (x[0], x[1], x[2] + y[2])))

def pair_conf(rdd):
    # confidence is assymetrical, the denominator decides direction
    # for each pair, compute two confidence scores: A -> B, A <- B
    (i1, i2), (s1, s2, s12) = rdd
    return [((i1, i2), s12 / s1), 
            ((i2, i1), s12 / s2)]

# warning: use all pairs to find rules, not just frequent pairs
conf_pair = pair_support.flatMap(pair_conf)
sorted_pair = sorted(conf_pair.collect(), key=lambda rdd : (-rdd[1], rdd[0][0]))
with open('hw1_q2d.txt', 'w') as file:
    for rel in sorted_pair[:5]:
        (a, b), conf = rel
        line = "Conf(%s -> %s) = %.10f"%(a, b, conf)
        print(line)
        file.write(line + "\n")

# --------------------------------------------------------------------------- 
# PART E

freq_pair_support = pair_support.filter(lambda x : x[1][2] >= 100)
freq_pairs = {x[0] : x[1][2] for x in freq_pair_support.collect()}

def build_triples(basket):
    triples = []
    if len(basket) < 3: return triples
    for i, item_1 in enumerate(basket[:-2]):
        for j in range(i + 1, len(basket) - 1):
            item_2 = basket[j]
            for item_3 in basket[j + 1:]:
                # sort triples in alphabetic order once, so that
                # all 2-item permutation will be in alphabetic order
                triple = sorted([item_1, item_2, item_3])

                if all(item in freq_items for item in triple):
                    # exclude index 2, 1, 0 one at a time to find three subset pairs
                    pairs = [tuple(triple[:idx] + triple[idx + 1:]) for idx in range(len(triple) - 1, -1, -1)]
                    
                    # construct triple only if all permutation of 2-item pairs are frequent
                    if all(pair in freq_pairs for pair in pairs):
                            val = [freq_pairs[pair] for pair in pairs] + [1]
                            triples.append((tuple(triple), tuple(val)))
    return triples

def triple_conf(rdd):
    # key is ordered such that A & B -> C
    # note that A & B are already sorted since i1 < i2 < i3
    (i1, i2, i3), (s12, s13, s23, s123) = rdd
    return [((i1, i2, i3), s123 / s12), 
            ((i1, i3, i2), s123 / s13), 
            ((i2, i3, i1), s123 / s23)]

# third pass
# warning: use all candidate triples to find rules, not just frequent triples
conf_triple = (sessions
    .flatMap(build_triples)
    .reduceByKey(lambda x, y: (x[0], x[1], x[2], x[3] + y[3]))
    .flatMap(triple_conf))
sorted_triple = sorted(conf_triple.collect(), key=lambda rdd : (-rdd[1], rdd[0][0], rdd[0][1]))
with open('hw1_q2e.txt', 'w') as file:
    for rel in sorted_triple[:5]:
        (a, b, c), conf = rel
        line = "Conf(%s, %s -> %s) = %.10f"%(a, b, c, conf)
        print(line)
        file.write(line + "\n")

sc.stop()