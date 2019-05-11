### Advanced SQL Queries
BigQuery public datasets [link](https://cloud.google.com/bigquery/public-data/)
#### Objective
* Use Nested fields (difference), Regular expressions (extract suffix), With statement, and Group and Having
* Extract programming information about code commits

#### Task 1. Get information about code commits
**diff** is a struct with many fields. Here we take the `new_path` field:

```SQL
SELECT
  author.email,
  diff.new_path AS path,
  DATETIME(TIMESTAMP_SECONDS(author.date.seconds)) AS date
FROM
  `bigquery-public-data.github_repos.commits`,
  UNNEST(difference) diff
WHERE
  EXTRACT(YEAR FROM TIMESTAMP_SECONDS(author.date.seconds))=2016
LIMIT 10
```

#### Task 2. Extract programming language
* Extract file suffix as language.
* Only keep language that contains purely of letters and has length < 8.

```SQL
WITH commits AS (
  SELECT
    author.email,
    LOWER(REGEXP_EXTRACT(diff.new_path, r'\.([^\./\(~_ \- #]*)$')) lang,
    diff.new_path AS path,
    TIMESTAMP_SECONDS(author.date.seconds) AS author_timestamp
  FROM
    `bigquery-public-data.github_repos.commits`,
    UNNEST(difference) diff
  WHERE
    EXTRACT(YEAR FROM TIMESTAMP_SECONDS(author.date.seconds))=2016
)
SELECT
  lang,
  COUNT(path) AS numcommits
FROM
  commits
WHERE
  LENGTH(lang)<8
  AND lang IS NOT NULL
  AND REGEXP_CONTAINS(lang, '[a-zA-Z]')
GROUP BY
  lang
HAVING
  numcommits > 100
ORDER BY
  numcommits DESC
```

#### Task 3. Weekend vs Weekday
Count the number of commits for each language on weekend vs weekday ([output](outputs/lab_3_task_3.csv)). It appears that the most popular weekend programming languages are JavaScript, PHP and C, Java, and Python.

```SQL
WITH commits AS (
  SELECT
    author.email,
    EXTRACT(DAYOFWEEK FROM TIMESTAMP_SECONDS(author.date.seconds)) BETWEEN 2 AND 6 is_weekday,
    LOWER(REGEXP_EXTRACT(diff.new_path, r'\.([^\./\(~_ \- #]*)$')) lang, diff.new_path AS path,
    TIMESTAMP_SECONDS(author.date.seconds) AS author_timestamp
  FROM
    `bigquery-public-data.github_repos.commits`,
    UNNEST(difference) diff
  WHERE
    EXTRACT(YEAR FROM TIMESTAMP_SECONDS(author.date.seconds))=2016
)
SELECT
  lang,
  is_weekday,
  COUNT(path) AS numcommits
FROM
  commits
WHERE
  lang IS NOT NULL
GROUP BY
  lang,
  is_weekday
HAVING
  numcommits > 100
ORDER BY
  numcommits DESC
```
