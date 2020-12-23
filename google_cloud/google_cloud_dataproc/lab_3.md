### Submit Dataproc jobs for unstructured data

* Setup a Dataproc cluster and SSH into master node.
* Enable Firewall rule to enable port 9870, 8088.
    * Specify target tags to be consistent with master node.
    * Source IP range: `<your-IP>/32` ([IP](http://ip4.me/)).
* Copy Data to Hadoop. Verify in port 9870 that file exists.

```bash
hadoop fs -mkdir /sampledata # create dir
hadoop fs -copyFromLocal road-not-taken.txt /sampledata/.
hadoop fs -copyFromLocal sherlock-holmes.txt /sampledata/.
hadoop fs -ls /sampledata # make sure file exists
```

* Access Hadoop in PySpark and debug interactively.
* Build python script.

```python
from pyspark.sql import SparkSession
from operator import add
import re

print("Okay Google.")

spark = SparkSession\
        .builder\
        .appName("CountUniqueWords")\
        .getOrCreate()

lines = spark.read.text("/sampledata/road-not-taken.txt").rdd.map(lambda x: x[0])
counts = lines.flatMap(lambda x: x.split(' ')) \
                  .filter(lambda x: re.sub('[^a-zA-Z]+', '', x)) \
                  .filter(lambda x: len(x)>1 ) \
                  .map(lambda x: x.upper()) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add) \
                  .sortByKey()
output = counts.collect()
for (word, count) in output:
  print("%s = %i" % (word, count))

spark.stop()
```

* Run the job in Terminal (not tracked by Dataproc Jobs page):

```bash
spark-submit wordcount.py
```
