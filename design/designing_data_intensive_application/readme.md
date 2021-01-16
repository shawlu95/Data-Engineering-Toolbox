algorithms## Designing Data Intensive Application
* [paperback](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321/ref=sr_1_1?dchild=1&keywords=Designing+Data+Intensive+Application&qid=1609142920&sr=8-1)
* data intensive: quantity of data, complexity, speed

### Anchor
* [Chapter 1: Terminology](#Chapter-1-Foundations-of-Data-Systems)
* [Chapter 2: Model and Language](#Chapter-2-Data-Model)
* [Chapter 3: Storage Engine](#Chapter-3-Storage)
* [Chapter 4: Encoding and Evolution](#Chapter-4-Encoding-and-Evolution)
* [Chapter 5: Replication](#Chapter-5-Replication)
* [Chapter 6: Partition](#Chapter-6-Partition)
* [Chapter 7: Transaction](#Chapter-7-Transaction)
* [Chapter 8: Distributed Problem](#Chapter-8-Distributed-Problem)
* [Chapter 9: Consistency and Consensus](#Chapter-9-Consistency-and-Consensus)
* [Chapter 10: Batch Processing](#Chapter-10-Batch Processing)
* [Chapter 12: Stream Processing](#Chapter-12-Stream-Processing)

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

___
## Chapter 7 Transaction
Transactions are an abstraction layer that allows an application to pretend that cer‐ tain concurrency problems and certain kinds of hardware and software faults don’t exist.

### Guarantee of transaction
* Atomicity: no intermediate state
* Consistency: belong to the application layer, not the DB server
* Isolation/serialization: concurrent transactions behave as if serial; but performance suffers
* Durability: data survive hardware failure & database crash

#### Multi-object transaction is still needed
* foreign key references other table
* denormalized document stores, need to have denormalized copies updated together
* secondary index needs updated

### Weak Isolation
Concurrency issue happens when
* one transaction treads data concurrently modified by another transaction
* two transactions modify the same data

#### Read Committed
* no dirty read: only read committed data
  - read-lock
* no dirty write: when writing data, only overwrite committed data
  - use row-level lock
  - Only one transaction can hold the lock for any given object
* in practice, have read write lock is inefficient. server keeps both new and old value, and start returning new value only after write lock is released
* read skew: read several records over a span of time, some records are updated in between
  - backup a snapshot of database will results in partially old and partially new data
  - large analytical query scanning big data will observe parts written at different points in time
* snapshot isolation: each transaction reads from a consistent snapshot of the database
  - use write lock to prevent dirty write
  - reader doesn't need lock
  - readers never block writers, and writers never block readers
  - db must keep **multiple version of uncommitted writes**: multi-version concurrency control (MVCC)
* use transaction ID to implement consistent snapshot. A read with transaction ID X can not observe:
  * all writes of in-progress transactions
  * writes of aborted transactions
  * **writes made by transaction of higher ID**
* how index works with snapshot isolation p 241

#### Prevent Lost Update in Concurrent Write
* many database server automatically group read-write cycle in transaction
* have application code to explicitly lock
* execute in parallel; detect lost update and abort transaction, then retry read-write cycle again
* compare and set: only set if value is same as old (read) value

### Write Skew
Dirty writes and lost updates are two of the most common race conditions. Here are more subtle onesL
* write skew generalizes dirty write: read the same objects, but modify different objects
  - concurrently booking the same room, after reading it's availalble
  - multiplayer game two players move to the same position
* best option: use serializable isolation level
* second best: explicitly lock the dependent rows

#### Phantom
When phantom is created:
1. check some condition
2. do some action depending on the condition
3. changes results that alters the condition in step 1

> This effect, where a write in one transaction changes the result of a search query in another transaction, is called a phantom . Snapshot isolation avoids phantoms in read-only queries, but in read-write transactions like the examples we discussed, phantoms can lead to particularly tricky cases of write skew.

* there is no object to which we can attach the locks

### Serializability - Strongest Isolation Level
* pessimistic to the extreme
* Methods of implementation
  * literally serial execution;
    - only allows stored procedure submitted in a single HTTP
    - no interactive communication in the transaction
    - write-heavy transaction can partition dataset so that each transaction only needs to interact with one partition
  * two-phase locking
  * Optimistic concurrency control techniques such as serializable snapshot isolation

### Two-Phase Locking

> If transaction A has read an object and transaction B wants to write to that object, B must wait until A commits or aborts before it can continue. (This ensures that B can’t change the object unexpectedly behind A’s back.)

> If transaction A has written an object and transaction B wants to read that object, B must wait until A commits or aborts before it can continue. (Reading an old version of the object, like in Figure 7-1, is not acceptable under 2PL.)

* **pessimistic** concurrency control mechanism
* not the same as two-phase commit (2PC)
* writers block not just writers, but readers too
  - snapshot isolation: readers never block writers, and writers never block readers
* protect against lost update, write skew
* a lock on each object in database
* lock can be **shared** or **exclusive** mode
  - to read an object, must acquire shared lock (many process can share the shared lock).
  - cannot read the object if an exclusive lock has been issued
  - to write to an object, must acquire exclusive lock, only one lock is issued at a time
  - a transaction must hold the relevant locks until end of transaction
* deadlock: two transaction waiting for each other to release lock
  - deadlocks can happen with the lock-based read committed isolation level
  - more frequent in 2PL
* performance is weaker than weak isolation
* unstable latency; slow at high latency percentile
* predicate lock: belongs to all objects that match some search condition
  - even to objects that do not yet exist in the database, but which might be added in the future (phantoms)
  - prevents all write skew and race conditions!
* index range lock:
  - predicate lock is inefficient; index range lock is better alternative
  - not as precise as predicate locks would be

### Serializable Snapshot Isolation Algorithm
* provides full serializability, but has only a small performance penalty
* optimistic concurrency control:
  - allow transactions to happen until something went wrong
  - retry aborted transaction
* based on snapshot isolation (prerequisite)
  - an algorithm for detecting serialization conflicts among writes and determining which transactions to abort.
* performs better when contention rate is low
* what to abort:
  - transaction based on outdated premise
  - track when a transaction ignores another transaction’s writes due to MVCC visibility rules
  - notify transaction is the data have been recently read by other transaction (but not blocking)
* latency much more predictable and less variable.
* read-only queries can run on a consistent snapshot without requiring any locks
* requires that read-write transactions be fairly short

___
## Chapter 8 Distributed Problem
* What can go wrong in distributed system: network, clock
* high performance computing (HPC) is easier working or failing, no partial fail
* distributed system can have partial fail, and are non-deterministic
* robust systems must be built on top of less reliable components (there's a limit on how much things can go wrong)

#### Unreliable Network
* only option is for sender to receive a reply. If no reply, cannot tell what went wrong
* unbounded delay: there's no upper limit
  - set an empirical value. too short can cause cascading failure
  - measure response time variability (jitter)
* congestion and queueing
  - if old data is worthless (video conference), use UDP instead of TCP
* comparing to telephone circuit
  - circuit has bounded delay, by reserving fixed amount of bandwith
  - network has unbounded delay because it's designed to handle busty traffic
  - more efficient busty traffic handling comes at cost of unbounded delay
  - reserving fixed bandwidth resulting in lower utilization of cable

#### Unreliable Clock
* clock hardware on computer: a quartz crystal oscillator; can drift; not reliable
* time-of-day clock/wall-time clock: sync with NTP, may jump forward or backward in time
* monotonic clock: suitable for measuring duration; absolute value is meaningless. NTP adjusts the frequency of monotonic clock moving forward to catch up or wait.
* NTP sync can be only as good as network delay
* logical clock: based on auto-incrementing index; good for ordering events
* google spanner offers confidence interval;
  - order is determined only if CI do not overlap;
  - wait for CI overlap to disappear before committing a write
* process pause
  - can last indefinite amount of time
  - paused process does not know it has been paused   
  - **lease**: a node obtains a lease, which allows it to be leader for some time. The lease needs to be renewed before expiration. If not renewed, another leader will be elected.
  - garbage collect can be in round robin fashion, similar to rolling upgrade

#### Truth and Lie
* truth is defined by majority (quorum)
* **fencing token** when node obtain a lock, it comes with an auto incrementing number
  - when server accepts a write, it check the token number
  - only commit write if the token number is greatest ever observed
* Byzantines fault
  - node may be dishonest
  - In peer-to-peer networks, where there is no such cen‐ tral authority, Byzantine fault tolerance is more relevant.

#### System Model
An abstraction that describes what things an algorithm may assume.
1. Synchronous model: assumes bounded network delay, bounded process pau‐ ses, and bounded clock error
2. Partially synchronous model: sometimes exceeds the bounds for network delay, process pauses, and clock drift
3. Asynchronous model: no timing assumption

Node models
* Crash-stop faults: one-way fail, never come back
* Crash-recovery faults: node recovers; disk storage is preserved; in-memory stuff are lost
* Byzantine (arbitrary) faults: node can do anything

> For modeling real systems, the partially synchronous model with crash-recovery faults is generally the most useful model.

* Safety: always hold, and if broken, can trace back to exactly when it broke
* Liveness: may not hold, but will **eventually** hold

___
## Chapter 9 Consistency and Consensus

### Linearizability
Make a system appear as if there were only one copy of the data, and all operations on it are atomic
- Serializability: property of transaction; ok to have different serial order than the transaction time order
- Linearizability: property of read & write of a register; does **not** prevent transaction race condition
* serializable snapshot isolation is not linearizable by design
* Linearizability is required when enforcing hard uniqueness constraint
  - customers booking the same seat
  - selling more SKU than in stock
* A faster algorithm for linearizability does not exist, but weaker consistency models can be much faster

### CAP Theorem
* sloppy definition, best to avoid
* Consistency, Availability, Partition tolerance: pick 2 out of 3
* either Consistent or Available when Partitioned
* only considers one consistency model (namely linearizability) and one kind of fault (network partitions)

### Ordering and Causality
* linearizability: a total order of operations:
* causality defines a partial order,
* linearizability implies causality
* causal consistency is the strongest possible consistency model that does not slow down due to network delays, and remains available in the face of network failures
* lamport timestamp: (counter, node_ID)
  - provides total ordering:
  - every node and every client keeps track of the maximum counter value it has seen so far, and includes that maximum on every request.
  - When a node receives a request or response with a maximum counter value greater than its own counter value, it immediately increases its own counter to that maximum.
  - cannot tell whether two operations are concurrent or whether they are causally dependent
* total order broadcast

### Distributed Transaction and Consensus
FLP Result: there is no algorithm that is always able to reach consensus if there is a risk that a node may crash.
  - proved in the asynchronous system mode
  - becomes solvable if can use clocks/timeout and identify crash node

#### Two-phase commit
Achieving atomic transaction commit across multiple nodes
- a **blocking** atomic commit protocol
- phase 0: participant nodes read and write data
- phase 1: nodes area ready to commit; coordinator sends a prepare request to all nodes
  - if voting yes, node surrenders the right to abort, must retry if node fails
- phase 2: coordinator sends commit request if all are ready, otherwise send abort request
  - if all are ready, coordinator must retry sending commit request infinitely many times if timeout
  - if coordinator fails, it will read from its disk transaction log when it recovers, and send commit request
  - when coordinator fails before sending commit request, nodes are stuck "in-doubt"; cannot fail, commit, or time-out
- performance penalty is heavy (10 times slower) because of network round trip and force disk write of log

#### Heterogeneous Transaction: XA Transaction
Involve more than one technologies. For example Kafka dumps into Redis.
* XA: extended architecture
* a API for interacting with a transaction coordinator
Disadvantage:
1. coordinator is single point of failure
2. coordinator's log makes the server side no longer stateless
3. tend to amplify failure

### Fault Tolerant Consensus
Properties of consensus:
* uniform agreement: every two nodes agree (safety)
* Integrity: vote only once (safety)
* validity: only vote on proposed thing (safety)
* termination: all live node must eventually vote (liveness)

#### Viewstamped Replication
* a total order algorithm: messages to be delivered exactly once, in the same order
* equivalent to repeated rounds of consensus

### Membership and Coordination Services
* ZooKeeper and etcd are designed to hold small amounts of data that can fit entirely in memory
* That small amount of data is replicated across all the nodes using a fault-tolerant total order broadcast algorithm
* ZooKeeper is modeled after Google’s Chubby lock service
  * Linearizable atomic operations (require consensus)
  * Total ordering of operations
  * Failure detection
  * Change notifications  
* data managed by ZooKeeper is quite slow-changing
* service discovery: when startup, register network endpoints in a service registry
* Membership services: keepping track (consensus) of which node is alive/dead

#### Reducible to Consensus Problems
* Linearizable compare-and-set registers
* Atomic transaction commit
* Total order broadcast
* Locks and leases
* Membership/coordination service
* Uniqueness constraint

___
### Chapter 10 Batch Processing
Different types of systems and performance measure:
* microservice: response time
* batch: throughput
* stream: latency

#### Unix Philosophy
connecting pro‐ grams with pipes
* make each program do one thing well, break down large project to manageable chunks
* no interactive input
* chain different stages with pipes (stdin, stdout)
* input is immutable

#### Mapreduce
* HDFS is built on shared-nothing principle
* putting computation near data to avoid network load
* the number of map tasks is determined by the number of input file blocks
* the number of reduce tasks is configured by the job author
* intermediate outputs are written to tmp files in HDFS

#### Reduce-side Join
* sort-merge join: sort mapper output, so reducer see records of the same key together
  - only keep one user's record in memory at a time
#### Map-side join
* can handle hotkey (linchpin)
* no reducer and no sorting
* **broadcast hash join** join a small table (in memory) with a large table
* **partitioned hash join** require both tables to be partitioned in the same way
* **map-side merge join** require same partition method, and sorted data. Input file does not need to fit in memory

#### Batch processing output
* avoid writing to database with request
* produce the entire file, and replace the old file in storage (all-or-nothing)

#### Beyond Mapreduce
* tez and spark engine do not materialize intermediate files (recompute if fail)

___
## Chapter 11 Stream Processing
* event: a small, self- contained, immutable object containing the details of something that happened at some point in time.
* event is not the same as request: request needs to be validated before an event can happen

### Message Broker
* a server which producer and consumer can connect to
* consumers may be "fan-out" (different consumer group in kafka) or "load balance" (different process of the same consumer group)
* consumer is decoupled from producer, async processing
* message log: a producer sends a message by appending it to the end of the log, and a consumer receives messages by reading the log sequentially
* broker assigns a monotonically increasing sequence number, or offset, to every message
* log can be partitioned to different machines, which handle producer and consumers independently
  - no ordering guarantee across different partitions.

### Database and Stream
An example of a non-trivial application:
* an OLTP database to serve user requests
* a cache to speed up common requests
* a full-text index to handle search queries
* a data warehouse for analytics.

#### Methods to keep different systems in sync
Change data capture
- observing all data changes written to a database and extracting them in a form in which they can be replicated to other systems
- one system behaves as leader (truthful) the rest follows
- to rebuild the db, must have a snapshot to start with (have a known position or offset in the change log)
- log compaction: remove overwritten key write events, only keep the most recent one

Event Sourcing
* developed in the domain-driven design (DDD) community
* CDC treats each record as mutable and uses the current version (compaction)
* event sourcing keep a log of change events, which are immutable
* need the full history of events to reconstruct the final state
* need to save current state so it doesn't have to process full log every time

#### Processing Stream
Complex event processing
- designed to search for patterns in stream
- normal OLAP query keep data static, and query transient
- CEP keep query static, data flows transient

Stream analytics
* compute aggregation and statistics across a window
* probabilisitic algorithm: Bloom filter, HyperLogLog
* maintaining materializer view
* search for event in stream based on complex conditions

Time
* event time: according to device clock
* processing time: according to server clock
Estimating true event time:
1. measure time when event occurred, based on device clock  
2. measure time when request sent, based on device clock  
3. measure time when request is received, based on server clock
4. subtract 2 from 3, add the difference to 1.

Types of window
* tumbling window
* hopping window
* sliding window
* session window

Stream join
* stream-stream join (window join)
* stream-table join (enrichment)
* table-table join

Fault tolerance
* batch is "effectively once semantics" since input is treated immutable
* Flink generates rolling checkpoint and write them to storage
* spark uses microbatching
* both checkpoint and microbatch provide exactly once within stream framework, but not across different technologies

Idenpotence
* An idempotent operation is one that you can perform multiple times, and it has the same effect as if you performed it only once.
* Even if an operation is not naturally idempotent, it can often be made idempotent with a bit of extra metadata.
