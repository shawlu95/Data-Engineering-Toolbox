## Designing Data Intensive Application
* [paperback](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321/ref=sr_1_1?dchild=1&keywords=Designing+Data+Intensive+Application&qid=1609142920&sr=8-1)
* data intensive: quantity of data, complexity, speed

### Anchor
* [Chapter 1: Terminology](#Chapter-1-Foundations-of-Data-Systems)
* [Chapter 2: Model and Language](#Chapter-2-Data-Model)
* [Chapter 3: Storage Engine](#Chapter-3-Storage)
* [Chapter 4: Encoding and Evolution](#Chapter-4-Encoding-and-Evolution)
* [Chapter 5: Replication](#Chapter-5-Replication)
* [Chapter 6: Partition](#Chapter-6-Partition)

___
### Chapter 1 Foundations of Data Systems
* a special purpose application is made from general purpose components
* boundary between messaging queue and database is blurred
  - kafka is a message queue with database-like durability guarantee
  - redis is a key-value store which can be used as message queue
* usually application code's responsibility to keep cache and indexes in sync with database

#### Reliability
* continue providing expected functionality when things go wrong
* *fault* means component goes wrong; *failure* means entire system goes down
* hardware failure
  - RAID configuration for disk
  - diesel power generator
  - dual power supply
  - hot-swappable CPU
  - cloud provider prioritize flexibility and scalability over single machine reliability (commodity hardware)
  - rolling upgrade, removes downtime
* software fault
  - can be dormant for a long time
  - hardware faults are uncorrelated; software faults are correlated
  - to prevent: process isolation; measure, analyze production env
* human error
  - configuration errors by operators were the leading cause of outages
  - design general purpose interface so people don't have to hack around
  - non-production sandbox
  - unit test and whole-system integration test
  - design for quick and easy recovery
  - telemetry

#### Scalability
* define load parameter: hit rate on cache, concurrent user, request per sec, read-write ratio
* twitter does cache compute at write time, and makes read-time quick
* throughput: number of records processed per sec
* latency: a request is waiting to be handled
* response time: delay user observes; a distribution
  - outlier can be caused by TCP retransmission, garbage collect pause etc
  - often use percentile: median, 95th etc (aka tail latency)
  - latency amplification: wait time is determined by the slowest call
  - efficient algo to calculate percentile: forward decay, t-digest, HdrHistogram

#### Maintenance
* operational: metrics monitor system health
* simplicity & abstraction
* evolve: test-driven development, refactoring

## Chapter 2 Data Model
Each layer hides the complexity of lower layer by providing a clean data model
* relational model: dominated 30 years
  - better join support
  - schema on write
* document model: JSON, better locality, no need for join; flexible schema
  - NoSQL: large dataset, high write throughput, flexible model
  - poor handling many-many relationships: multiple read, adds application code complexity
  - schema-on-read
  - need to keep document small for locality performance
  - schema on read
* graph model: for highly connected data; many-to-many relationships
  - SQL introduces recursive common table expression
  - schema on read
* polyglot persistence: relational will continue to be used along side a broad variety of non-relational
* impedance mismatch: need a translation layer between relational DB and object oriented program
* declarative: specify condition and result pattern, leave the DAG to optimizer (SQL, cypher)
* imperative: must specify how data are transformed step by step; **difficult to parallelize** (gremlin)
* Triple store: subject, verbs, object
  - object can be a property or another vertex (no difference)
  - example: Jim likes apple, Jime age 18
  - SPARQL is a language for Triple store + RDF data
  - SPARQL is similar to Cypher (which is modeled after SPARQL)

___
### Chapter 3 Storage
* log-structured engine
  - append-only sequence of records
  - O(1) write speed
* page-oriented engine
* An index is an additional structure that is derived from the primary data
  - slow down write speed

#### Bitcast
* keep a hash mapping key to file offset
* provide fast read: keys must be kept in memory
  - a snapshot of hash map is saved to disk for crash recovery
  - hash map can be recovered by full file scan
* use checksum to discard partially written/corrupted records
* have one writer thread only, multiple reader threads
* mark deleted record with tombstone
* apply compaction periodically to remove old records and tombstone
* con: key space limited to memory size; impossible to scan by key range
```bash
#!/bin/bash
db_set () {
  echo "$1,$2" >> /tmp/txt_db
}
db_get () {
  # return the most recent-added
  grep "^$1," /tmp/txt_db | sed -e "s/^$1,//" | tail -n 1
}
```


#### SSTable, Memtable, LSM Tree
* used in **LevelDB** and **RocksDB**
* sorted string table: key-values are sorted by key
* memtable, SSTable are introduced by Google Bigtable paper
* merging segments is quick: just like merge sort
* sparse index: just keep some of the keys in memory
* maintaining sorted segments
  - write can come in any order
  - write records are saved to memtable (usually a red-black tree/AVL tree)
  - when tree becomes large, write to disk as a new segment
  - when segment is being produced, start a new memtable to accept new write request
  - write request are appended to a log in non-sorted order to allow crash recovery
  - serve read request: look memtable, then starting with newest segment
  - aka *Log-structured Merge Tree (LSM Tree)*
* size-tiered compaction
* level-tiered compaction

#### B-Tree
* most popular data base structure
* also sorted key, provide efficient lookup and range query
* B-trees break the database down into fixed-size blocks or pages (4Kb)
* The number of references to child pages in one page of the B-tree is called the branching factor.
* A four-level tree of 4 KB pages with a branching factor of 500 can store up to 256 TB
* Always balanaced: N key always have depth logN
* B-tree rewrite entire page at a time
* use write-ahead log (append-only) to recover from crash and resolve inconsistency
* a value field either contains a value or pointer to its value
* leaf node may contains pointer to sibling page to avoid returning to parent page

#### Comparison
* LSM Tree: faster for write;
  - lower write amplification than B-Tree
  - better compression, smaller file
  - compaction process interferes with read/write, avg impact small, but high-percentile huge
* B-Tree: faster for read
  - write to log, then to disk
  - each key only has one copy

#### Other Index
* clustered index: rows are stored together with the index
  - primary key of MySQL
* non-clustered index: index contains reference to where rows are stored
* convering index: combination of the two
* concatenated index: concatenate multiple columns together
  - order matters; place big filter first
* full-text search & fuzzy index
* im-memory database: ensure durability by writing change log to disk
  - save time not by keeping data in memory
  - save time by avoid encoding data into a disk-written format
  - Redis and Couchbase provide weak durability by writing to disk asynchronously.

#### Data Warehouse
* separate OLAP from OLTP
  - OLAP: bottleneck disk bandwidth
  - OLTP: bottleneck disk seek time
* OLTP requires high availability and low latency
* analyze run large query without impacting online transaction

### OLAP engine
* Apache Hive, Spark SQL, Cloudera Impala, FB Presto, Apache Tajo, Apache Drill, Google Dremel
* star schema: a fact table at center, linked to multiple dimension table
* snowflake schema: dimension branching out into sub-dimension
* dimension tables are much smaller than fact table
* OLTP are row-oriented
* OLAP are col-oriented: don't store all columns from one row together
  - each column file contains the rows in the *same order*
  - breaking up columns reduces disk read throughput
  - compression technique further reduces throughput
* Cassandra and HBase are row-oriented: still stores all columns of a row together
* use materialized view and aggregation cube to pre-computed aggregate data and boost certain query

___
### Chapter 4 Encoding and Evolution
* old and new data will co-exist:
  - staged rollout/rolling upgrade
  - user may not upgrade app
* forward compatibility: old code need to handle new data
* backward compatibility: new code need to handle old data
* data have two state: in-memory (data structure) vs in-network (byte)
  - encoding: a.k.a marshalling, serialization
  - decoding: a.k.a. parsing, de-serialization, unmarshalling
#### language-built in serde protocol:
- Python pickle, Java Kryo, Ruby Marshall, java.io.Serializable
- not efficient
- not versioned
#### textual format: JSON, XML, CSV
- ambiguous about number encoding
- JSON XML does not support binary string
#### binary format: most compact
- open source lib: Thrift (Facebook), Protocol Buffer (Google)
- require schema definition in Interface Definition Language (IDL)
- schema specify numeric field tag, which works as column alias (no column name ref needed)
- forward compatibility: old code ignore field with unknown tag; but knows how many byte to skip
- backward compatibility: new column must be OPTIONAL
- deleting: only delete OPTIONAL column; never reuse tag
- avro: Hadoop side project
  * no byte indicating field name/tag or data type, totally reliant on schema IDL
  * reader's schema & writer's schema don't have to be the same; just need to be compatible
  * forward compatible: old reader can read new writer
  * backward compatible: new reader, old writer
  * can only add/remove field which has *default* value
  * changing a field-name is backward compatible, but not forward compatible
  * adding a datatype to union type is backward compatible, but not forward compatible
  * having no field tag allows dynamically evolving schema
### Dataflow
* data flow through database:
  - be careful at application level: when old app read new version data, and write back to database, new field might be lost
  - data outlive code: schema evolution provides a uniform facade overtime
* data flow through service:
  - server and client must maintain forward and backward compatibility
  - service-oriented architecture, microservices architecture: decompose application into smaller services
> A key design goal of a service-oriented/microservices architecture is to make the application easier to change and maintain by making services independently deploya‐ ble and evolvable.

  - rest is not a protocol but a design philosophy which builds on HTTP principle
  - API designed according to REST principle is RESTful
* Remote procedure call (RPC): aim to make service call feel like a function call. *fundementally flawed*:
  - unpredictable fail point (network issue)
  - network call may timeout (return with no result)
  - response time varies wildly
  - must encode data to send over network
  - client may be totally different programming language
  - workaround: use *future/promise*
  - it is reasonable to assume that all the servers will be updated first, and all the clients second.
  - only need backward compatibility on requests, and forward compatibility on responses.
* asynchronous message-passing systems
  - data is read with low latency (like RPC)
  - data is temporarily stored in a message brokers
  - one-way: sender doesn't get a reply

___
## Distributed System
* vertical scaling: shared-memeory achitecture
* shared-disk architecture: not interesting
* shared-nothing architecture: aka horizontal scaling
* partitioning: divide a dataset into subsets
* replication: provide fail safe redundancy

### Chapter 5 Replication
Difficulty is how to push changes to all replica
* leader: accept read request and write request
* follower: only accept read
* setting up a follower:
  1. take a snapshot of leader and copy to follower
  2. follower requests all changes happened since snapshot (aka caught up)
* follower fail
  * a change log is kept in follower
  * read the last transaction before fail
  * request from leaders all changes after
* leader failover: a follower becomes new leader
  1. decide leader is down: usually a timeout
  2. elect new leader; appointed by a controller node; most up-to-date follower becomes leaders
  3. client needs to start sending write request to new leader
  * old leader’s unreplicated writes to simply be discarded (**dangerous**)
  * split brain: two leaders accepting write; cannot resolve inconsistency
* synchronous replication: guarantee up-to-date copy on follower, but slow
  - synchronous mode usually only have one synchronous follower (semi-synchronous)
  - one failed node takes down entire system
* complete async: most popular; no durable write guarantee
#### Replication Method
* statement based: sending transaction statement to follower; cannot resolve nondeterministic function/trigger/auto-increment index
* Write ahead log (WAL): leader appends to log and sent the append across network
  - con: describe a low level (byte); no inteoprable across different storage format
* logical (row-based) replication: same idea as log, but use a different log format independent of storage format
  - usually row-granularity
* trigger-based replication: offer flexible solution, delegate code to application layer; greater overhead

#### Problem with
* eventual consistency: when serving read, async replication may lead to stale state. But stale state will eventually be refreshed
* replication lag: between leader write and follower caught up
* read-after-write consistency: user should immediately see his edit
  * when query his own info, read from leader
  * remember user's last update on server; when update is < 1 minute old, read from leader; otherwise read from follower
  * send user timestamp, when serving read request, follower must be caught up with the timestamp
* monotonic read: avoid the situation where user can query a greater lag replica and see older data. Just route the same user to the same replica.
* consistent prefix read: causality should be preserved;
  * problematic for partitioned DB; each partition independent (no global ordering)
  * send causality related writes to same partition

#### Multi-leader
* suitable scenario: multiple datacenters, each center has one each leader; leader acts as follower to other leader
* advantage:
  - lower latency; write can be processed at local data center
  - tolerance of datacenter outage
  - tolerance of network problem
* disadvantage: handling write conflict
  - avoid: all writes on a particular record are routed to same data center
  - conflict-free replicated datatype (CRDT)
  - last write win (LWW): prone to data loss
  - merge value together
  - preserve both versions and let use resolve conflict later
* repair mechanism
  - read repair
  - anti-entropy process: constantly looking for differences in replicas and copy from one another
* quorum consistency
  - successful write need to be acknowledged by w node
  - successful read need to query from r node
  - require r + w > n (number of nodes)
  - this makes sure there's overlap between read node and successful written nodes
  - ideal for cases requiring **high availability and low latency**
* sloppy quorum
  - if the w node data normally live become unreachable, write to any other w node
  - when the expected w nodes become available, copy the writes over (`hinted handoff`)
  - increase write availability
#### Concurrency and Conflict
* cannot rely on timestamp to tell who's first; clock synchronization is an issue
* we can simply say that two operations are concurrent if neither happens before the other
* client must read version number before submitting write request, which tells what state the write is based on
* can only overwrite lower or equal version number value
* version vector: version numbers from all replica

___
### Chapter 6 Partition
synonym
* `shard` in MongoDB, elastic search, SolrCloud
* `region`: HBase
* `tablet`: bigtable
* `vnode` cassandra Riak
* `vBucket`: Couchbase
* goal: query load evenly across nodes
* each node can be leader of some partitions, follower of other partitions

#### Partition Strategy
* partition by key range (prone to hotspot, e.g. key by time)
* partition by hash of key: lose efficient range query; evenly spread
* compromise: compound key, first part identifies partition; second identifies sort order

#### Secondary Index
How to partition a database with secondary index:
* document-based partitioning:
  - local index; partitions are independent
  - keep a list of document ID for each secondary index key
  - query by secondary index without primary index will scan all partitions
  - secondary indexes are stored in the same partition as the primary key and value
* term-based partitioning
  - global index
  - index itself is partitioned
  - range partition supports query range
  - hash partition offers more evenly load

#### Rebalancing
* mode hash N: bad strategy; when N changes, most data will be reassigned partition
* fixed number of partitions:
  - set large enough partitions at the beginning
  - number does not change
  - assignment of partitions change as cluster scale up/down
* dynamic partitioning
  - split partition when reaching configured size (vice versa)
  - *pre-splitting*: configure a set of partitions on an empty database
  - partition number proportional to dataset size
* partition proportional to node
  - have fixed number of partitions per node
  - when new node is added, randomly choose fixed number of partitions to split

#### Service Discovery
How does client know what to ask for
* contact any node, which forwards request to the right node
* have partition-aware load balancer to broker request
* require clients to be fully aware
* massive parallel processing (MPP) engine: break query into multiple stages and partitions 
