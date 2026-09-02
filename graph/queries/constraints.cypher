// Idempotent Neo4j Cypher Constraints & Indexes
CREATE CONSTRAINT plant_id_unique IF NOT EXISTS FOR (p:Plant) REQUIRE p.plant_id IS UNIQUE;
CREATE CONSTRAINT line_id_unique IF NOT EXISTS FOR (l:ProductionLine) REQUIRE l.line_id IS UNIQUE;
CREATE CONSTRAINT supplier_id_unique IF NOT EXISTS FOR (s:Supplier) REQUIRE s.supplier_id IS UNIQUE;
CREATE CONSTRAINT material_id_unique IF NOT EXISTS FOR (m:Material) REQUIRE m.material_id IS UNIQUE;
CREATE CONSTRAINT machine_id_unique IF NOT EXISTS FOR (m:Machine) REQUIRE m.machine_id IS UNIQUE;
CREATE CONSTRAINT sensor_id_unique IF NOT EXISTS FOR (s:Sensor) REQUIRE s.sensor_id IS UNIQUE;
CREATE CONSTRAINT employee_id_unique IF NOT EXISTS FOR (e:Employee) REQUIRE e.employee_id IS UNIQUE;
CREATE CONSTRAINT order_id_unique IF NOT EXISTS FOR (o:ProductionOrder) REQUIRE o.order_id IS UNIQUE;
CREATE CONSTRAINT maint_event_id_unique IF NOT EXISTS FOR (me:MaintenanceEvent) REQUIRE me.event_id IS UNIQUE;
CREATE CONSTRAINT qual_event_id_unique IF NOT EXISTS FOR (qe:QualityEvent) REQUIRE qe.quality_id IS UNIQUE;

CREATE INDEX machine_name_idx IF NOT EXISTS FOR (m:Machine) ON (m.name);
CREATE INDEX sensor_type_idx IF NOT EXISTS FOR (s:Sensor) ON (s.sensor_type);
