
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

```python
print(rdd.toDebugString())
```
