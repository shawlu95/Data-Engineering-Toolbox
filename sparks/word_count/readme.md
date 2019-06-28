### Word & Letter Count
This directory contains two spark programs: [count_word.py](count_word.py) and [count_letter.py](count_letter.py). Here are two ways to run the programs: (1) Jupyter notebook; (2) spark-submit.

___
#### Run in Jyputer
Install and launch the docker image [jupyter/all-spark-notebook](https://hub.docker.com/r/jupyter/all-spark-notebook/tags). Open [word_count.ipynb](word_count.ipynb).

```bash
# for example, launch the docker image at port 1000
docker run -p 10000:8888 jupyter/all-spark-notebook:d4cbf2f80a2a
```

___
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

___
#### Results

Word count (top 10):
```
('', 197060),
('the', 23455),
('I', 22225),
('and', 18715),
('to', 16433),
('of', 15830),
('a', 12851),
('you', 12236),
('my', 10840),
('in', 10074)
```

Letter count:
```
(a, 86000)
(b, 46001)
(c, 34983)
(d, 39173)
(e, 20409)
(f, 37186)
(g, 21167)
(h, 61028)
(i, 62420)
(j, 3372)
(k, 9535)
(l, 32389)
(m, 56252)
(n, 27313)
(o, 43712)
(p, 28059)
(q, 2388)
(r, 15234)
(s, 75226)
(t, 127781)
(u, 9230)
(v, 5801)
(w, 60097)
(x, 14)
(y, 25926)
(z, 79)
```
