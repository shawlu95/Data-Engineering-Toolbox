import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

def build_pairs(line):
    # Because the graph is undirected, it does not matter which ID comes first.
    # Sort ID so that the reverse order is treated as the same edge.
    # No need to transform to integer, though strings are sorted differently than numbers.
    user, friends = line[0], sorted(line[1].split(","))

    # Any pair of users from 'friends' has 'user' as their common friend
    valid_pairs = [((friends[i], j), 1) 
                        for i in range(len(friends) - 1) 
                        for j in friends[i + 1:]]
                        
    # 'user' is already freind with his friends, so it does not matter how many common friends
    # they share, they should not be recommended to each other
    invalid_pairs = [((user, friend), -float("inf")) if user < friend 
                        else ((friend, user), -float("inf")) 
                        for friend in friends]
    return valid_pairs + invalid_pairs

# since two users share one common friend
# this common friend sould be counted for each of the two users
def double_count(rdd):
    (user_1, user_2), count = rdd
    return [(user_1, [(user_2, count)]),
            (user_2, [(user_1, count)])]

def sort_count(rdd):
    user, candidates = rdd
    # sort by common friends, break tie by user_id
    sorted_candidates = sorted(candidates, key=lambda x : (-x[1], int(x[0])))
    return (user, [candidate[0] for candidate in sorted_candidates])

def truncate_10(rdd):
    user, sorted_candidates = rdd
    if len(sorted_candidates) > 10:
        sorted_candidates = sorted_candidates[:10]
    return (user, sorted_candidates)

# fname = "hw1/q1/data/soc-LiveJournal1Adj.txt"
fname = sys.argv[1]
recommendations = (sc.textFile(fname)
                    # .sample(False, 0.1, 0) # uncomment this line to load a small sample only
                    .map(lambda line : line.split('\t'))
                    .flatMap(build_pairs)
                    .reduceByKey(lambda n1, n2: (n1 + n2))
                    .filter(lambda x : x[1] > 0) # eliminate pairs which are already friends
                    .flatMap(double_count)
                    .reduceByKey(lambda l1, l2: l1 + l2) # group for each user: (user, [(user2, n2), (user3, n3) ...])
                    .map(sort_count)
                    .map(truncate_10))

hit_list = [924, 8941, 8942, 9019, 9020, 9021, 9022, 9990, 9992, 9993]
result = recommendations.filter(lambda rec : int(rec[0]) in hit_list).collect()
result.sort(key=lambda x : int(x[0]))

with open('hw1_q1.txt', 'w') as file:
    for line in result:
        user, rec = line
        line = "%s\t%s"%(line[0], ",".join(line[1]))
        print(line)
        file.write(line + "\n")

sc.stop()