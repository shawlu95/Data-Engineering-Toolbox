### Mining Unstructured Data with Cloud Dataproc
This folder contains notes for the Coursera class *Leveraging Unstructured Data with Cloud Dataproc on Google Cloud Platform* ([link](https://www.coursera.org/learn/leveraging-unstructured-data-dataproc-gcp/home/welcome))
* Unstructured data: big data that you collect but don't analyze: email, news group, field inspection photos.
* Structured data have schema: rows columns and formal relationship.
* Unstructured data are defined in relative terms: can be structured for one task, but unstructured for another task (even if it has schema).
* Over 90% of enterprise data are unstructured.
> Structured data has a useful organization or schema. Unstructured data includes not only data that is without a schema, but also data that has some structure, but that structure is not useful for the intended analysis or query.

#### Approach to Big Data
* Vertical scaling: more powerful computer.
* Horizontal scaling: more computing nodes.
* Google File System -> Hadoop, HDFS
    - Hadoop, Pig, Hive, Spark

#### Operational Issues with Managing a Cluster
* Equipment, power.
* Utilization.
* Scaling.
* Sharding, rebalancing.

#### Ways to Create Dataproc Cluster
* a deployment manager template, which is an infrastructure automation service in Google Cloud
* CLI command. Custom VM e.g. 6 CPU, 30 GB * 1024 = 30720:
```bash
gcloud dataproc clusters create test-cluster /
    --worker-machine-type custom-6-30720
    --worker-machine-type custom-6-23040
```
* Google Cloud Console.
    * Create one cluster per job.
    * Give a unique name
    * Zone is important: same zone as data storage (where compute nodes are located) to minimize egress charge.

#### Preemptible VM
* Up to 80% discount. At the risk of being taken away as persistent VM.
* Used for non-critical jobs; processing only, not HDFS/data storage.
* > 50% preemptible VM has diminishing return and higher likelihood of failure.
* Busy regions may not have available preemptible VM.

#### Submitting Jobs
* Hadoop Job Interface/Resource manager: master node port 8088 (check status)
* Hadoop Admin interface: master node 9870

#### HiveQL
* Hive is declarative: specify how exactly to perform data analysis. Can't decide how to use resources.
* Pig makes execution plan, requests underlying system to determine how to process data (*Pipeline Paradigm*).
