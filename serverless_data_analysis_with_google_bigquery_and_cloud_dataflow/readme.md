### Serverless Data Analysis with Google BigQuery and Cloud Dataflow
This folder contains notes for the Coursera class *Serverless Data Analysis with Google BigQuery and Cloud Dataflow* ([link](https://www.coursera.org/learn/serverless-data-analysis-bigquery-cloud-dataflow-gcp/home/welcome))

#### Beyond MapReduce
Disadvantage of MapReduce: sharding data into mappers. Reducers aggregates shards of results. Mixing storage and compute: "The amount of machines that you need to do your compute is going to drive how you're going to split your data."

Second generation: Dremel and Pub/Sub that auto-scale.
* Dremel is internal BigQuery tool (same engineering team).
* Have data stored in Cloud Storage in **denormalized** form.

![alt-text](figs/workflow.png)

#### Normalizing vs. Denormalizing
* **Normalize**: Normalizing the data means turning it into a relational system. This stores the data efficiently and makes query processing a clear and direct task.
* **De-normalize**: Denormalizing is the strategy of accepting repeated fields in the data to gain processing performance. Data must be normalized before it can be denormalized.
    - further increases orderliness.
    - no longer relational, boosting efficiency, in parallel in columnar processing.
    - Takes more storage space.
* Nested fields combine the two (no example given).

___
### BigQuery
#### Advantage of BigQuery
* Interactive analysis at petabyte-scale for business intelligence (near-real time, for immediate, transaction-level response, use Cloud SQL/Spanner)
* No-ops: pay for amount of data scanned.
* Cluster-less: easy to collaborate, share, mashing up different datasets.

#### Essential Concepts
* Relational databases are row-oriented storage and support transaction updates.
* BigQuery is **columnar**: each column is stored in a separated, compressed file replicated +3 times.
* No indices, partitions or keys is required (partitions can be used to reduce cost).
* To save cost, limit the column to scan.
* Table name format: `<project>.<dataset>.<table>`

___
#### Advanced Features
##### Array/Struct
To correlate columns during aggregation.
* First bind columns using `ARRAY_AGG`.
* Unpack columns using `ARRAY(SELECT AS STRUCT ...)`.

```SQL
WITH TitlesAndScores AS (
    SELECT
        ARRAY_AGG(STRUCT(title, score)) AS titles,
        EXTRACT(DATE FROM time_ts) AS date
    FROM `bigquery-public-data.hacker_news.stories`
    WHERE score IS NOT NULL AND title IS NOT NULL
    GROUP BY date
)
SELECT date,
    ARRAY(SELECT AS STRUCT title, score FROM
          UNNEST(titles) ORDER BY score DESC LIMIT 2)
AS top_articles
FROM TitlesAndScores;
```

**User-defined Function**(UDF):
* Standard SQL UDFs are scalar; legacy are tabular.
* UDFs are temporary, and valid for current session only.
* Return data <= 5MB
* Can run 6 concurrent JavaScript UDF per project.

```sql
CREATE TEMPORARY FUNCTION
multiply(x FLOAT64, y FLOAT64)
RETURNS FLOAT64
LANGUAGE js AS
"""
return x * y;
"""
```

##### Wildcard Tables
* Richer prefix, faster efficiency!
* Example: `bigquery-public-data.noaa_gsod.gsod*`
* Must be enclosed in backtick

##### Partitioning
* One table may contain a partition column.
* Time-partitioned table: cost-effective way to manage data.
* Similar to sharding: a time partition is analogous to a shard.


###### Other Shared Features
* Join
* Windows
* Regular expression

___
#### Performance and Pricing
##### Optimizing Queries
* Input and output in GB.
* Shuffle: how many bytes to pass to next stage.
* Materialization: how many bytes to write.
* GPU work: UDFs.
* Check `explanation plan` before running query.
* Monitor in `StackDriver`.

##### General Guidelines
* Minimize columns to be processed. Avoid `SELECT *`.
* Filter `WHERE` as early as possible to reduce data passed between stages.
* Avoid self join (squaring number of rows).
* Do big join first to reduce rows.
* `GROUP BY`: How many rows are grouped per key? Lower cardinality, higher speed.
* Built-in function > custom SQL function > JS CDFs.
* Use `APPROX_COUNT_DISTINCT` instead of `EXACT COUNT(DISTINCT)`.
* Order in the end, on smallest amount of data.

___
### Dataflow
* An execution framework: **Apache Beam**.
* **Pipeline** a directed graph of steps (cann branch, merge, if-else logic).
* Each step is executed on the cloud by a runner, elasticallt scaled.
* Can code operation in batch data (window optional) and stream data (window required). Same code that process streaming and batch data.
* Input and output are `PCollection` (parallel collection).
    - Supports parallel processing.
    - Not an in-memory collection; can be unbounded.
* Every transformation step accepts a name variable, to be visualized in monitoring console.
    - Better unique.
    - Two overloaded operator: `|`, `>>`.

#### Ingest Data
* Source: Pub/Sub, Cloud Storage, BigQuery.
```java
PCollection<string> lines = p.apply(TextIO.Read.from("gs://.../input-*.csv.gz"))
PCollection<string> lines = p.apply(PubsubIO.Read.from("input_topic"))
PCollection<TableRow> rows = p.apply(BigQueryIO.Read.from("SELECT ...;"))
```

* Sink: Pub/Sub, Cloud Storage, BigQuery.
```java
lines.apply(TextIO.Write.to("/data/output").withSuffix(".txt"))
lines.apply(TextIO.Write.to("/data/output").withSuffix(".txt").withoutSharding()) // no sharding for small task
```

* Execute task on cloud (python).
```bash
python ./task.py \
    --project=$PROJECT \
    --job_name=myjob \
    --staging_location=gs://$BUCKET/staging/ \
    --temp_location=gs://$BUCKET/staging/ \
    --runner=DataFlowRunner
```

#### Map = ParDo
* Each compute node processes data local to it.
* Pardo acts on **one** item at a time.
    - multiple instances of class on many machines.
    - Should not maintain any state (e.g. average across all data points).
* Useful for:
    - Filtering;
    - Converting variable type;
    - Extracting parts from input (fields from TableRow);
    - calculating input from different parts of input (e.g. L2 norm).
* Example map task (can replace lambda with a generator):
```python
'WordLength' >> beam.Map(lambda word: (word, len(word)))
```

#### Reduce = GroupBy & Combine
* Group by key is equivalent to `reduceByKey`
* Combine by key is more efficient than group by key
    - balances workload across key. A key can be split into multiple workers.
* Can also group by time.

```python
# Group By
cityAndZipcodes = p | beam.Map(lambda fields : (fields[0], fields[3]))
grouped = cityAndZipcodes | beam.GroupByKey()

# Combine
totalAmount = salesAmounts | Combine.globally(sum) # each item contains a float
totalSalesPerPerson = salesRecords | salesRecords.perKey(sum) # each item is key-val pair
```

#### Multiple Sources of PCollections
* Take the smaller source, and convert into a view.
* Pass in view as a side input.
* Retrieve side input from the processing function.

#### Dataflow Template
The templates help separate the development activities and the developers from the execution activities and the users. The user environment no longer has dependencies back to the development environment.

___
### Dataprep
Dataprep is an interactive graphical system for preparing structured or unstructured data for use in analytics such as BigQuery, visualization like, Data Studio and to train machine learning models.
* Tools for data cleanup, structuring, and transformation.

___
### Labs
1. Build a BigQuery Query ([Note](lab_1.md)).
2. Loading and Exporting Data ([Note](lab_2.md)).
3. Advanced SQL Queries ([Note](lab_3.md)).
4. A Simple Dataflow Pipeline ([Note](lab_4.md)).
5. MapReduce in Dataflow ([Note](lab_5.md)).
6. Side Inputs ([Note](lab_6.md)).

### Resources
* Training repository ([link](https://github.com/GoogleCloudPlatform/training-data-analyst))
* BigQuery documentation ([link](https://cloud.google.com/bigquery/docs/)).
* Tutorials ([link](https://cloud.google.com/bigquery/docs/tutorials))
* Pricing ([link](https://cloud.google.com/bigquery/pricing))
* Client libraries ([link](https://cloud.google.com/bigquery/client-libraries))
* Cloud Dataflow ([link](http://cloud.google.com/dataflow/))
* Dataprep ([link](https://cloud.google.com/dataprep/))
* Training ([link](https://cloud.google.com/solutions/processing-logs-at-scale-using-dataflow))
