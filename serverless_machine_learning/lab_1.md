### Create ML datasets 

#### Datalab
To activate, enter `datalab create dataengvm --zone us-central1-a`, confirm and enter password. It takes 5 minutes to start. Enter Datalab via web port 8081.

> The connection to your Datalab instance remains open for as long as the datalab command is active. If the cloud shell used for running the datalab command is closed or interrupted, the connection to your Cloud Datalab VM will terminate. If that happens, you may be able to reconnect using the command `datalab connect dataengvm` in your new Cloud Shell (the datalab is called `dataengvm`).

Clone repo in notebook in a magic cell:

```bash
%bash
git clone https://github.com/GoogleCloudPlatform/training-data-analyst
cd training-data-analyst
```

Notebook: `datalab/training-data-analyst/courses/machine_learning/datasets/create_datasets.ipynb`

#### Trouble-shooting
* Failure: clear cell output.
* Reset kernel. Resetting the kernel causes the job in progress to change state to `FINISHED` and to have its FinalStatus marked as `SUCCEEDED`.
* If a job is stuck in execution, you can browse to the `Hadoop Applications` interface, and click on a job that is running. In the upper left corner there is a link that says "`Kill Application`".

#### Tensorflow
* Good for machine learning.
* Also good for solving differential equations.
* Why lazy evaluation: separate graph creation from execution (multiple remote hardware device).


#### Handy Syntax
Use boolean mask to drop rows.

```Python
def preprocess(trips_in):
  trips = trips_in.copy(deep=True)
  trips.fare_amount = trips.fare_amount + trips.tolls_amount
  del trips['tolls_amount']
  del trips['total_amount']
  del trips['trip_distance']
  del trips['pickup_datetime']
  qc = np.all([\
             trips['pickup_longitude'] > -78, \
             trips['pickup_longitude'] < -70, \
             trips['dropoff_longitude'] > -78, \
             trips['dropoff_longitude'] < -70, \
             trips['pickup_latitude'] > 37, \
             trips['pickup_latitude'] < 45, \
             trips['dropoff_latitude'] > 37, \
             trips['dropoff_latitude'] < 45, \
             trips['passenger_count'] > 0,
            ], axis=0)
  return trips[qc]

tripsqc = preprocess(trips)
tripsqc.describe()
```

Split datasets:

```Python
shuffled = tripsqc.sample(frac=1)
trainsize = int(len(shuffled['fare_amount']) * 0.70)
validsize = int(len(shuffled['fare_amount']) * 0.15)

df_train = shuffled.iloc[:trainsize, :]
df_valid = shuffled.iloc[trainsize:(trainsize+validsize), :]
df_test = shuffled.iloc[(trainsize+validsize):, :]
```

#### Handy Bash
```Bash
!head -10 taxi-valid.csv
!ls -l *.csv
```
