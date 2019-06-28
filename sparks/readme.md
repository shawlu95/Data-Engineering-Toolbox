### Spark Examples

The following examples are taken from Stanford course *CS246 Mining Massive Data Sets* (example 1 ~ 5) and miscellaneous sources.

___
#### Examples from *CS246 Mining Massive Data Sets*
##### 1. Word Count & Letter Count [[Open](word_count)]
Count frequency of words and letter from a given text file (e.g. hamlet).
* Map, flat-map.
* Regular expression in mapping.
* Running Spark in Docker image.

##### 2. Recommending Friends [[Open](recommend_friends)]
Emulating "People You May Know" features. Based on number of common friends, recommend users as potential new friends.
* De-duplication.
* Permutation, and use sorting to speed up program.

##### 3. Association Rules [[Open](association_rules)]
Emulating "People Who Bought this also Bought..." features. Implementing A-priori algorithm.
* Computing support in custom function.
* Finding frequent pair and frequent triple quickly.

##### 4. K-means on Spark [[Open](k_means)]
Explore the effects on convergence of different distance measures and initialization measures.
* Euclidean vs. Manhattan distance.
* Random vs. farthest initialization.

##### 5. Page Rank & HITS [[Open](page_rank)]
Page rank:
* Matrix *M* is large and is processed as an RDD.
* Implementing matrix-vector multiplication in Spark.

HITS:
* Link matrix *L*.
* Scaling factor *lambda*.
* Hubbiness vector *h*.
* Authority vector *a*.
