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
  
