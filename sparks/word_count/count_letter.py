import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
# fname = "hw0/pg100.txt"
fname = sys.argv[1]
lines = sc.textFile(fname)
phrases = lines.flatMap(lambda l: re.split(r'[^\w]+', l))

# only consider words that begins with letters (not numbers)
words = phrases.filter(lambda word: re.match('^[A-Za-z]', word))

# map to lowercase, key contains the first letter only
letters = words.map(lambda w: (w[0].lower(), 1))

counts = letters.reduceByKey(lambda n1, n2: n1 + n2)
result = sorted(counts.collect(), key=lambda rdd : rdd[0])
with open('hw0.txt', 'w') as file:
	for letter, count in result:
		line = "(%s, %i)"%(letter, count)
		print(line)
		file.write(line + "\n")

sc.stop()