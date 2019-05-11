### MapReduce in Dataflow

#### Objective
* Identify Map and Reduce operations
* Execute the pipeline
* Use command line parameters

#### Apache Beam Packages
```bash
sudo apt-get install python-pip -y

pip install apache-beam[gcp] oauth2client==3.0.0
# downgrade as 1.11 breaks apitools
sudo pip install --force six==1.10
pip install -U pip
pip -V
sudo pip install apache_beam
```

#### Notes
Study the Python file [is_popular.py](https://github.com/shawlu95/training-data-analyst/blob/master/courses/data_analysis/lab2/python/is_popular.py).

* What custom arguments are defined? **Ans**: --output_prefix, --input
* What is the default output prefix? **Ans**: /tmp/output
* How is the variable output_prefix in main() set? **Ans**: declared by parser and overwritten if passed by `sys.args`.
* How are the pipeline arguments such as --runner set? **Ans**:
* What are the key steps in the pipeline? **Ans**: see below.
* Which of these steps happen in parallel? **Ans**: GetImports, PackageUse
* Which of these steps are aggregations? **Ans**: TotalUse, Top_5

Parser use case:
```python
import argparse
parser = argparse.ArgumentParser(description='Find the most used Java packages')
parser.add_argument('--output_prefix', default='/tmp/output', help='Output prefix')
parser.add_argument('--input', default='../javahelp/src/main/java/com/google/cloud/training/dataanalyst/javahelp/', help='Input directory')
```

Pipeline, see definition of transformation in the original [file](https://github.com/shawlu95/training-data-analyst/blob/master/courses/data_analysis/lab2/python/is_popular.py).
```python
(p
  | 'GetJava' >> beam.io.ReadFromText(input)
  | 'GetImports' >> beam.FlatMap(lambda line: startsWith(line, keyword))
  | 'PackageUse' >> beam.FlatMap(lambda line: packageUse(line, keyword))
  | 'TotalUse' >> beam.CombinePerKey(sum)
  | 'Top_5' >> beam.transforms.combiners.Top.Of(5, by_value)
  | 'write' >> beam.io.WriteToText(output_prefix)
)

p.run().wait_until_finish()
```

#### Execution Locally
Use default parameters:

```bash
cd ~/training-data-analyst/courses/data_analysis/lab2/python # navigate
python ./is_popular.py # execute
ls -al /tmp # check output files
cat /tmp/output-* # print output files
```

Pass custom parameters e.g. change output prefix (must be declared in parser):

```bash
python ./is_popular.py --output_prefix=/tmp/myoutput
ls -lrt /tmp/myoutput*
```

Output top 5 most popular packages imported:
```
[(u'org', 45), (u'org.apache', 44), (u'org.apache.beam', 44), (u'org.apache.beam.sdk', 43), (u'org.apache.beam.sdk.transforms', 16)]
```
