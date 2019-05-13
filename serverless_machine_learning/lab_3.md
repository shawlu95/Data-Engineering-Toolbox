### Estimator API
This lab focuses on Estimator API use case. The model is overfitted, and didn't even beat the baseline ([link](https://github.com/shawlu95/training-data-analyst/blob/master/courses/machine_learning/tensorflow/b_estimator.ipynb))

#### Notes
* Reset model isntead of training from scratch:
```python
tf.logging.set_verbosity(tf.logging.INFO)
OUTDIR = 'taxi_trained'
shutil.rmtree(OUTDIR, ignore_errors = True)
```

* Create a list of column object (numeric type):
```python
def make_feature_cols():
  input_columns = [tf.feature_column.numeric_column(k) for k in FEATURES]
  return input_columns
```

* Convert pandas dataframe to `tf.const`:
```python
def make_input_fn(df, num_epochs):
  return tf.estimator.inputs.pandas_input_fn(
    x = df,
    y = df[LABEL],
    batch_size = 128,
    num_epochs = num_epochs,
    shuffle = True,
    queue_capacity = 1000,
    num_threads = 1
  )
```
