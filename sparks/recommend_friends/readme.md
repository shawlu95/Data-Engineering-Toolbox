### Recommending Friends

Write a Spark program that implements a simple “People You Might Know” social network friendship recommendation algorithm. The key idea is that if two people have a lot of mutual friends, then the system should recommend that they connect with each other.

#### Data
* Associated data file is [soc-LiveJournal1Adj.txt](soc-LiveJournal1Adj.txt).
* The file contains the adjacency list and has multiple lines in the following format: `<User><TAB><Friends>`

Here, `<User>` is a unique integer ID corresponding to a unique user and `<Friends>` is a comma separated list of unique IDs corresponding to the friends of the user with the unique ID `<User>`. Note that the friendships are mutual (i.e., edges are undirected): if A is friend with B then B is also friend with A. The data provided is consistent with that rule as there is an explicit entry for each side of each edge.

Let us use a simple algorithm such that, for each user U, the algorithm rec- ommends N = 10 users who are not already friends with U, but have the most number of mutual friends in common with U.

#### Pipeline sketch
1. Construct candidate pairs for users who share common friends (map task).

2. Count the number of common friends for each pair of users and exclude from those pairs those who are already friends (reduce task).

3. Permute the ordering of key so that a common friend is counted for each user in a pair (map task).

4. For each user, order all users with whom he shares common friends by the number of common friends they share (groupByKey, similar to reduce task).

#### Output
```
924	439,2409,6995,11860,15416,43748,45881
8941	8943,8944,8940
8942	8939,8940,8943,8944
9019	9022,317,9023
9020	9021,9016,9017,9022,317,9023
9021	9020,9016,9017,9022,317,9023
9022	9019,9020,9021,317,9016,9017,9023
9990	13134,13478,13877,34299,34485,34642,37941
9992	9987,9989,35667,9991
9993	9991,13134,13478,13877,34299,34485,34642,37941
processing completed, time elapsed: 241.91s
```

#### Code
Jupyter notebook: [recommend_friends.ipynb](recommend_friends.ipynb)

Python script: [recommend_friends.py](recommend_friends.py)
```bash
bin/spark-submit hw1/q1/q1_code.py hw1/q1/data/soc-LiveJournal1Adj.txt
```
