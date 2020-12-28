## Designing Data Intensive Application
* [paperback]()
* data intensive: quantity of data, complexity, speed

### Anchor
* [Chapter 1: Terminology](#Chapter-1-Foundations-of-Data-Systems)
* [Chapter 2: Model and Language](#Chapter-2-Data-Model)
* [Chapter 3: Storage Engine](#Chapter-3-Storage)
* [Chapter 4: Encoding and Evolution](#Chapter-4-Encoding-and-Evolution)
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
