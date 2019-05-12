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
