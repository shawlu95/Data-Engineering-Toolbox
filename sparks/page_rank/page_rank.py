# bash: shawlu$ bin/spark-submit hw3/q2/q2.py
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

# indexed 1 ~ 100
data_fname = "data/graph-full.txt"
data = (sc
    .textFile(data_fname)
    .map(lambda line : map(int, line.split('\t')))
    .map(lambda edge: (tuple(edge), 1))
    .reduceByKey(lambda x, y: 1)
    .map(lambda point: point[0]))

iteration = 40
n = 1000

# -------------- Page Rank
beta = 0.8

# initialize uniform ranking
r = {i + 1 : 1.0 / n for i in range(n)}

# column must sum to 1, sum (j, i) over j equal to 1
# not that x[0] is column index, x[1] is row index
a = data.map(lambda x: (x[0], 1)) # (col, 1)
b = a.reduceByKey(lambda x, y: x + y) # (col, nonzero count)
degree = {rdd[0] : rdd[1] for rdd in b.collect()} # col -> nonzero count

# key: (r, c), val: (1 / col nonzero count)
m = data.map(lambda edge: ((edge[1], edge[0]), 1.0 / degree[edge[0]]))

for _ in range(iteration):
    m2 = m.map(lambda rdd: (rdd[0][0], rdd[1] * r[rdd[0][1]]))
    m3 = m2.reduceByKey(lambda x, y: x + y)
    r_next = m3.map(lambda x: (x[0], x[1] * beta + (1 - beta) / n))
    r = {x[0] : x[1] for x in r_next.collect()}

ranking = sorted(r_next.collect(), key=lambda rdd : -rdd[1])
print("\nTop 5 (DESC):")
for idx, score in ranking[:5]:
    print(idx, score)

print("\nBottom  (ASC):")
for idx, score in ranking[-5:][::-1]:
    print(idx, score)

# -------------- HITS
L = data
h = {i + 1 : 1.0 for i in range(n)}

for _ in range(iteration):
    # L.T * h
    a_rdd = (L
        .map(lambda rc : (rc[1], 1 * h[rc[0]])) 
        .reduceByKey(lambda x, y : x + y))

    # normalize
    a_max = max(a_rdd.collect(), key=lambda x : x[1])
    a_rdd = a_rdd.map(lambda x : (x[0], x[1] / a_max[1]))
    a = {x[0] : x[1] for x in a_rdd.collect()}

    # h = La
    h_rdd = (L
        .map(lambda rc : (rc[0], 1 * a[rc[1]]))
        .reduceByKey(lambda x, y : x + y))
    
    # normalize
    h_max = max(h_rdd.collect(), key=lambda x : x[1])
    h_rdd = h_rdd.map(lambda x : (x[0], x[1] / h_max[1]))
    h = {x[0] : x[1] for x in h_rdd.collect()}

print("\nTop 5 authority (DESC):")
for idx, score in a_rdd.top(5, key=lambda x: x[1]):
    print(idx, score)
print("\nBottom 5 authority (ASC):")
for idx, score in a_rdd.top(5, key=lambda x: -x[1]):
    print(idx, score)
print("\nTop 5 hubbiness (DESC):")
for idx, score in h_rdd.top(5, key=lambda x: x[1]):
    print(idx, score)
print("\nBottom 5 hubbiness (ASC):")
for idx, score in h_rdd.top(5, key=lambda x: -x[1]):
    print(idx, score)