#### Getting Started with Tensorflow

### Basic Syntax
Separation of graph building and execution.
```python
a = tf.constant([5, 3, 8])
b = tf.constant([3, -1, 2])
c = tf.add(a, b)

with tf.Session() as sess:
  result = sess.run(c)
  print(result)
```

Using feed_dict to handle unknown dimension.
```python
a = tf.placeholder(dtype=tf.int32, shape=(None,))  # batchsize x scalar
b = tf.placeholder(dtype=tf.int32, shape=(None,))
c = tf.add(a, b)
with tf.Session() as sess:
  result = sess.run(c, feed_dict={
      a: [3, 4, 5],
      b: [-1, 2, 3]
    })
  print(result)
```

Immediate execution using Eager.
```python
import tensorflow as tf
from tensorflow.contrib.eager.python import tfe

tfe.enable_eager_execution()
```
