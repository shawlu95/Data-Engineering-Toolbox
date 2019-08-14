#### jupyter/all-spark-notebook
jupyter/all-spark-notebook includes Python, R, and Scala support for Apache Spark, optionally on Mesos.
* Everything in jupyter/pyspark-notebook and its ancestor images
* IRKernel to support R code in Jupyter notebooks
* Apache Toree and spylon-kernel to support Scala code in Jupyter notebooks
* ggplot2, sparklyr, and rcurl packages
* Run all-spark notebook. Image: `d4cbf2f80a2a`
```bash
docker pull jupyter/all-spark-notebook
docker run -p 10000:8888 jupyter/all-spark-notebook:d4cbf2f80a2a
```

#### jupyter/tensorflow-notebook
* Everything in jupyter/scipy-notebook and its ancestor images
* tensorflow and keras machine learning libraries
* Run tensorflow notebook. Image: `d4cbf2f80a2a`
```bash
docker pull jupyter/tensorflow-notebook
docker run -p 10001:8888 jupyter/tensorflow-notebook:d4cbf2f80a2a
```

#### pytorch/pytorch
–name gives a name to the container rather than a random one
-v maps the folder in the local machine to a folder inside the container (mounts the first path to the second – divided by the : symbol )
-p defines the ports on the local machine and the container

```bash
docker pull pytorch/pytorch

# must use absolute URL
docker run -it \
  --name pytorch1 \
  -v /Users/shawlu/Documents/GitHub/coursera/coursera_ai/week2/pytorch:/workspace \
  -p 5000:8888 \
  -p 5001:6006 pytorch/pytorch

# after booting up docker image
pip install jupyter

jupyter notebook --ip 0.0.0.0 --port 8888 --allow-root &

# change 127.0.0.1:8888 into 127.0.0.1:5000
http://127.0.0.1:8888/?token=...

# remove stopped container
docker system prune
```


#### Resource
* GitHub Jupyter Docker Stacks [[Link](https://github.com/jupyter/docker-stacks)]
* Image specification [[Link](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-tensorflow-notebook)]
* jupyter/all-spark-notebook [[Link](https://hub.docker.com/r/jupyter/all-spark-notebook/tags)]
