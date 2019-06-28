import re
import sys
from pyspark import SparkConf, SparkContext

# bin/spark-submit hw1/q1/q1_code.py hw1/q1/data/soc-LiveJournal1Adj.txt

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

def get_bad_keys(line):
    user, friends = line[0], sorted(line[1].split(","))
    bad_keys = [(user, friend) if user < friend else (friend, user) for friend in friends]
    return list(bad_keys)

# Any pair of users from 'friends' has 'user' as their common friend
def build_pairs(line):
    user, friends = line[0], sorted(line[1].split(","))
    positive_keys = [(friends[i], j) for i in range(len(friends)) for j in friends[i + 1:]]
    # positive_keys = set([(min(x),max(x)) for x in itertools.permutations(friends, 2)])
    positive_pairs = map(lambda key : (key, 1), positive_keys)
    return list(positive_pairs)

def top_10(user):
    candidates = user[1]
    sorted_candidates = list(sorted(candidates, key=lambda pair : (-pair[1], int(pair[0]))))
    top_10 = sorted_candidates[:min(10, len(candidates))]
    return (user[0], [rec for (rec, count) in top_10])

def build_pairs(line):
    # Because the graph is undirected, it does not matter which ID comes first.
    # Sort ID so that the reverse order is treated as the same edge.
    # No need to transform to integer, though strings are sorted differently than numbers.
    user, friends = line[0], sorted(line[1].split(","))

    # Any pair of users from 'friends' has 'user' as their common friend
    positive_keys = [(friends[i], j) for i in range(len(friends) - 1) for j in friends[i + 1:]]
    positive_pairs = map(lambda key : (key, 1), positive_keys)
    
    # 'user' is already freind with his friends, so it does not matter how many common friends
    # they share, they should not be recommended to each other
    negative_keys = [(user, friend) if user < friend else (friend, user) for friend in friends]
    negative_pairs = map(lambda key : (key, -2**32), negative_keys)
    return list(positive_pairs) + list(negative_pairs)

# doc = sc.textFile("hw1/q1/data/soc-LiveJournal1Adj.txt").sample(False, 0.1, 0)
doc = sc.textFile(sys.argv[1]).sample(False, 0.1, 0)
lines = doc.map(lambda line : line.split('\t'))

# bad_keys = lines.flatMap(get_bad_keys).collect()
# pairs = lines.flatMap(build_pairs)
# filtered_pairs = pairs.filter(lambda pair: pair[0] not in bad_keys)
# count = filtered_pairs.reduceByKey(lambda n1, n2: (n1 + n2))

pairs = lines.flatMap(build_pairs)

count = pairs.reduceByKey(lambda n1, n2: (n1 + n2)).filter(lambda x : x[1] > 0)

# map ((user1, user2), n) to (user1, (user2, n)), (user2, (user1, n))
two_way_count = count.flatMap(lambda x : ((x[0][0], (x[0][1], x[1])), (x[0][1], (x[0][0], x[1]))))
# users = count.flatMap(lambda (pair, count) : [(pair[0], (pair[1], count), (pair[1], (pair[0], count)))])

# group for each user: (user, [(user2, n2), (user3, n3) ...])
count_by_user = two_way_count.groupByKey()

# for each user, sort non-friend users by common friends
recommendations = count_by_user.map(top_10)

# sanity check
# recommendations.filter(lambda rec : rec[0] == "11").collect()

check = [str(user_id) for user_id in [924, 8941, 8942, 9019, 9020, 9021, 9022, 9990, 9992, 9993]]
result = recommendations.filter(lambda rec : rec[0] in check).collect()
result.sort(key=lambda x : int(x[0]))

with open('hw1_q1.txt', 'w') as file:
    for line in result:
        line = "%s\t%s\n"%(line[0], ",".join(line[1]))
        print(line, end="")
        file.write(line)

sc.stop()