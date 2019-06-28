### Association Rules
Association Rules are frequently used for Market Basket Analysis (MBA) by retailers to understand the purchase behavior of their customers. This information can be then used for many different purposes such as cross-selling and up-selling of products, sales promotions, loyalty programs, store design, discount plans and many others.

**Application in product recommendations**: The action or practice of selling additional products or services to existing customers is called cross-selling. Giving product recommendation is one of the examples of cross-selling that are frequently used by online retailers. One simple method to give product recommendations is to recommend products that are frequently browsed together by the customers.

Suppose we want to recommend new products to the customer based on the products they have already browsed online. Write a program using the A-priori algorithm to find products which are frequently browsed together. Fix the support to s =100 (i.e. product pairs need to occur together at least 100 times to be considered frequent) and find itemsets of size 2 and 3.

Use the online browsing behavior dataset from [browsing.txt](data/browsing.txt). Each line represents a browsing session of a customer. On each line, each string of 8 characters represents the ID of an item browsed during that session. The items are separated by spaces.

___
#### Output
Identify pairs of items (X, Y ) such that the support of {X, Y } is at least 100. For all such pairs, compute the confidence scores of the corresponding association rules: X ⇒ Y , Y ⇒ X. Sort the rules in decreasing order of confidence scores and list the top 5 rules in the writeup. Break ties, if any, by **lexicographically** increasing order on the left hand side of the rule.

```
Conf(DAI93865 -> FRO40251) = 1.0000000000
Conf(GRO85051 -> FRO40251) = 0.9991762768
Conf(GRO38636 -> FRO40251) = 0.9906542056
Conf(ELE12951 -> FRO40251) = 0.9905660377
Conf(DAI88079 -> FRO40251) = 0.9867256637
processing completed, time elapsed: 6.18s
```

Identify item triples (X, Y, Z) such that the support of {X, Y, Z} is at least 100. For all such triples, compute the confidence scores of the corresponding association rules: (X, Y ) ⇒ Z, (X, Z) ⇒ Y , (Y, Z) ⇒ X. Sort the rules in decreasing order of confidence scores and list the top 5 rules in the writeup. Order the left-hand-side pair **lexicographically** and break ties, if any, by lexicographical order of the first then the second item in the pair.

```
Conf(DAI23334, ELE92920 -> DAI62779) = 1.0000000000
Conf(DAI31081, GRO85051 -> FRO40251) = 1.0000000000
Conf(DAI55911, GRO85051 -> FRO40251) = 1.0000000000
Conf(DAI62779, DAI88079 -> FRO40251) = 1.0000000000
Conf(DAI75645, GRO85051 -> FRO40251) = 1.0000000000
processing completed, time elapsed: 13.91s
```

___
#### Code
Jupyter notebook: [association_rules.ipynb](association_rules.ipynb)

Python script: [association_rules.py](association_rules.py)
```bash
../../bin/spark-submit association_rules.py data/browsing.txt
```
