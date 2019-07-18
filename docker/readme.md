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

#### Resource
* GitHub Jupyter Docker Stacks [[Link](https://github.com/jupyter/docker-stacks)]
* Image specification [[Link](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-tensorflow-notebook)]
* jupyter/all-spark-notebook [[Link](https://hub.docker.com/r/jupyter/all-spark-notebook/tags)]
