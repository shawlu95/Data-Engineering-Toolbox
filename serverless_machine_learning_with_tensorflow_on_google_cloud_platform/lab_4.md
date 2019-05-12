### Refactoring to add batching and feature
#### Objective
* Code study: [notebok](https://github.com/shawlu95/training-data-analyst/blob/master/courses/machine_learning/tensorflow/c_batched.ipynb).
* Refactor the input (potentially distributed shards of files).
* Refactor the way the features are created.
* Create and train the model.
* Evaluate model.

#### Refactoring File Loading

* Dictionary has a `.pop(key)` method that pop the value of a key, removing it from dictionary.
* Set `num_epochs` to `None` for training, 1 for prediction.

```python
CSV_COLUMNS = ['fare_amount', 'pickuplon','pickuplat','dropofflon','dropofflat','passengers', 'key']
LABEL_COLUMN = 'fare_amount'
DEFAULTS = [[0.0], [-74.0], [40.0], [-74.0], [40.7], [1.0], ['nokey']]

def read_dataset(filename, mode, batch_size = 512):
  def _input_fn():
    def decode_csv(value_column):
      columns = tf.decode_csv(value_column, record_defaults = DEFAULTS)

      # feature is a dictionary (one row)
      features = dict(zip(CSV_COLUMNS, columns))

      # this is a scalar, not a dictionary
      label = features.pop(LABEL_COLUMN)
      return features, label

    # Create list of files that match pattern
    file_list = tf.gfile.Glob(filename)

    # Create dataset from file list, decode_csv is called on every line!
    dataset = tf.data.TextLineDataset(file_list).map(decode_csv)
    if mode == tf.estimator.ModeKeys.TRAIN:
        num_epochs = None # indefinitely
        dataset = dataset.shuffle(buffer_size = 10 * batch_size)
    else:
        num_epochs = 1 # end-of-input after this

    dataset = dataset.repeat(num_epochs).batch(batch_size)
    return dataset.make_one_shot_iterator().get_next()
  return _input_fn


def get_train():
  return read_dataset('./taxi-train.csv', mode = tf.estimator.ModeKeys.TRAIN)

def get_valid():
  return read_dataset('./taxi-valid.csv', mode = tf.estimator.ModeKeys.EVAL)

def get_test():
  return read_dataset('./taxi-test.csv', mode = tf.estimator.ModeKeys.EVAL)
```

#### Refactoring Feature Engineering
* Feature columns are defined at model creation as `feature_columns` param.
* Frature values are substituted in as `input_fn` param in `model.train`.

```python
INPUT_COLUMNS = [
    tf.feature_column.numeric_column('pickuplon'),
    tf.feature_column.numeric_column('pickuplat'),
    tf.feature_column.numeric_column('dropofflat'),
    tf.feature_column.numeric_column('dropofflon'),
    tf.feature_column.numeric_column('passengers'),
]

def add_more_features(feats):
  # Nothing to add (yet!)
  return feats

feature_cols = add_more_features(INPUT_COLUMNS)
```
