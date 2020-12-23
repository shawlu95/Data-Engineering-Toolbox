### Work with structured and semi-structured data
> Hive is designed for batch jobs and not for transactions. It ingests data into a data warehouse format requiring a schema. It does not support real-time queries, row-level updates, or unstructured data. Some queries may run much slower than others due to the underlying transformations Hive has to implement to simulate SQL.

#### Preparation
* Create a Dataproc cluster with tags.
* Add Firewall rule([IP](http://ip4.me/)).
* Copy file to HDFS:
```bash
hadoop fs -mkdir /pet-details # create directory
hadoop fs -put pet-details.txt # Stage the data in HDFS.
```
Content of `pet-details.txt`:
```
Dog,Noir,Schnoodle,Black,21
Dog,Bree,MaltePoo,White,10
Dog,Pickles,Golden Retriever,Yellow,30
Dog,Sparky,Mutt,Gray,13
Cat,Tom,Alley,Yellow,11
Cat,Cleo,Siamese,Gray,22
Frog,Kermit,Bull,Green,1
Pig,Bacon,Pot Belly,Pink,30
Pig,Babe,Domestic,White,150
Dog,Rusty,Poodle,White,20
Cat,Joe,Mix,Black,15
```

#### Hive
* Load HDFS file into Hive (after loading, the file is moved from `/pet-details/pet-details.txt` to ` user > hive > warehouse > pets.db > details`). Activate Hive by typing in Cloud Shell: `hive`.

```SQL
CREATE DATABASE pets;
USE pets;

CREATE TABLE details (Type String, Name String, Breed String, Color String, Weight Int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
SHOW TABLES;
DESCRIBE pets.details;

load data INPATH '/pet-details/pet-details.txt' OVERWRITE INTO TABLE details;
```

#### Pig
* Sample Pig application `cat pet-details.pig`:
```pig
rmf /GroupedByType
x1 = load '/pet-details' using PigStorage(',') as (Type:chararray,Name:chararray,Breed:chararray,Color:chararray,Weight:int);
x2 = filter x1 by Type != 'Type';
x3 = foreach x2 generate Type, Name, Breed, Color, Weight, Weight / 2.24 as Kilos:float;
x4 = filter x3 by LOWER(Color) == 'black' or LOWER(Color) == 'white';
x5 = group x4 by Type;
store x5 into '/GroupedByType';
```

* Upload file to HDFS: `hadoop fs -put pet-details.txt /pet-details`.
* Run Pig app: `pig < pet-details.pig`.
* Look at output file at `GroupedByType/part-r-00000`
* Download file from HDFS:
```bash
cd
mkdir output
cd output
hadoop fs -get /GroupedByType/part* .
```
* Content of `part-r-00000`:
```
Cat     {(Cat,Joe,Mix,Black,15,6.696428571428571)}
Dog     {(Dog,Rusty,Poodle,White,20,8.928571428571427),(Dog,Bree,MaltePoo,White,10,4.4642857142857135),(Dog,Noir,Schnoodle,Black,21,9.374999999999998)}
Pig     {(Pig,Babe,Domestic,White,150,66.96428571428571)}
```
