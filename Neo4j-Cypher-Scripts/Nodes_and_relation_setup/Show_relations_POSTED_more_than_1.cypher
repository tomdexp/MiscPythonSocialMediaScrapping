//Show relations : POSTED (more than 1)
MATCH (n)
WHERE size((n)-[:POSTED]->()) > 1 // Change value here to increase the filter
WITH n
LIMIT 100
MATCH p = (n)-[:POSTED]->()
RETURN p
LIMIT 100