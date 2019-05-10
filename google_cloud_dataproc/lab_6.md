### Machine Learning
#### Objective
Add Machine Learning (ML) to a Spark application.

#### Setup
* Create a cluster, a bucket (same name) and SSH into master node.
* Create environment variable:

```bash
APIKEY=<your-api-key>
BUCKET=<bucket name>
DEVSHELL_PROJECT_ID=<project ID>
export DEVSHELL_PROJECT_ID
export BUCKET
export APIKEY
```

* Study staging script:
    * Edits the three python scripts 01-dataprocML.py, 02-dataprocML.py, 03-dataprocML.py, and replaces the APIKEY, BUCKET, and DEVSHELL_PROJECT_ID with the values from the exported environment variables.
    * Copies the updated files to your bucket in Cloud Storage, so that Dataproc can access them.
    * Copies sample data files to your bucket.

```bash
#!/bin/bash
# Go to the standard location
cd ~/training-data-analyst/courses/unstructured/
# "If at first you don't succeed, try, try again."
#   If this is our first time here, backup the program files
#   If this is a subsequent run, restore fresh from backup before proceeding
#
if [ -d "backup" ]; then
  cp backup/*dataproc* .
else
  mkdir backup
  cp *dataproc* backup
fi
# Verify that the environment variables exist
#
OKFLAG=1
if [[ -v $BUCKET ]]; then
  echo "BUCKET environment variable not found"
  OKFLAG=0
fi
if [[ -v $DEVSHELL_PROJECT_ID ]]; then
  echo "DEVSHELL_PROJECT_ID environment variable not found"
  OKFLAG=0
fi
if [[ -v $APIKEY ]]; then
  echo "APIKEY environment variable not found"
  OKFLAG=0
fi
if [ OKFLAG==1 ]; then
  # Edit the script files
  sed -i "s/your-api-key/$APIKEY/" *dataprocML.py
  sed -i "s/your-project-id/$DEVSHELL_PROJECT_ID/" *dataprocML.py
  sed -i "s/your-bucket/$BUCKET/" *dataprocML.py
  # Copy python scripts to the bucket
  gsutil cp *dataprocML.py gs://$BUCKET/
  # Copy data to the bucket
  gsutil cp gs:\/\/cloud-training\/gcpdei\/road* gs:\/\/$BUCKET\/sampledata\/
  gsutil cp gs:\/\/cloud-training\/gcpdei\/time* gs:\/\/$BUCKET\/sampledata\/
fi
```

### Submitting Tasks
The three programs are "snapshots" from a development process. Each program builds on and enhances the one before it. Examining and running each program shows you how to progressively develop a Dataproc/Spark + Machine Learning application.

#### Task 1
This program is just a Python program. It will run on Dataproc, but it does not make use of any of the big data features. The program creates a sample line of text in memory and then passes it to the Natural Language Processing service for Sentiment Analysis.

The function SentimentAnalysis() is a wrapper around the REST API. This code creates the structured format of the request and passes the request along with the API Key.

Why is the output printed using a json.dumps?

You could do post-processing of the returned data using Python.

The stagelabs.sh script you ran in Task 1 should have replaced the DEVSHELL_PROJECT_ID, BUCKET, and APIKEY with your information from the environment variables.

**Submit**: in Dataproc -> Jobs, submit job with PySpark type, in same region, and main Python file `gs://<bucket name>/01-dataprocML.py` Equivalent command line:

```bash
gcloud dataproc jobs wait job-994b60b4 --project qwiklabs-gcp-968cc3e724ddeff8 --region us-central1
```

Console output:

```
19/05/10 19:33:04 INFO org.spark_project.jetty.util.log: Logging initialized @3128ms
19/05/10 19:33:04 INFO org.spark_project.jetty.server.Server: jetty-9.3.z-SNAPSHOT, build timestamp: unknown, git hash: unknown
19/05/10 19:33:04 INFO org.spark_project.jetty.server.Server: Started @3232ms
19/05/10 19:33:04 INFO org.spark_project.jetty.server.AbstractConnector: Started ServerConnector@22b422ad{HTTP/1.1,[http/1.1]}{0.0.0.0:4040}
19/05/10 19:33:04 WARN org.apache.spark.scheduler.FairSchedulableBuilder: Fair Scheduler configuration file not found so jobs will be scheduled in FIFO order. To use fair scheduling, configure pools in fairscheduler.xml or set spark.scheduler.allocation.file to a file that contains the configuration.
AIzaSyDAxezM0Ps8uYTefPJsVZOTjZqxLHKwcwU
qwiklabs-gcp-968cc3e724ddeff8
('Function returns: ', <type 'dict'>)
{
    "documentSentiment": {
        "magnitude": 0.8,
        "polarity": 1,
        "score": 0.8
    },
    "language": "en",
    "sentences": [
        {
            "sentiment": {
                "magnitude": 0.8,
                "polarity": 1,
                "score": 0.8
            },
            "text": {
                "beginOffset": -1,
                "content": "There are places I remember, all my life though some have changed."
            }
        }
    ]
}
19/05/10 19:33:07 INFO org.spark_project.jetty.server.AbstractConnector: Stopped Spark@22b422ad{HTTP/1.1,[http/1.1]}{0.0.0.0:4040}
Job output is complete
```

#### Task 2: Sentiment Analysis with Spark
Copy a text file to bucket:
```bash
gsutil cp /training/road-not-taken.txt gs://$BUCKET/sampledata/road-not-taken.txt
```
**Submit**: in Dataproc -> Jobs, submit job with PySpark type, in same region, and main Python file `gs://<bucket name>/02-dataprocML.py`. Equivalent command line:

```bash
gcloud dataproc jobs wait job-de4ccba1 --project qwiklabs-gcp-968cc3e724ddeff8 --region us-central1
```

Console outputs:
```
19/05/10 19:53:35 INFO org.spark_project.jetty.util.log: Logging initialized @3183ms
19/05/10 19:53:35 INFO org.spark_project.jetty.server.Server: jetty-9.3.z-SNAPSHOT, build timestamp: unknown, git hash: unknown
19/05/10 19:53:35 INFO org.spark_project.jetty.server.Server: Started @3295ms
19/05/10 19:53:35 INFO org.spark_project.jetty.server.AbstractConnector: Started ServerConnector@1bf61390{HTTP/1.1,[http/1.1]}{0.0.0.0:4040}
19/05/10 19:53:36 WARN org.apache.spark.scheduler.FairSchedulableBuilder: Fair Scheduler configuration file not found so jobs will be scheduled in FIFO order. To use fair scheduling, configure pools in fairscheduler.xml or set spark.scheduler.allocation.file to a file that contains the configuration.
AIzaSyDAxezM0Ps8uYTefPJsVZOTjZqxLHKwcwU
qwiklabs-gcp-968cc3e724ddeff8
19/05/10 19:53:40 INFO org.apache.hadoop.mapreduce.lib.input.FileInputFormat: Total input files to process : 1
19/05/10 19:53:40 INFO org.apache.hadoop.mapreduce.lib.input.FileInputFormat: Total input files to process : 1
19/05/10 19:53:40 INFO org.apache.hadoop.mapreduce.lib.input.CombineFileInputFormat: DEBUG: Terminated node allocation with : CompletedNodes: 1, size left: 0
('Magnitude= ', 0.8, ' | Score= ', -0.8, ' | Text= ', [u'roads diverged in a yellow wood,\nAnd sorry I could not travel both\nAnd be one traveler, long I stood\nAnd looked down one as far as I could\nTo where it bent in the undergrowth;'])
('Magnitude= ', 0.6, ' | Score= ', 0.6, ' | Text= ', [u'Then took the other, as just as fair,\nAnd having perhaps the better claim,\nBecause it was grassy and wanted wear;\nThough as for that the passing there\nHad worn them really about the same,'])
('Magnitude= ', 0.1, ' | Score= ', -0.1, ' | Text= ', [u'And both that morning equally lay\nIn leaves no step had trodden black.'])
('Magnitude= ', 0, ' | Score= ', 0, ' | Text= ', [u'Oh, I kept the first for another day!'])
('Magnitude= ', 0.1, ' | Score= ', -0.1, ' | Text= ', [u'Yet knowing how way leads on to way,\nI doubted if I should ever come back.'])
('Magnitude= ', 0.3, ' | Score= ', -0.3, ' | Text= ', [u'I shall be telling this with a sigh\nSomewhere ages and ages hence:\nTwo roads diverged in a wood, and I-\nI took the one less traveled by,\nAnd that has made all the difference.'])
19/05/10 19:53:42 INFO org.spark_project.jetty.server.AbstractConnector: Stopped Spark@1bf61390{HTTP/1.1,[http/1.1]}{0.0.0.0:4040}
Job output is complete
```


#### Task 3: Doing Something Useful
**Submit**: in Dataproc -> Jobs, submit job with PySpark type, in same region, and main Python file `gs://<bucket name>/02-dataprocML.py`. Equivalent command line:
```bash
gcloud dataproc jobs wait job-40e7e0d4 --project qwiklabs-gcp-968cc3e724ddeff8 --region us-central1
```

Outputs:

```
19/05/10 19:48:47 INFO org.spark_project.jetty.util.log: Logging initialized @2571ms
19/05/10 19:48:47 INFO org.spark_project.jetty.server.Server: jetty-9.3.z-SNAPSHOT, build timestamp: unknown, git hash: unknown
19/05/10 19:48:47 INFO org.spark_project.jetty.server.Server: Started @2682ms
19/05/10 19:48:47 INFO org.spark_project.jetty.server.AbstractConnector: Started ServerConnector@1bf61390{HTTP/1.1,[http/1.1]}{0.0.0.0:4040}
19/05/10 19:48:47 WARN org.apache.spark.scheduler.FairSchedulableBuilder: Fair Scheduler configuration file not found so jobs will be scheduled in FIFO order. To use fair scheduling, configure pools in fairscheduler.xml or set spark.scheduler.allocation.file to a file that contains the configuration.
AIzaSyDAxezM0Ps8uYTefPJsVZOTjZqxLHKwcwU
qwiklabs-gcp-968cc3e724ddeff8
19/05/10 19:48:51 INFO org.apache.hadoop.mapreduce.lib.input.FileInputFormat: Total input files to process : 1
19/05/10 19:48:51 INFO org.apache.hadoop.mapreduce.lib.input.FileInputFormat: Total input files to process : 1
19/05/10 19:48:51 INFO org.apache.hadoop.mapreduce.lib.input.CombineFileInputFormat: DEBUG: Terminated node allocation with : CompletedNodes: 1, size left: 0



('Magnitude= ', 0.8, ' | Score= ', -0.8, ' | Text= ', [u'And he put it to us in this\nway--marking the points with a lean forefinger--as we sat and lazily\nadmired his earnestness over this new paradox (as we thought it)\nand his fecundity.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', -0.8, ' | Text= ', [u'Badly.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', -0.8, ' | Text= ', [u'He walked with just such a limp as I have seen in footsore tramps.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', -0.8, ' | Text= ', [u'I might seem some old-world savage animal, only the more\ndreadful and disgusting for our common likeness--a foul creature to\nbe incontinently slain.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', -0.8, ' | Text= ', [u'I seemed to\nreel; I felt a nightmare sensation of falling; and, looking round,\nI saw the laboratory exactly as before.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', -0.8, ' | Text= ', [u'It let loose the judgment I had suspended\nupon their clothes, their frail light limbs, and fragile features.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', -0.8, ' | Text= ', [u'It struck my chin violently.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', -0.8, ' | Text= ', [u'It was here that I was destined, at a later date, to have\na very strange experience--the first intimation of a still stranger\ndiscovery--but of that I will speak in its proper place.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', -0.8, ' | Text= ', [u"It's too long a story to tell over greasy plates.'"], '\n')
('Magnitude= ', 0.8, ' | Score= ', -0.8, ' | Text= ', [u'The twinkling succession of\ndarkness and light was excessively painful to the eye.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', -0.8, ' | Text= ', [u'With a pretty absence of ceremony they began to eat the\nfruit with their hands, flinging peel and stalks, and so forth, into\nthe round openings in the sides of the tables.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u"'Easier, far easier down than up.'"], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u"'I nodded, pointed to the sun, and gave them such a vivid rendering\nof a thunderclap as startled them."], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u"'It would be remarkably convenient for the historian,' the\nPsychologist suggested."], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u"'There were others coming, and presently a little group of perhaps\neight or ten of these exquisite creatures were about me."], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'As I\nwent with them the memory of my confident anticipations of a\nprofoundly grave and intellectual posterity came, with irresistible\nmerriment, to my mind.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'At that the Time Traveller laughed cheerfully.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'But no interruptions!'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'But presently a fresh series of impressions\ngrew up in my mind--a certain curiosity and therewith a certain\ndread--until at last they took complete possession of me.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'Filby contented himself with laughter.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'For after the battle comes\nQuiet.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'I saw great and splendid architecture rising about\nme, more massive than any buildings of our own time, and yet, as it\nseemed, built of glimmer and mist.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'I saw mankind housed in\nsplendid shelters, gloriously clothed, and as yet I had found them\nengaged in no toil.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'Indeed, there was something in\nthese pretty little people that inspired confidence--a graceful\ngentleness, a certain childlike ease.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'It appears incredible to me that any kind of trick, however\nsubtly conceived and however adroitly done, could have been played\nupon us under these conditions.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'Nevertheless,\nthe general effect was extremely rich and picturesque.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'The fact is, the Time Traveller was one of those men who\nare too clever to be believed: you never felt that you saw all round\nhim; you always suspected some subtle reserve, some ingenuity in\nambush, behind his lucid frankness.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'The great buildings about me stood out clear and\ndistinct, shining with the wet of the thunderstorm, and picked out\nin white by the unmelted hailstones piled along their courses.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'The whole world will be intelligent,\neducated, and co-operating; things will move faster and faster\ntowards the subjugation of Nature.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'Then came one laughing towards me, carrying a chain of\nbeautiful flowers altogether new to me, and put it about my neck.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u"Then, 'Remarkable Behaviour of an Eminent\nScientist,' I heard the Editor say, thinking (after his wont) in\nheadlines."], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'These people of the remote\nfuture were strict vegetarians, and while I was with them, in spite\nof some carnal cravings, I had to be frugivorous also.'], '\n')
('Magnitude= ', 0.8, ' | Score= ', 0.8, ' | Text= ', [u'You who\nhave never seen the like can scarcely imagine what delicate and\nwonderful flowers countless years of culture had created.'], '\n')
('Magnitude= ', 0.9, ' | Score= ', -0.9, ' | Text= ', [u"'Is not that rather a large thing to expect us to begin upon?'\nsaid Filby, an argumentative person with red hair."], '\n')
('Magnitude= ', 0.9, ' | Score= ', -0.9, ' | Text= ', [u"'There I found a seat of some yellow metal that I did not recognize,\ncorroded in places with a kind of pinkish rust and half smothered\nin soft moss, the arm-rests cast and filed into the resemblance of\ngriffins' heads."], '\n')
('Magnitude= ', 0.9, ' | Score= ', -0.9, ' | Text= ', [u'His coat was dusty and dirty, and\nsmeared with green down the sleeves; his hair disordered, and as it\nseemed to me greyer--either with dust and dirt or because its colour\nhad actually faded.'], '\n')
('Magnitude= ', 0.9, ' | Score= ', -0.9, ' | Text= ', [u"I don't want to waste this model,\nand then be told I'm a quack.'"], '\n')
('Magnitude= ', 0.9, ' | Score= ', -0.9, ' | Text= ', [u'The fact is that, insensibly, the absolute strangeness of everything,\nthe sickly jarring and swaying of the machine, above all, the\nfeeling of prolonged falling, had absolutely upset my nerve.'], '\n')
('Magnitude= ', 0.9, ' | Score= ', -0.9, ' | Text= ', [u'The slowest snail that\never crawled dashed by too fast for me.'], '\n')
('Magnitude= ', 0.9, ' | Score= ', -0.9, ' | Text= ', [u'Then, in the\nintermittent darknesses, I saw the moon spinning swiftly through her\nquarters from new to full, and had a faint glimpse of the circling\nstars.'], '\n')
('Magnitude= ', 0.9, ' | Score= ', -0.9, ' | Text= ', [u'They are excessively unpleasant.'], '\n')
('Magnitude= ', 0.9, ' | Score= ', -0.9, ' | Text= ', [u'What if in this interval the race had lost its manliness and had\ndeveloped into something inhuman, unsympathetic, and overwhelmingly\npowerful?'], '\n')
('Magnitude= ', 0.9, ' | Score= ', 0.9, ' | Text= ', [u"'It's beautifully made,' he said."], '\n')
('Magnitude= ', 0.9, ' | Score= ', 0.9, ' | Text= ', [u"'Now, it is very remarkable that this is so extensively overlooked,'\ncontinued the Time Traveller, with a slight accession of\ncheerfulness."], '\n')
('Magnitude= ', 0.9, ' | Score= ', 0.9, ' | Text= ', [u"'The calm of evening was upon the world as I emerged from the great\nhall, and the scene was lit by the warm glow of the setting sun."], '\n')
('Magnitude= ', 0.9, ' | Score= ', 0.9, ' | Text= ', [u'But the fruits were very delightful;\none, in particular, that seemed to be in season all the time I was\nthere--a floury thing in a three-sided husk--was especially good,\nand I made it my staple.'], '\n')
('Magnitude= ', 0.9, ' | Score= ', 0.9, ' | Text= ', [u"I've had a most amazing time.'"], '\n')
('Magnitude= ', 0.9, ' | Score= ', 0.9, ' | Text= ', [u"It's plain\nenough, and helps the paradox delightfully."], '\n')
('Magnitude= ', 0.9, ' | Score= ', 0.9, ' | Text= ', [u'The air was free from gnats, the earth from weeds or\nfungi; everywhere were fruits and sweet and delightful flowers;\nbrilliant butterflies flew hither and thither.'], '\n')
('Magnitude= ', 0.9, ' | Score= ', 0.9, ' | Text= ', [u'We improve our\nfavourite plants and animals--and how few they are--gradually by\nselective breeding; now a new and better peach, now a seedless\ngrape, now a sweeter and larger flower, now a more convenient breed\nof cattle.'], '\n')
19/05/10 19:49:33 INFO org.spark_project.jetty.server.AbstractConnector: Stopped Spark@1bf61390{HTTP/1.1,[http/1.1]}{0.0.0.0:4040}
Job output is complete
```
