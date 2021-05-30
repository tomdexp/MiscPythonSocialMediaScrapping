//2) Setup Relations
LOAD CSV WITH HEADERS FROM 'file:///table_post.csv' AS row 
MATCH (post:Post {post_ID: row.post_ID})
MATCH (user:User {profile_ID: row.profile_ID})
MERGE (user)-[:POSTED]->(post);

LOAD CSV WITH HEADERS FROM 'file:///table_relation.csv' AS row 
MATCH (p1:User {profileUrl:row.username_following})
MATCH (p2:User {profileUrl:row.username_followed})
CREATE (p1)-[:FOLLOWS]->(p2);