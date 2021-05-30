//Show relations : post and user
MATCH (p1:User)-[]-(p2:User)
MATCH (p:Post)-[]-(u:User)
RETURN p1,p2,p,u;