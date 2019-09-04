#### Chapter 1: Shortcomings of Relational DB
* Handle real relationships badly
  - changeable, variety (lots of null)
* slow to join, multi join
* no reverse pointing (bad for directional)
  * who are Bob's followers: `followed_by`
  * who does Bob follow: `follows`
* no **index free adjacency**
* must maintain linkage table
* bad for pattern matching
* only single, undirected, named relationships
* normalized schema not fast enough for real application needs
* data model can change after deployment
* Database refactoring is slow, risky, and expensive.

> Although denormalization may be a safe thing to do (assuming developers under‐ stand the denormalized model and how it maps to their domain-centric code, and have robust transactional support from the database), it is usually not a trivial task. For the best results, we usually turn to a true RDBMS expert to munge our normal‐ ized model into a denormalized one aligned with the characteristics of the underlying RDBMS and physical storage tier. In doing this, we accept that there may be substan‐ tial data redundancy.

#### Chapter 2: Data Modeling
Cypher is the most widely deployed, making it the de facto standard.
* node: has labels, properties (key-val pair, val can be primitive, array)
* edge: always directional, has properties

Languages
* SPARQL: RDF query language
* Gremlin: imperative
* Cypher: declarative
  - draw nodes with parentheses
  - relationships using pairs of dashes with greater-than or less-than signs
  - The < and > signs indicate relationship direction
  - prefix properties by colon

```Python
# Find pairs of friends who know Jim
MATCH (a:Person {name:'Jim'})-[:KNOWS]->(b)-[:KNOWS]->(c), (a)-[:KNOWS]->(c)
RETURN b, c;

MATCH (a:Person)-[:KNOWS]->(b)-[:KNOWS]->(c), (a)-[:KNOWS]->(c) WHERE a.name = 'Jim'
RETURN b, c;
```

#### Pitfalls
* Using nodes as edges, edges as nodes
  - create two types of nodes: user, email

``` Python
# create index
CREATE INDEX ON :Venue(name)

# create unique index
CREATE CONSTRAINT ON (c:Country) ASSERT c.name IS UNIQUE

# no more than 2 cities / streets away
<-[:STREET|CITY*1..2]-

MATCH (s:Node {char:'移'})-[:idiom]-(d:Node)
RETURN s, d;

MATCH p=(s:Node {char:'移'})-[:idiom*4]->(:Node)
RETURN s.char AS replier, length(p) - 1 AS depth;

MATCH p=(s:Node {char:'移'})-[:idiom*4]->(:Node)
RETURN p LIMIT 10;
```
