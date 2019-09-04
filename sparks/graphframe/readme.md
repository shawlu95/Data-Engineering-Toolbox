
## Cypher Refresher

### SQL Function
```JAVA

CREATE (ee:Person { name: "Emil", from: "Sweden", klout: 99 }),
(js:Person { name: "Johan", from: "Sweden", learn: "surfing" }),
(ir:Person { name: "Ian", from: "England", title: "author" }),
(rvb:Person { name: "Rik", from: "Belgium", pet: "Orval" }),
(ally:Person { name: "Allison", from: "California", hobby: "surfing" }),
(ee)-[:KNOWS {since: 2001}]->(js),
(ee)-[:KNOWS {rating: 5}]->(ir),
(js)-[:KNOWS]->(ir),
(js)-[:KNOWS]->(rvb),
(ir)-[:KNOWS]->(js),
(ir)-[:KNOWS]->(ally),
(rvb)-[:KNOWS]->(ally);

// Find the actor named "Tom Hanks"...
MATCH (tom {name: "Tom Hanks"}) RETURN tom;

// Find the movie with title "Cloud Atlas"...
MATCH (cloudAtlas {title: "Cloud Atlas"}) RETURN cloudAtlas;

MATCH (people:Person) RETURN people.name LIMIT 10;

MATCH (people:Person) WITH COUNT(people) AS c RETURN c;

// Find 10 people...
MATCH (movie:Movie) WITH COUNT(movie) AS c RETURN c;

// Find movies released in the 1990s...
MATCH (nineties:Movie)
WHERE nineties.released >= 1990
  AND nineties.released < 2000
RETURN nineties.title;

// List all Tom Hanks movies...
MATCH (tom:Person {name: "Tom Hanks"})-[:ACTED_IN]->(tomHanksMovies)
RETURN tom,tomHanksMovies;

// Who directed "Cloud Atlas"?
MATCH (cloudAtlas {title: "Cloud Atlas"})<-[:DIRECTED]-(directors)
RETURN directors.name;

// Tom Hanks' co-actors...
MATCH (tom:Person {name:"Tom Hanks"})-[:ACTED_IN]->(m)<-[:ACTED_IN]-(coActors)
RETURN coActors.name;

// How people are related to "Cloud Atlas"...
// What other relationships exist?
MATCH (people:Person)-[relatedTo]-(:Movie {title: "Cloud Atlas"})
RETURN people.name, Type(relatedTo), relatedTo;

// List the product categories provided by each supplier.
MATCH (s:Supplier)-->(:Product)-->(c:Category)
RETURN s.companyName as Company, collect(distinct c.categoryName) as Categories;

// Find the produce suppliers.
MATCH (c:Category {categoryName:"Produce"})<--(:Product)<--(s:Supplier)
RETURN DISTINCT s.companyName as ProduceSuppliers;

// Find customers who purchased produce categories
MATCH (cust:Customer)-[:PURCHASED]->(:Order)-[o:ORDERS]->(p:Product),
      (p)-[:PART_OF]->(c:Category {categoryName:"Produce"})
RETURN DISTINCT cust.contactName as CustomerName, SUM(o.quantity) AS TotalProductsPurchased
```

#### Solver Function
```JAVA
// Movies and actors up to 4 "hops" away from Kevin Bacon
MATCH (bacon:Person {name:"Kevin Bacon"})-[*1..4]-(hollywood)
RETURN DISTINCT hollywood;

// Extend Tom Hanks co-actors, to find co-co-actors who haven't worked with Tom Hanks...
MATCH (tom:Person {name:"Tom Hanks"})-[:ACTED_IN]->(m)<-[:ACTED_IN]-(coActors),
      (coActors)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cocoActors)
WHERE NOT (tom)-[:ACTED_IN]->()<-[:ACTED_IN]-(cocoActors) AND tom <> cocoActors
RETURN cocoActors.name AS Recommended, count(*) AS Strength ORDER BY Strength DESC;

// Find someone to introduce Tom Hanks to Tom Cruise
MATCH (tom:Person {name:"Tom Hanks"})-[:ACTED_IN]->(m)<-[:ACTED_IN]-(coActors),
      (coActors)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cruise:Person {name:"Tom Cruise"})
RETURN tom, m, coActors, m2, cruise;
```

![alt-text](assets/hank_cruise.svg)

#### Graph Algorithm
```JAVA
// Bacon path, the shortest path of any relationships to Meg Ryan
MATCH p=shortestPath(
  (bacon:Person {name:"Kevin Bacon"})-[*]-(meg:Person {name:"Meg Ryan"})
)
RETURN p;
```

#### Update
In contrast to specifying the node directly, the following query shows how to set a property for a node selected by an expression:
```Python
MATCH (n { name: 'Andy' })
SET (
CASE
WHEN n.age = 36
THEN n END ).worksIn = 'Malmo'
RETURN n.name, n.worksIn
```

#### Delete
* Nodes can't be deleted if relationships exist
* Delete both nodes and relationships together

```Java
// delete a node (must not have existing relationship)
MATCH (n:Person { name: 'UNKNOWN' })
DELETE n;

// delete a node and all its relationships
MATCH (n { name: 'Andy' })
DETACH DELETE n;

// delete relationship only
// This deletes all outgoing KNOWS relationships from the node with the name 'Andy'.
MATCH (n { name: 'Andy' })-[r:KNOWS]->()
DELETE r;

MATCH (n { name: 'Johan' })-[r:KNOWS]->(friend {name: 'Rik'})
DELETE r;

MATCH (n { name: 'Ian' })-[r:KNOWS]->(friend {name: 'Allison'})
DELETE r;

// delete all node & relationship
MATCH (n) DETACH DELETE n;
MATCH (n) RETURN n;
```

#### Remove [[Link](https://neo4j.com/docs/cypher-manual/3.5/clauses/remove/)]
```Java
// remove age property for a node
MATCH (a { name: 'Andy' })
REMOVE a.age
RETURN a.name, a.age;

// remove a label
MATCH (n { name: 'Peter' })
REMOVE n:German
RETURN n.name, labels(n);

// remove multiple labels
MATCH (n { name: 'Peter' })
REMOVE n:German:Swedish
RETURN n.name, labels(n);
```

### With
```Python
# aggregate
MATCH (david { name: 'David' })--(otherPerson)-->()
WITH otherPerson, count(*) AS foaf
WHERE foaf > 1
RETURN otherPerson.name;

# sort before collect
MATCH (n)
WITH n
ORDER BY n.name DESC LIMIT 3
RETURN collect(n.name);

# limit
MATCH (n { name: 'Anders' })--(m)
WITH m
ORDER BY m.name DESC LIMIT 1
MATCH (m)--(o)
RETURN o.name

# count degree
match (p)--(r) with p, count(r) as degree return p.name, degree order by degree desc;

match (p)--()
WITH p,count(*) as degree
match (p)-->()
WITH p,degree,count(*) as outdegree
match (p)<--()
return p.name, degree, outdegree, count(*) as indegree
order by degree desc;
```

```Python
CALL algo.unionFind.stream("Person", "KNOWS")
YIELD nodeId, setId
RETURN  algo.getNodeById(nodeId).name as name, setId as component

CALL algo.scc.stream("Person", "KNOWS")
YIELD nodeId, partition
RETURN  algo.getNodeById(nodeId).name as name, partition as component;

# assign component
CALL algo.unionFind.stream("Person", "KNOWS")
YIELD nodeId, setId
WITH algo.getNodeById(nodeId).name as name, setId as component
MATCH (p)
WHERE p.name = name
SET p += {component: component}
RETURN p;

# louvain
CALL algo.louvain.stream("Person", "KNOWS")
YIELD nodeId, communities
RETURN algo.getNodeById(nodeId).name as name, communities as communities;

CALL algo.louvain.stream("Person", "KNOWS")
YIELD nodeId, communities
WITH algo.getNodeById(nodeId).name as name, communities as communities
MATCH (p)
WHERE p.name = name
# SET p += {component: component}
SET p:component
RETURN p;

# labelPropagation
CALL algo.labelPropagation.stream("Person", "KNOWS", { iterations: 10 })
YIELD nodeId, label RETURN label,
collect(algo.getNodeById(nodeId).name) AS libraries ORDER BY size(libraries) DESC;

# triangle
CALL algo.triangle.stream("Person","KNOWS") YIELD nodeA, nodeB, nodeC
RETURN
  algo.getNodeById(nodeA).name AS nodeA,
  algo.getNodeById(nodeB).name AS nodeB,
  algo.getNodeById(nodeC).name AS nodeC;

CALL algo.triangleCount.stream('Person', 'KNOWS') YIELD nodeId, triangles, coefficient
WHERE coefficient > 0
RETURN algo.getNodeById(nodeId).name AS name, coefficient
ORDER BY coefficient DESC
LIMIT 10;

CALL algo.triangleCount.stream('Person', 'KNOWS') YIELD nodeId, triangles, coefficient
WHERE coefficient > 0
WITH algo.getNodeById(nodeId).name AS name, coefficient
ORDER BY coefficient DESC
LIMIT 10
MATCH (p)
WHERE p.name = name
SET p:Core, p += {core: True, coefficient: coefficient}
RETURN p;

# assign degree
MATCH (p)--(r)
WITH p.name AS name, count(r) AS degree
MATCH (p)
where p.name = name
SET p += {degree: degree}
RETURN p;

CALL algo.betweenness.stream("Person", "KNOWS")
YIELD nodeId, centrality
WITH algo.getNodeById(nodeId).name as name, centrality
MATCH (p)
where p.name = name
SET p += {betweenness: centrality}
RETURN p;

CALL algo.closeness.stream("Person", "KNOWS", {improved: true})
YIELD nodeId, centrality
WITH algo.getNodeById(nodeId).name as name, centrality
MATCH (p)
where p.name = name
SET p += {closeness: centrality}
RETURN p;

CALL algo.closeness.harmonic.stream("Person", "KNOWS")
YIELD nodeId, centrality
WITH algo.getNodeById(nodeId).name as name, centrality
MATCH (p)
where p.name = name
SET p += {harmonic: centrality}
RETURN p;

# Find Core
MATCH (p)
WITH p.component as c, MAX(p.degree) as maxdegree
WHERE maxdegree > 1
WITH c, maxdegree
MATCH (p)
WHERE p.degree = maxdegree
  and p.component = c
RETURN MAX(p.name), p.degree, p.component

# Mark Core
MATCH (p)
WITH p.component as c, MAX(p.degree) as maxdegree
WHERE maxdegree > 1
WITH c, maxdegree
MATCH (p)
WHERE p.degree = maxdegree
  and p.component = c
WITH MAX(p.name) as name, p.degree as degree, p.component as component
MATCH (p)
WHERE p.name = name
SET p:Core, p += {core: True}
RETURN p;

MATCH (p) SET p += {core: False};

MATCH (n)
REMOVE n:Core
return n;
```

#### Load CSV
```Python
WITH "https://github.com/neo4j-graph-analytics/book/raw/master/data/" AS base WITH base + "sw-nodes.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MERGE (:Library {id: row.id});

WITH "https://github.com/neo4j-graph-analytics/book/raw/master/data/" AS base WITH base + "sw-relationships.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MATCH (source:Library {id: row.src})
MATCH (destination:Library {id: row.dst}) MERGE (source)-[:DEPENDS_ON]->(destination);
```
#### Monitor
```
:sysinfo
```
