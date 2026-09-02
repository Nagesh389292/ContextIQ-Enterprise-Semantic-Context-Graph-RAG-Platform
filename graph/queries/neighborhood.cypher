// Traversal Query for 1-hop / 2-hop entity neighborhood subgraph
MATCH (n {machine_id: $entity_id})
OPTIONAL MATCH (n)-[r]-(m)
RETURN n, r, m
LIMIT 50;
