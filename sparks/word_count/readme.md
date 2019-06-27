### Word Count
This directory contains two spark programs: word count and letter count.

#### Run in Jyputer
Install and launch the docker image [jupyter/all-spark-notebook](https://hub.docker.com/r/jupyter/all-spark-notebook/tags). Open [word_count.ipynb](word_count.ipynb).

```bash
# for example, launch the docker image at port 1000
docker run -p 10000:8888 jupyter/all-spark-notebook:d4cbf2f80a2a
```

#### Submit to Spark
Run Spark in development mode:

```bash
bin/pyspark
```

Submit program to PySpark:
* Python script: `count_letter.py`
* Input file: `pg100.txt`
* Output directory: `word_count` (must not exist yet)

```bash
bin/spark-submit count_word.py pg100.txt word_count
bin/spark-submit count_letter.py pg100.txt
```
