# Graph README — Neo4j Knowledge Graph

## Schema

### Node Labels
```
:Plant          :ProductionLine    :Machine
:Sensor         :Supplier          :Material
:Employee       :ProductionOrder   :MaintenanceEvent
:FailureEvent   :QualityEvent      :Document
```

### Relationship Types
```
(:Machine)-[:LOCATED_AT]->(:Plant)
(:Machine)-[:PART_OF]->(:ProductionLine)
(:Machine)-[:HAS_SENSOR]->(:Sensor)
(:Machine)-[:SUPPLIED_BY]->(:Supplier)
(:Supplier)-[:SUPPLIES]->(:Material)
(:ProductionOrder)-[:USES]->(:Material)
(:ProductionOrder)-[:EXECUTED_AT]->(:ProductionLine)
(:MaintenanceEvent)-[:AFFECTED]->(:Machine)
(:MaintenanceEvent)-[:PERFORMED_BY]->(:Employee)
(:FailureEvent)-[:AFFECTED]->(:Machine)
(:Document)-[:DOCUMENTS]->(:Machine)
```

## Sample Cypher Queries

See `queries/` directory for full query files.

## Implementation Status

- [ ] `schema.py` — Phase 4
- [ ] `loader.py` — Phase 4
- [ ] `queries/*.cypher` — Phase 4
