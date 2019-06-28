
#### Motivation
Spark began as toy project to test Apache Mesos (general purpose resource scheduler, earlier than Kubernetes).
* Written in Scala; new things are not developed in Scala. Java is preferred.
* Spark shell
  - command line thing
  - REPL: read, evaluate, print, loop
  - do operation live
  - works for Python and Scala (no Java, which is boilerplate)
  - If only answer is needed, use REPL.
* functional programming is fundamental to Spark.
  - can pass function as parameter.
* Keys do not arrive at reducers in sorted order as does in Hadoop.

```bash
# name is good for YARN, Mesos, not good for local
pyspark -name "my app"
```

* Spark application
* Spark streaming deals with real time (Hadoop stream does not).
* GraphX: doesn't get much use
* SparkML: great treasure stove, falling out of favor lately.
* Log level
  - TRACE, DEBUG, INFO, WARN, ERROR, FATAL, OFF

```
sc.setLogLevel("INFO")
```

#### Resilient Distributed Datasets
* Fundamental unit of data in Spark
* **Predates** Spark SQL and DataFrame/DatasetAPI (CS246 doesn't involve DataFrame)
* Immutable
* Lazy evaluation: triggered by `action`
* Two types of operation:
  - action: returns value, populate all intermediate RDD
  - transform: returns NEW RDD (immutable)
* Pipeline: just map reduce, every RDD goes through transformation independently.
* Can dynamically set type depending on its stored values.
* Text:
  - `.textFile`: delimited by new line
  - `.wholeTextFiles`: read all files in a directory
  - output: `saveAsTextFile`, `saveAsHadoopFile`
* Create RDD from collection: `sc.parallelize(array)`, not used often.
* Common operation:
  - map, reduceByKey
  - first
  - foreach: can use side effect, non-functional functional programming
  - top(n): sort and takes top n
  - sample
  - takeSample
  - distinct
  - union: combine two rdd
  - lookup(key): no collect

```python
print(rdd.toDebugString())
```

#### Pair RDD
* tuple of two elements: key-value pair
* keyBy
* countByKey
* groupByKey: values put in tuples
* sortByKey
* join: inner join, returns only matching
* leftOuterJoin, rightOuterJoin, fullOuterJoin
* lookup(key)
* mapValues
* flatMapValues: break one key-value to multiple pair (e.g. split)

___
#### Quize: TF-IDF
Relevance of a word to a document.

```bash
# upload entire directory to Hadoop
hdfs dfs -put shk

# list
hdfs dfs -ls

pyspark
```

In Spark Shell
```Python
// not good, each row is a rdd
sc.textFile("shk")

// each doc is a rdd
docs = sc.wholeTextFiles("shk").flatMapValues(lambda x: x.split(" "))

// term frequency: need to count word for unique document pairing
tf = docs.map(lambda (k, v): ((k, v), 1)).reduceByKey(lambda v1, v2: v1 + v2)

// inverse document frequency: replace document with 1, need to remove de-duplicate
df= docs.distinct().map(lambda (k, v): (v, 1)).reduceByKey(lambda v1, v2: v1 + v2)

// sanity check: df.lookup("Romeo") returns [1]

// we know there are 38 documents
idf = df.map(lambda (k, v): (k. math.log(38.0 / v)))

// need to align key before joining them, needs to store document somewhere
// duplicate idf for every tf, which is unique term-document
// after join, rdd becomes (t, ((d, v), idf))
tfidf = tf.map(lambda ((d, t), v): (t, (d, v))).join(idf).map(lambda (t, ((d, c), i)): ((t, d), c * i))
```

___
#### Deployment
Spark-submit: productionize, submit homework
* every program needs a spark context (SparkSQL requires spark session).
* Shell creates `sc` automatically.
* Stop context and session when done.
* Scala and Java must be compiled into JAR file and submit.
* `Maven`: a build tool that does dependency management. Edit obtuse XML, not fun.
* Prefer IntelliJ to Eclipse. No one uses Eclipse in real world.

```python
sc = SparkContext()
sc.stop()

spark = SparkSession.builder.getOrCreate()
# can do spark.sparkContext
spark.stop()
```

Parameters:
* --Master: default YARN
* --jars: additional JAR, Scala,Java only
* --pyfiles: Python only
* --drover-java-options: pass params to driver
* --num-executors
* --driver-cores
* --help
* `--local[*], local[n]`

```bash
spark-submit program.py
spark-submit --class WordCount MyJar.jar fileURL
```

Configiration Hierarchy
* program > comand line > properties file > default

Two modes:
* Client mode: driver runs on client. Default.
* Cluster mode: whole bloody thing on cluster.
* spark shell only runs in client mode.
* Distributed, YARN or Mesos

#### Partition & Stage
Operation that preserves partitions: map, flatMap, filter
Repartition: reduce, sort, group
* Stage: seriesof operations that do not re-partition 
* Shuffle demarcates stages.
* A stage cannot start until previous stage completes.
* Can manually repartition.

#### DAG Scheduler
* Narrow: need data in one partition (map, filter).
* Wide operation: gets ashuffle, creates new stage (reduce, sort, ...ByKey).

#### Persistant (built-in)
* 
