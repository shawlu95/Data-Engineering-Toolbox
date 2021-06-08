## Designing Data Intensive Application
* [paperback]()
* data intensive: quantity of data, complexity, speed

### Anchor
* [Chapter 1: Terminology]
* [Chapter 2: Model and Language]
* [Chapter 3: Storage Engine]
* [Chapter 4: Data Format]
___
### Foundations of Data Systems

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
* graph model: for highly connected data
* polyglot persistence: relational will continue to be used along side a broad variety of non-relational
* impedance mismatch: need a translation layer between relational DB and object oriented program
* SQL is declarative: specify condition and result pattern, leave the DAG to optimizer
* imperative: must specify how data are transformed step by step; **difficult to parallelize**
