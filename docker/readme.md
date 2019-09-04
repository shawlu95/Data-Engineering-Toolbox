#### jupyter/all-spark-notebook
jupyter/all-spark-notebook includes Python, R, and Scala support for Apache Spark, optionally on Mesos.
* Everything in jupyter/pyspark-notebook and its ancestor images
* IRKernel to support R code in Jupyter notebooks
* Apache Toree and spylon-kernel to support Scala code in Jupyter notebooks
* ggplot2, sparklyr, and rcurl packages
* Run all-spark notebook. Image: `d4cbf2f80a2a`
```bash
docker run -p 10000:8888 jupyter/all-spark-notebook:d4cbf2f80a2a
```

#### jupyter/tensorflow-notebook
* Everything in jupyter/scipy-notebook and its ancestor images
* tensorflow and keras machine learning libraries
* Run tensorflow notebook. Image: `d4cbf2f80a2a`
```bash
docker run -p 10001:8888 jupyter/tensorflow-notebook:d4cbf2f80a2a
```

___
#### Pyspark Notebook extended with GraphFrames

I found that connecting [GraphFrames](https://github.com/graphframes/graphframes) to [pyspark](http://spark.apache.org/) inside a Jupyter notebook was trickier than I expected. This Dockerfile is the simplest way I found to get it to work. It is based on `jupyter/pyspark-notebook`, which seemed to be a reasonable starting point.

```
python 3.7
spark 2.4
graphframes 0.7.0
```

Build the image and take note of the `id` to run the container. Be sure to forward port `8888` when starting it:

```bash
docker build .

# with GraphFrame
docker run -t --rm -p 10000:8888 01449e522820

# add neo4j
docker run -t --rm -p 10000:8888 8ecb36a9026a
```

The terminal output will contain the notebook url (`localhost:8888`) and a token. Visit the url in a browser and use the token to authenticate.

If everything goes will, the following minimalistic graph should build properly.

```python
from pyspark.sql import SparkSession
from graphframes import GraphFrame

session = SparkSession\
    .builder\
    .master('local')\
    .getOrCreate()

nodes = session.createDataFrame(
  [('1', 'Ada'), ('2', 'Bernd'), ('3', 'Claire')],
  ['id', 'name'])

edges = session.createDataFrame(
  [('1', '2'), ('2', '1'), ('1', '3')],
  ['src', 'dst'])

graph = GraphFrame(nodes, edges)
graph.inDegrees.show()
```

#### Useful Commands
```bash
# list container
docker ps -a

# stop & remove container
docker stop f8c22c8e9d87

# restart container
docker start -a f8c22c8e9d87

# check port (container must be running)
docker port 2c3bf3db31ca 8888
# 0.0.0.0:10000

docker rm f8c22c8e9d87
```

`-v /some/host/folder/for/work:/home/jovyan/work `- Mounts a host machine directory as folder in the container. Useful when you want to preserve notebooks and other work even after the container is destroyed. You must grant the within-container notebook user or group (`NB_UID` or `NB_GID`) write access to the host directory (e.g., `sudo chown 1000 /some/host/folder/for/work`).

```bash
sudo chown 1000 /Users/shawlu/Documents/GitHub/Data-Engineering-Toolbox/sparks
sudo chmod 1000 /Users/shawlu/Documents/GitHub/Data-Engineering-Toolbox/sparks
sudo chmod -R ugo+rw /Users/shawlu/Documents/GitHub/Data-Engineering-Toolbox/sparks

docker run -t --rm -p 10000:8888 -v /Users/shawlu/Documents/GitHub/Data-Engineering-Toolbox/sparks:/home/jovyan/work f8c22c8e9d87
```

#### Resource
* GitHub Jupyter Docker Stacks [[Link](https://github.com/jupyter/docker-stacks)]
* Image specification [[Link](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-tensorflow-notebook)]
* jupyter/all-spark-notebook [[Link](https://hub.docker.com/r/jupyter/all-spark-notebook/tags)]
* Running container [[Link](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/running.html)]
* Common setup [[Link](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html)]
* Docker CLI [[Link](https://docs.docker.com/engine/reference/commandline/cli/)]
