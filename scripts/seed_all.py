"""
Master seed script — runs the full data pipeline:
  1. Generate synthetic CSVs (if not already present)
  2. Create PostgreSQL tables
  3. Load all CSVs into PostgreSQL
  4. (Phase 4) Load Neo4j graph  — stub
  5. (Phase 5) Generate documents — stub
  6. (Phase 5) Embed & index docs — stub

Usage:
  python scripts/seed_all.py
  python scripts/seed_all.py --skip-csv   # skip CSV generation
  python scripts/seed_all.py --dry-run    # validate without writing
"""

import argparse
import csv
import sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

# Ensure project root on path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from loguru import logger
from data.database import init_db, get_db_session, check_connection
from data.schemas.models import (
    Plant, ProductionLine, Supplier, Material, Machine,
    Sensor, Employee, ProductionOrder, MaintenanceEvent,
    QualityEvent, Telemetry,
)

RAW_DIR = ROOT / "data" / "raw"

# ─────────────────────────────────────────────────────────────
# CSV → ORM type coercion helpers
# ─────────────────────────────────────────────────────────────

def _str_or_none(v: str) -> str | None:
    return v.strip() if v and v.strip() else None

def _int_or_none(v: str) -> int | None:
    try: return int(v) if v.strip() else None
    except: return None

def _dec_or_none(v: str) -> Decimal | None:
    try: return Decimal(v) if v.strip() else None
    except: return None

def _date_or_none(v: str) -> date | None:
    try: return date.fromisoformat(v.strip()) if v.strip() else None
    except: return None

def _datetime_or_none(v: str) -> datetime | None:
    try: return datetime.fromisoformat(v.strip()) if v.strip() else None
    except: return None

def _bool(v: str) -> bool:
    return v.strip().lower() in ("true", "1", "yes")


# ─────────────────────────────────────────────────────────────
# Loaders per table
# ─────────────────────────────────────────────────────────────

def load_csv(filename: str) -> list[dict]:
    path = RAW_DIR / filename
    if not path.exists():
        logger.warning(f"  CSV not found: {path}")
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def seed_plants(session):
    rows = load_csv("plants.csv")
    objects = [
        Plant(
            plant_id=r["plant_id"],
            name=r["name"],
            location=_str_or_none(r.get("location", "")),
            country=_str_or_none(r.get("country", "")),
            established=_date_or_none(r.get("established", "")),
            capacity=_int_or_none(r.get("capacity", "")),
        )
        for r in rows
    ]
    session.bulk_save_objects(objects, update_changed_only=True)
    logger.info(f"  Plants:             {len(objects):>5}")


def seed_production_lines(session):
    rows = load_csv("production_lines.csv")
    objects = [
        ProductionLine(
            line_id=r["line_id"],
            name=r["name"],
            plant_id=_str_or_none(r.get("plant_id", "")),
            line_type=_str_or_none(r.get("line_type", "")),
            capacity_per_hour=_int_or_none(r.get("capacity_per_hour", "")),
            status=r.get("status", "active"),
        )
        for r in rows
    ]
    session.bulk_save_objects(objects, update_changed_only=True)
    logger.info(f"  Production lines:   {len(objects):>5}")


def seed_suppliers(session):
    rows = load_csv("suppliers.csv")
    objects = [
        Supplier(
            supplier_id=r["supplier_id"],
            name=r["name"],
            country=_str_or_none(r.get("country", "")),
            contact_name=_str_or_none(r.get("contact_name", "")),
            email=_str_or_none(r.get("email", "")),
            rating=_dec_or_none(r.get("rating", "")),
            tier=_int_or_none(r.get("tier", "1")) or 1,
        )
        for r in rows
    ]
    session.bulk_save_objects(objects, update_changed_only=True)
    logger.info(f"  Suppliers:          {len(objects):>5}")


def seed_materials(session):
    rows = load_csv("materials.csv")
    objects = [
        Material(
            material_id=r["material_id"],
            name=r["name"],
            category=_str_or_none(r.get("category", "")),
            unit=_str_or_none(r.get("unit", "")),
            unit_cost=_dec_or_none(r.get("unit_cost", "")),
            lead_time_days=_int_or_none(r.get("lead_time_days", "")),
            supplier_id=_str_or_none(r.get("supplier_id", "")),
        )
        for r in rows
    ]
    session.bulk_save_objects(objects, update_changed_only=True)
    logger.info(f"  Materials:          {len(objects):>5}")


def seed_machines(session):
    rows = load_csv("machines.csv")
    objects = [
        Machine(
            machine_id=r["machine_id"],
            name=r["name"],
            machine_type=_str_or_none(r.get("machine_type", "")),
            plant_id=_str_or_none(r.get("plant_id", "")),
            line_id=_str_or_none(r.get("line_id", "")),
            supplier_id=_str_or_none(r.get("supplier_id", "")),
            manufacturer=_str_or_none(r.get("manufacturer", "")),
            model_number=_str_or_none(r.get("model_number", "")),
            installation_date=_date_or_none(r.get("installation_date", "")),
            status=r.get("status", "operational"),
        )
        for r in rows
    ]
    session.bulk_save_objects(objects, update_changed_only=True)
    logger.info(f"  Machines:           {len(objects):>5}")


def seed_sensors(session):
    rows = load_csv("sensors.csv")
    objects = [
        Sensor(
            sensor_id=r["sensor_id"],
            machine_id=_str_or_none(r.get("machine_id", "")),
            sensor_type=_str_or_none(r.get("sensor_type", "")),
            unit=_str_or_none(r.get("unit", "")),
            min_threshold=_dec_or_none(r.get("min_threshold", "")),
            max_threshold=_dec_or_none(r.get("max_threshold", "")),
            location_tag=_str_or_none(r.get("location_tag", "")),
            status=r.get("status", "active"),
        )
        for r in rows
    ]
    session.bulk_save_objects(objects, update_changed_only=True)
    logger.info(f"  Sensors:            {len(objects):>5}")


def seed_employees(session):
    rows = load_csv("employees.csv")
    objects = [
        Employee(
            employee_id=r["employee_id"],
            name=r["name"],
            role=_str_or_none(r.get("role", "")),
            department=_str_or_none(r.get("department", "")),
            plant_id=_str_or_none(r.get("plant_id", "")),
            email=_str_or_none(r.get("email", "")),
            hire_date=_date_or_none(r.get("hire_date", "")),
        )
        for r in rows
    ]
    session.bulk_save_objects(objects, update_changed_only=True)
    logger.info(f"  Employees:          {len(objects):>5}")


def seed_production_orders(session):
    rows = load_csv("production_orders.csv")
    objects = [
        ProductionOrder(
            order_id=r["order_id"],
            product_name=r["product_name"],
            line_id=_str_or_none(r.get("line_id", "")),
            plant_id=_str_or_none(r.get("plant_id", "")),
            quantity=_int_or_none(r.get("quantity", "")),
            start_date=_date_or_none(r.get("start_date", "")),
            end_date=_date_or_none(r.get("end_date", "")),
            status=r.get("status", "planned"),
            priority=r.get("priority", "normal"),
        )
        for r in rows
    ]
    session.bulk_save_objects(objects, update_changed_only=True)
    logger.info(f"  Production orders:  {len(objects):>5}")


def seed_maintenance_events(session):
    rows = load_csv("maintenance_events.csv")
    objects = [
        MaintenanceEvent(
            event_id=r["event_id"],
            machine_id=_str_or_none(r.get("machine_id", "")),
            event_type=_str_or_none(r.get("event_type", "")),
            description=_str_or_none(r.get("description", "")),
            technician_id=_str_or_none(r.get("technician_id", "")),
            start_time=_datetime_or_none(r.get("start_time", "")),
            end_time=_datetime_or_none(r.get("end_time", "")),
            duration_hours=_dec_or_none(r.get("duration_hours", "")),
            root_cause=_str_or_none(r.get("root_cause", "")),
            parts_replaced=_str_or_none(r.get("parts_replaced", "")),
            cost=_dec_or_none(r.get("cost", "")),
        )
        for r in rows
    ]
    session.bulk_save_objects(objects, update_changed_only=True)
    logger.info(f"  Maintenance events: {len(objects):>5}")


def seed_quality_events(session):
    rows = load_csv("quality_events.csv")
    objects = [
        QualityEvent(
            quality_id=r["quality_id"],
            order_id=_str_or_none(r.get("order_id", "")),
            machine_id=_str_or_none(r.get("machine_id", "")),
            inspector_id=_str_or_none(r.get("inspector_id", "")),
            inspection_type=_str_or_none(r.get("inspection_type", "")),
            result=_str_or_none(r.get("result", "")),
            defect_type=_str_or_none(r.get("defect_type", "")),
            defect_count=_int_or_none(r.get("defect_count", "0")) or 0,
            notes=_str_or_none(r.get("notes", "")),
            inspection_time=_datetime_or_none(r.get("inspection_time", "")),
        )
        for r in rows
    ]
    session.bulk_save_objects(objects, update_changed_only=True)
    logger.info(f"  Quality events:     {len(objects):>5}")


def seed_telemetry(session, batch_size: int = 500):
    rows = load_csv("telemetry.csv")
    total = 0
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        objects = [
            Telemetry(
                sensor_id=_str_or_none(r.get("sensor_id", "")),
                machine_id=_str_or_none(r.get("machine_id", "")),
                value=Decimal(r["value"]),
                unit=_str_or_none(r.get("unit", "")),
                is_anomaly=_bool(r.get("is_anomaly", "false")),
                threshold_exceeded=_bool(r.get("threshold_exceeded", "false")),
                recorded_at=datetime.fromisoformat(r["recorded_at"]),
            )
            for r in batch
        ]
        session.bulk_save_objects(objects)
        session.flush()
        total += len(objects)
    logger.info(f"  Telemetry records:  {total:>5}")


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
def main(skip_csv: bool = False, dry_run: bool = False) -> None:
    logger.info("=" * 55)
    logger.info("  ESCE Master Seed Script")
    logger.info("=" * 55)

    # Step 1 — Generate CSVs
    if not skip_csv:
        logger.info("\n[1/4] Generating synthetic datasets...")
        if dry_run:
            logger.info("  DRY RUN: skipping CSV generation")
        else:
            import subprocess
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "generate_data.py")],
                capture_output=True, text=True,
            )
            print(result.stdout)
            if result.returncode != 0:
                logger.error(result.stderr)
                sys.exit(1)
    else:
        logger.info("[1/4] Skipping CSV generation (--skip-csv)")

    if dry_run:
        logger.info("DRY RUN: all subsequent steps skipped. CSVs validated.")
        return

    # Step 2 — Connect & create tables
    logger.info("\n[2/4] Initialising PostgreSQL...")
    if not check_connection():
        logger.error("Cannot connect to PostgreSQL. Is docker-compose up?")
        sys.exit(1)
    init_db()

    # Step 3 — Seed all tables (order matters for FK constraints)
    logger.info("\n[3/4] Seeding PostgreSQL tables...")
    with get_db_session() as session:
        seed_plants(session)
        seed_production_lines(session)
        seed_suppliers(session)
        seed_materials(session)
        seed_machines(session)
        seed_sensors(session)
        seed_employees(session)
        seed_production_orders(session)
        seed_maintenance_events(session)
        seed_quality_events(session)
        seed_telemetry(session)
    logger.info("  All tables seeded successfully.")

    # Step 4 — Stub for future phases
    logger.info("\n[4/4] Phase 4-5 stubs (Neo4j / ChromaDB)...")
    logger.info("  Neo4j graph loading  -> Phase 4")
    logger.info("  Document generation  -> Phase 5")
    logger.info("  Vector indexing      -> Phase 5")

    logger.info("\n" + "=" * 55)
    logger.info("  Seed complete!")
    logger.info("=" * 55 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ESCE Master Seed Script")
    parser.add_argument("--skip-csv", action="store_true", help="Skip CSV generation")
    parser.add_argument("--dry-run",  action="store_true", help="Validate without writing to DB")
    args = parser.parse_args()
    main(skip_csv=args.skip_csv, dry_run=args.dry_run)
