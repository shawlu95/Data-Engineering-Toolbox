### Page Rank
List the top 5 node ids with the highest PageRank scores.
```
Top 5 (DESC):
263 0.002020291181518219
537 0.0019433415714531497
965 0.0019254478071662631
243 0.001852634016241731
285 0.001827372170064514
```

List the bottom 5 node ids with the lowest PageRank scores.
```
Bottom  (ASC):
558 0.0003286018525215297
93 0.0003513568937516577
62 0.00035314810510596274
424 0.0003548153864930145
408 0.00038779848719291705

processing completed, time elapsed: 9.44s
```

___
### HITS Implementation
List the 5 node ids with the highest hubbiness score.
```
Top 5 hubbiness (DESC):
840 1.0
155 0.9499618624906541
234 0.8986645288972266
389 0.8634171101843793
472 0.8632841092495219
```

List the 5 node ids with the lowest hubbiness score.
```
Bottom 5 hubbiness (ASC):
23 0.042066854890936534
835 0.05779059354433016
141 0.0645311764622518
539 0.06602659373418493
889 0.07678413939216454
```

List the 5 node ids with the highest authority score.
```
Top 5 authority (DESC):
893 1.0
16 0.9635572849634398
799 0.9510158161074017
146 0.9246703586198444
473 0.8998661973604051
```

List the 5 node ids with the lowest authority score.
```
Bottom 5 authority (ASC):
19 0.05608316377607618
135 0.06653910487622795
462 0.07544228624641901
24 0.08171239406816945
910 0.08571673456144878

processing completed, time elapsed: 18.28s
```

___
#### Code
Jupyter notebook: [page_rank.ipynb](page_rank.ipynb)

Python script: [page_rank.py](page_rank.py)
```bash
../../bin/spark-submit page_rank.py
```
