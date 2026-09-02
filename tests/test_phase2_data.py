"""
Phase 2 tests — validates synthetic CSV datasets and ORM model imports.
Does NOT require a live database connection.
"""

import csv
import sys
import os
from pathlib import Path
import pytest

ROOT = Path(__file__).parent.parent
RAW_DIR = ROOT / "data" / "raw"
sys.path.insert(0, str(ROOT))


# ─────────────────────────────────────────────────────────────
# CSV existence and basic shape tests
# ─────────────────────────────────────────────────────────────
EXPECTED_CSVS = {
    "plants.csv":              (3,   ["plant_id", "name", "country"]),
    "production_lines.csv":    (8,   ["line_id", "name", "plant_id"]),
    "suppliers.csv":           (15,  ["supplier_id", "name", "country"]),
    "materials.csv":           (40,  ["material_id", "name", "supplier_id"]),
    "machines.csv":            (50,  ["machine_id", "name", "machine_type", "plant_id"]),
    "sensors.csv":             (150, ["sensor_id", "machine_id", "sensor_type"]),
    "employees.csv":           (100, ["employee_id", "name", "role"]),
    "production_orders.csv":   (500, ["order_id", "product_name", "status"]),
    "maintenance_events.csv":  (200, ["event_id", "machine_id", "event_type"]),
    "quality_events.csv":      (150, ["quality_id", "machine_id", "result"]),
    "telemetry.csv":           (10000, ["sensor_id", "machine_id", "value"]),
}


class TestCSVDatasets:
    """Validate all 11 synthetic CSV files."""

    @pytest.mark.parametrize("filename,expected_rows,required_cols", [
        (f, r, c) for f, (r, c) in EXPECTED_CSVS.items()
    ])
    def test_csv_exists(self, filename, expected_rows, required_cols):
        assert (RAW_DIR / filename).exists(), f"Missing: {filename}"

    @pytest.mark.parametrize("filename,expected_rows,required_cols", [
        (f, r, c) for f, (r, c) in EXPECTED_CSVS.items()
    ])
    def test_csv_row_count(self, filename, expected_rows, required_cols):
        path = RAW_DIR / filename
        if not path.exists():
            pytest.skip(f"{filename} not generated yet")
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == expected_rows, (
            f"{filename}: expected {expected_rows} rows, got {len(rows)}"
        )

    @pytest.mark.parametrize("filename,expected_rows,required_cols", [
        (f, r, c) for f, (r, c) in EXPECTED_CSVS.items()
    ])
    def test_csv_required_columns(self, filename, expected_rows, required_cols):
        path = RAW_DIR / filename
        if not path.exists():
            pytest.skip(f"{filename} not generated yet")
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            actual_cols = reader.fieldnames or []
        for col in required_cols:
            assert col in actual_cols, f"{filename}: missing column '{col}'"

    def test_machines_have_valid_plant_refs(self):
        """Every machine's plant_id must exist in plants.csv."""
        plants_path = RAW_DIR / "plants.csv"
        machines_path = RAW_DIR / "machines.csv"
        if not plants_path.exists() or not machines_path.exists():
            pytest.skip("CSVs not generated yet")

        with open(plants_path, encoding="utf-8") as f:
            plant_ids = {r["plant_id"] for r in csv.DictReader(f)}
        with open(machines_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                assert row["plant_id"] in plant_ids, (
                    f"Machine {row['machine_id']} has unknown plant_id {row['plant_id']}"
                )

    def test_sensors_have_valid_machine_refs(self):
        """Every sensor's machine_id must exist in machines.csv."""
        machines_path = RAW_DIR / "machines.csv"
        sensors_path  = RAW_DIR / "sensors.csv"
        if not machines_path.exists() or not sensors_path.exists():
            pytest.skip("CSVs not generated yet")

        with open(machines_path, encoding="utf-8") as f:
            machine_ids = {r["machine_id"] for r in csv.DictReader(f)}
        with open(sensors_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                assert row["machine_id"] in machine_ids, (
                    f"Sensor {row['sensor_id']} references unknown machine {row['machine_id']}"
                )

    def test_telemetry_has_no_null_values(self):
        """Telemetry records must always have a sensor_id, machine_id, and value."""
        path = RAW_DIR / "telemetry.csv"
        if not path.exists():
            pytest.skip("telemetry.csv not generated yet")
        with open(path, encoding="utf-8") as f:
            for i, row in enumerate(csv.DictReader(f)):
                assert row["sensor_id"].strip(), f"Row {i}: null sensor_id"
                assert row["machine_id"].strip(), f"Row {i}: null machine_id"
                assert row["value"].strip(),      f"Row {i}: null value"

    def test_telemetry_anomaly_rate(self):
        """Anomaly rate should be approximately 5% (allow ±3%)."""
        path = RAW_DIR / "telemetry.csv"
        if not path.exists():
            pytest.skip("telemetry.csv not generated yet")
        with open(path, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        anomalies = sum(1 for r in rows if r["is_anomaly"].lower() == "true")
        rate = anomalies / len(rows)
        assert 0.02 <= rate <= 0.08, f"Anomaly rate {rate:.2%} outside expected 2-8% range"


# ─────────────────────────────────────────────────────────────
# ORM model import and basic structure tests
# ─────────────────────────────────────────────────────────────
class TestORMModels:

    def test_imports(self):
        from data.schemas.models import (
            Base, Plant, ProductionLine, Supplier, Material, Machine,
            Sensor, Employee, ProductionOrder, MaintenanceEvent,
            QualityEvent, Telemetry,
        )
        assert Base is not None

    def test_table_names(self):
        from data.schemas.models import (
            Plant, ProductionLine, Supplier, Material, Machine,
            Sensor, Employee, ProductionOrder, MaintenanceEvent,
            QualityEvent, Telemetry,
        )
        assert Plant.__tablename__ == "plants"
        assert Machine.__tablename__ == "machines"
        assert Sensor.__tablename__ == "sensors"
        assert Telemetry.__tablename__ == "telemetry"

    def test_machine_has_relationships(self):
        from data.schemas.models import Machine
        # Verify relationship attributes exist
        assert hasattr(Machine, "sensors")
        assert hasattr(Machine, "maintenance_events")
        assert hasattr(Machine, "plant")

    def test_pydantic_schemas_import(self):
        from data.schemas.schemas import (
            PlantResponse, MachineResponse, MachineDetail,
            SupplierResponse, EntityStats,
        )
        assert PlantResponse is not None
        assert EntityStats is not None

    def test_database_module_import(self):
        from data.database import init_db, check_connection, get_db
        assert callable(init_db)
        assert callable(check_connection)
        assert callable(get_db)
