# Ontology README — Enterprise Manufacturing Semantic Model

This directory contains the full **RDF/OWL/SHACL** ontology for the Enterprise Semantic Context Engine.

## Files

| File | Format | Description |
|---|---|---|
| `enterprise.ttl` | Turtle (RDF/RDFS) | Core ontology — classes, properties, relationships |
| `enterprise.owl` | OWL/XML | OWL axioms — cardinality, domain/range constraints |
| `shapes.ttl` | Turtle (SHACL) | Validation shapes for entity constraints |

## Namespace

```
PREFIX : <http://enterprise-sce.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX sh: <http://www.w3.org/ns/shacl#>
```

## Class Hierarchy (28 classes)

```
owl:Thing
├── EnterpriseAsset
│   ├── Machine
│   │   ├── CNCMachine
│   │   ├── RobotArm
│   │   ├── Compressor
│   │   ├── ConveyorBelt
│   │   └── HydraulicPress
│   ├── Sensor
│   │   ├── TemperatureSensor
│   │   ├── VibrationSensor
│   │   └── PressureSensor
│   ├── ProductionLine
│   └── Plant
│
├── BusinessEntity
│   ├── Supplier
│   ├── Employee
│   │   ├── Operator
│   │   ├── MaintenanceEngineer
│   │   └── QualityEngineer
│   ├── Customer
│   └── Material
│
├── BusinessProcess
│   ├── ProcureToPay
│   ├── PlanToProduce
│   ├── MaintenanceProcess
│   └── QualityInspection
│
├── Document
│   ├── Manual
│   ├── SOP
│   ├── SafetyProcedure
│   └── QualityProcedure
│
└── Event
    ├── MaintenanceEvent
    ├── ProductionEvent
    └── FailureEvent
```

## Key Object Properties

| Property | Domain | Range | Constraint |
|---|---|---|---|
| `installedAt` | Machine | Plant | exactly 1 |
| `partOf` | Machine | ProductionLine | min 1 |
| `hasSensor` | Machine | Sensor | min 1 |
| `suppliedBy` | Machine | Supplier | — |
| `supplies` | Supplier | Material | min 1 |
| `usesMaterial` | ProductionOrder | Material | min 1 |
| `executedAt` | ProductionOrder | ProductionLine | exactly 1 |
| `affects` | MaintenanceEvent | Machine | min 1 |
| `generates` | Sensor | TelemetryEvent | — |

## SHACL Validation Rules

Every `Machine` must have:
- `:machineId` (xsd:string, exactly 1)
- `:installedAt` (exactly 1 Plant)
- `:manufacturer` (xsd:string)
- `:hasSensor` (min 1 Sensor)

Every `Supplier` must have:
- `:supplierId` (xsd:string, exactly 1)
- `:name` (xsd:string)
- `:country` (xsd:string)

Every `ProductionOrder` must have:
- `:orderId` (xsd:string, exactly 1)
- `:executedAt` (exactly 1 ProductionLine)
- `:startDate` (xsd:date)

## Implementation Status

- [ ] `enterprise.ttl` — Phase 3
- [ ] `enterprise.owl` — Phase 3
- [ ] `shapes.ttl` — Phase 3
