### Apache Flink
Open source platform for distributed steam and batch processing.

#### Speed:
Flink > Spark > Hadoop

#### Stateful Stream Processing
* Processing takes a state as input
* Has to be **fault tolerant**.

#### Event vs Processing Time
* Best to window by event time.
* Need to extract event time from data.
* Watermark: I don't expect thing older than this again.
* `setStramTimeCharacteristic`

#### Fault Tolerance
* Losing state! Need to recover.
* `enableCheckpointing`
* Safe point: global snapshot
  - can return at any time

#### Re-processing
* Return to a safe point, run updated code

#### Resource
Robust Stream Processing with Apache Flink [[Local](videos/robust_stream_processing_with_apache_flink.mp4)][[Youtube](https://www.youtube.com/watch?v=kyLtjuz5A0c)]
