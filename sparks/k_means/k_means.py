# bash: shawlu$ bin/spark-submit hw2/q2/q2.py
from __future__ import print_function
from pyspark import SparkConf, SparkContext
import matplotlib.pyplot as plt

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

data_fname = "data/data.txt"
c1_fname = "data/c1.txt"
c2_fname = "data/c2.txt"

data = (sc
    .textFile(data_fname)
    # .sample(False, 0.1, 0) # uncomment this line to load a small sample only
    .map(lambda line : list(map(float, line.split(' ')))))

c1, c2 = [(sc
    .textFile(fname)
    .map(lambda line : list(map(float, line.split(' '))))
    .collect()) for fname in [c1_fname, c2_fname]]

def euc_dist(x, y):
    return sum([(i - j) ** 2 for i, j in zip(x, y)])

def man_dist(x, y):
    return sum([abs(i - j) for i, j in zip(x, y)])

def min_idx(vals):
    i = j = 0
    for j in range(len(vals)):
        if vals[j] < vals[i]:
            i = j
    assert(vals[i] == min(vals))
    return i

def compute_centroid(l):
    """
    l: list of data points assgined to a centroid
    """
    s, n = l[0], len(l)
    for p in l[1:]: 
        s = [i + j for i, j in zip(s, p)]
    return [i / n for i in s]

setup = {"c1_euc" : (euc_dist, c1), 
        "c2_euc" : (euc_dist, c2), 
        "c1_man" : (man_dist, c1), 
        "c2_man" : (man_dist, c2)}

for title, (dist, c) in setup.items():
    cost_hist = []
    for i in range(21):
        # step 1: map each data point to (point, [distance from all cnetroids])
        # step 2: map to (point, idx_centroid, cost)
        a = (data
            .map(lambda x: (x, [dist(x, y) for y in c]))
            .map(lambda x : (x[0], min_idx(x[1]), min(x[1]))))

        # step 3: compute cost
        cost_hist.append(sum(x[2] for x in a.collect()))

        # step 4: update centroid, (idx_centroid, [point])
        c = (a
            .map(lambda x : (x[1], [x[0]]))
            .reduceByKey(lambda x, y : x + y)
            .map(lambda x : compute_centroid(x[1]))
            ).collect()

        print("%s iteration %i, loss %.2f"%(title, i + 1, cost_hist[-1]), end="\r")

    plt.plot(cost_hist)
    plt.savefig("output/%s.png"%title)
    plt.close()

    # report improvement after 10 iterations, take the 11th index
    print("Improve (%s) %.2f%%                                       "
        %(title, 100 * (cost_hist[0] - cost_hist[10]) / cost_hist[0]))
