//1) Setup Nodes
LOAD CSV WITH HEADERS FROM 'file:///table_post.csv' AS row 
MERGE (post:Post {post_ID: row.post_ID})
    ON CREATE SET post.postText = row.postText 
    ON CREATE SET post.profile_ID = row.profile_ID
    ON CREATE SET post.profileUrl = row.profileUrl
    ON CREATE SET post.likeCount = row.likeCount;

LOAD CSV WITH HEADERS FROM 'file:///table_profile.csv' AS row 
MERGE (user:User {profile_ID: row.profile_ID})
    ON CREATE SET user.userName = row.userName
    ON CREATE SET user.subCount = row.subCount
    ON CREATE SET user.profileUrl = row.profileUrl;