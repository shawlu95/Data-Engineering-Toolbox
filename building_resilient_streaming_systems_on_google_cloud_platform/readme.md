### Building Resilient Streaming Systems on Google Cloud Platform
This folder contains notes for the Coursera class *Building Resilient Streaming Systems on Google Cloud Platform* ([link](https://www.coursera.org/learn/building-resilient-streaming-systems-gcp/home/welcome)).

* Unbounded data are becoming more and more common as sensors become cheaper.
* Example:
    - traffic on highway (massive, varied, growing);
    - credit card transaction, trading (requires immediate processing);
    - online-games in which users move (Pokemon Go).

#### Challenges
* Ingest massive volume of data: durable, fault tolerant (do not loss request).
    - Cannot tie sender to receiver (error propagates).
    - Use loosely coupled system.
    - Solution: Cloud Pub/Sub ingest (Global message queue).
* Latency is expected.
    - Because of different network path, some may arrive late.
    - `MAX` and `AVG` over a moving window is speculative result. Need to correct.
    - Solution: Beam/Dataflow model processing and imperative analysis.
        - Controls to ensure correctness
        - Ability to flexibly reason about time
* Instant insight.
    - Cannot store, which increases latency.
    - Solution: BigQuery: *SQL query will get carried out on the streaming buffer even before it has been saved to disk in durable storage.*
    - `.apply(BigQueryIO.writeTableRows().to(trafficTable))`
    - **Drawback**: cannot have very high throughput and very low latency (use `BigTable` instead).
> Paradigm: Unified language when querying historic and streaming data.

![alt-text](figs/common_config.png)

___
### Pub/Sub
A global, multi-tenanted, managed, real-time messaging services.
* Publisher publishes to topics.
    - Do not need to know who joined and who left.
* Subscribers receive updates from topics.
    - Do not need to know new publishers to topics.
* At least once delivery guarantee.
    - Dataflow handles de-duplication, order and window.
* Messages are durable for 7 days before receipt.
* Low latency for high performance ~ 100s milliseconds.
* Good at capturing data and distributing data.
* ~ email system: sender and receiver do not have to be online at the same time.
* Simplify interaction: each party only interacts with a single service.
* Automatic scaling to avoid over-provisioning.
* **Fan-in**: one topic -> many subscribers.
* **Fan-out**: multiple publishers -> one topic.
* Subscribers **Pull**: subscribers check if new messages exist.
    - Have delay. End point is a server of device capable of API call.
    - Server respond `error` queue is empty.
    - Respond with `ACK ID`, subscribers must call the acknowledgement method with the ID to confirm receipt (Dataflow handles de-dup).
* Publishers **Push**: register for notifications when there is a new message.
    - No delay. End point must be HTTPS server accepting `webhook`.
    - Server calls HTTPS endpoint. Subscribers respond to calls as ACK.
    - If delivery fails, retry at exponentially interval for 7 days.
* Alternative: `Firebase` for real-time person-to-person communications such as for gaming, chat, and streaming of activities.

 > Pub/Sub is not a database or a data storage service, it's a communication method. It's used for data ingest and streaming of data to a storage destinations such as a data warehouse, cloud storage, or BigQuery.

#### Create Topic and Publish
 * Use `gcloud`, or import `pubsub` from `google.cloud` (Python).
 ```bash
 gcloud pubsub topics create sandiego
 gcloud pubsub topics publish sandiego "hello"
 ```
 * Can add extra attributes, metadata (e.g. timestamp).
 * Can publish a set of messages to a topic in a single request: `with publisher.batch() as batch`.

#### Create Subscription and Pull
* Very similar to publishers API.
```bash
gcloud pubsub subscriptions create --topic sandiego mySub1
gcloud pubsub subscriptions pull --auto-ack mySub1
```

___
### DataFlow
Fully-managed, auto-scaled execution environment for Beam pipelines.

Operations on streaming data:
* Element-wise transform.
* Aggregation.
* Compositing.

Traditional method is to build two pipelines:
1. Low latency, real time streaming layer.
2. Batch pipeline layer.

Solution – Apache Beam: a unified model to process batch and stream.
* Time-based window: use publishing timestamp as event time and place it in right window.
* **event-time-based finite chunks**: not processing time.
* Publishing timestamp is system time, and recorded automatically.
* Different types of window:
    - fixed size window: hour, day, week, month.
    - sliding window: set window duration, and frequency of computation.
    - sessions (how many actions in a single session).
* Example: Traffic Amount Pub/Sub -> Get Messages -> extract data -> BigQuery
* Late data: DataFlow learns the `watermark` of a window:
    - `watermark` is a learnable heuristic on how complete is a window (may be incorrect).
    - `trigger`: defines what to do with late data.
#### Coordinating with Pub/Sub
* Pub/Sub does not preserve order or messages. DataFlow corrects this.
* Pub/Sub may result in duplicates. DataFlow removes duplicates based on Pub/Sub ID.
* In case publishers retry same messages, explicitly passing an ID when publishing. DataFlow will use custom ID for de-duplicates.

___
### BigQuery
Enabling ad-hoc analysis and dashboard.
* Ingestion rate: 100,000 rows/table/second.
* De-duplicate on "best-effort", not guaranteed.
* For continuous analysis, use Dataflow.

___
### Spanner
* Horizontally scalable (add nodes), globally consistent
* Good for: relational database, strong consistency, horizontal scalability, transaction.
* Financial, inventory application. Provisioning for multinational businesses.
* Data replicated across multiple zones. Sharded for high throughput.
* ACID properties as for relational database.

___
### BigTable
For streaming data **analytics** (not transaction) when BigQuery is not enough.
* Milliseconds latency. High throughput.
* Big (> 1TB) semi-structured or structured.
* NoSQL: no required transaction or strong relational semantics.
* Good for: time series, machine learning.
* **Not cluster-free**: but clusters only contain **pointer** to data.
    * Also separates computation from storage.
    * Data remain in colossus (GCS).
* Use web interface or `gcloud` CLI to create cluster of BigTable nodes.
    * Cannot change Cluster ID, zone or storage type after cluster creation.
    * Can use Python or `DataFlow`(preferred) to interact with BigTable.

#### BigTable Ingesting
1. Create table.
2. Convert object to Mutation inside a ParDo.
3. Write Mutations to BigTable
4. Read from BigTable: HBase API, HBase CLI, BigQuery

#### Design
* A table only has one key column, called `row key`.
* No other column can be indexed.
* Rows are stored in `ACS` order of `row key`.
* Group columns into `column families`.
* Wide table design: each column value exists for every row (dense).
* Narrow (sparse) table design: many columns do not have many data
    * e.g. rating matrix
    * follower: row key must encode both follower and followed ID
* Can query a prefix of the `row key`, better than query entire key.
    * What is the most common query to support -> become row key prefix.
    * Rows that are likely pulled in a single query should be stored near each other.
    * Only need latest few records? Add timestamp to key, in `reversed` format so latest are stored at top.
* Block Read & Write: better to be continuous in memory.
* Evenly distributed for read & write: load balancing.
    * Avoid starting row key as domain (certain domains are extremely active).
    * Avoid sequential ID (newer customers are more active).
    * Avoid static identifier (e.g. CPU usage) that gets repeatedly updated.

#### Performance
* Learn access pattern:
    - how many nodes it needs to keep running;
    - where the tablets need to be;
    - how the tablets need to be split up;
    - which machines need to process what data.
* Rebalances data by moving data **pointers** across nodes.
    - Redistribute reads.
    - Distribute storage (Cloud Storage).
* Cluster performance consistent, predictable.
    - e.g. 220 MB/s scan for SSD, 180 MB/s for HHD (SSD faster).
* Design schema to minimize data skew.
* Let BigTable learn before making changes to break bottleneck.
* Test BigTable with > 300 GB.
* Performance increases linearly with number of nodes.
* Clients & BigTable are in the same zone.
* Note count directly determines throughput.
___
### Lab
1. Publish Streaming Data into PubSub ([link](lab_1.md)).
2. Streaming Data Pipelines ([link](lab_2.md)).
3. Streaming Analytics and Dashboards ([link](lab_3.md)).
4. Streaming data into Bigtable ([link](lab_4.md)).

### Reference
* Data Science on the Google Cloud Platform
