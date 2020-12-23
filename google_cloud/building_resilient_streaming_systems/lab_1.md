### Publish Streaming Data into PubSub
#### Objective
1. Simulate your traffic sensor data into a Pub/Sub topic.
2. Integrate with Dataflow pipeline.
3. Store result in a BigQuery table.

#### Workflow
* SSH into a compute VM. Copy repository. Export `DEVSHELL_PROJECT_ID`.
* Basic CLI commands use case. When subscriber joined, messages published before are not retrievable.

```bash
$ gcloud pubsub topics create sandiego
Created topic [projects/qwiklabs-gcp-842ceb5fef108517/topics/sandiego].
$ gcloud pubsub topics publish sandiego --message "hello"
messageIds:
- '548778315955333'
$ gcloud pubsub subscriptions create --topic sandiego mySub1
Created subscription [projects/qwiklabs-gcp-842ceb5fef108517/subscriptions/mySub1].
$ gcloud pubsub subscriptions pull --auto-ack mySub1
Listed 0 items.
$ gcloud pubsub topics publish sandiego --message "hello again"
messageIds:
- '548774187391935'
$ gcloud pubsub subscriptions pull --auto-ack mySub1
┌─────────────┬─────────────────┬────────────┐
│     DATA    │    MESSAGE_ID   │ ATTRIBUTES │
├─────────────┼─────────────────┼────────────┤
│ hello again │ 548774187391935 │            │
└─────────────┴─────────────────┴────────────┘
$ gcloud pubsub subscriptions delete mySub1
Deleted subscription [projects/qwiklabs-gcp-842ceb5fef108517/subscriptions/mySub1].
```

#### Simulation
The [send_sensor_data.py](https://github.com/shawlu95/training-data-analyst/blob/master/courses/streaming/publish/send_sensor_data.py) simulates traffic sensors. The `speedFactor` parameter determines how fast the simulation will go. A speedFactor of 60 means "60 times faster" than the recorded timing. The simulation dataset is downloaded by [download_data.sh](https://github.com/shawlu95/training-data-analyst/blob/master/courses/streaming/publish/download_data.sh).

**Publisher**
```bash
# Install dependency
sudo apt-get install -y python-pip
sudo pip install -U google-cloud-pubsub

# start simulating
./send_sensor_data.py --speedFactor=60 --project $DEVSHELL_PROJECT_ID
```

**Subscriber**
```bash
gcloud pubsub subscriptions create --topic sandiego mySub2
gcloud pubsub subscriptions pull --auto-ack mySub2
gcloud pubsub subscriptions delete mySub2
```
