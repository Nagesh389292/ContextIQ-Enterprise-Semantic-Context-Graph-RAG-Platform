"""
Phase 2 — Enterprise Data: Synthetic dataset generator.
Generates all 10 CSV files with realistic, cross-referenced manufacturing data.
Run: python scripts/generate_data.py
"""

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# Reference tables (IDs defined once, reused across files)
# ─────────────────────────────────────────────────────────────

PLANT_IDS = ["P001", "P002", "P003"]

LINE_IDS_BY_PLANT = {
    "P001": ["L001", "L002", "L003"],
    "P002": ["L004", "L005"],
    "P003": ["L006", "L007", "L008"],
}
ALL_LINE_IDS = [lid for lids in LINE_IDS_BY_PLANT.values() for lid in lids]

SUPPLIER_IDS = [f"S{str(i).zfill(3)}" for i in range(1, 16)]  # S001-S015

MACHINE_IDS = [f"M{str(i).zfill(3)}" for i in range(1, 51)]   # M001-M050

SENSOR_IDS  = [f"SN{str(i).zfill(3)}" for i in range(1, 151)] # SN001-SN150

MATERIAL_IDS = [f"MAT{str(i).zfill(3)}" for i in range(1, 41)] # MAT001-MAT040

EMPLOYEE_IDS = [f"E{str(i).zfill(3)}" for i in range(1, 101)]  # E001-E100

ORDER_IDS = [f"PO-{str(i).zfill(5)}" for i in range(1, 501)]   # PO-00001-PO-00500

MACHINE_TYPES = ["CNC", "Robot Arm", "Conveyor", "Compressor", "Hydraulic Press", "Welding Robot", "Grinding Machine"]
SENSOR_TYPES = ["temperature", "vibration", "pressure", "current", "speed", "humidity"]
MATERIAL_CATEGORIES = ["Bearing", "Motor", "Pump", "Controller", "Battery Module", "Sensor Unit", "Hydraulic Fluid", "Lubricant", "Steel Plate", "Circuit Board"]
EMPLOYEE_ROLES = ["Operator", "Maintenance Engineer", "Production Manager", "Quality Engineer", "Safety Officer"]
LINE_TYPES = ["Assembly", "Paint", "Battery", "Welding", "Quality Control", "Packaging"]

# Pre-assign machines to plants/lines
machine_plant_map: dict[str, str] = {}
machine_line_map: dict[str, str] = {}
machine_supplier_map: dict[str, str] = {}

for i, mid in enumerate(MACHINE_IDS):
    pid = PLANT_IDS[i % len(PLANT_IDS)]
    lids = LINE_IDS_BY_PLANT[pid]
    machine_plant_map[mid] = pid
    machine_line_map[mid] = random.choice(lids)
    machine_supplier_map[mid] = random.choice(SUPPLIER_IDS)

# Pre-assign sensors to machines (3 sensors per machine)
sensor_machine_map: dict[str, str] = {}
for i, sid in enumerate(SENSOR_IDS):
    sensor_machine_map[sid] = MACHINE_IDS[i % len(MACHINE_IDS)]

# Pre-assign employees to plants
employee_plant_map: dict[str, str] = {}
for i, eid in enumerate(EMPLOYEE_IDS):
    employee_plant_map[eid] = PLANT_IDS[i % len(PLANT_IDS)]


def rand_date(start: str, end: str) -> str:
    s = date.fromisoformat(start)
    e = date.fromisoformat(end)
    return (s + timedelta(days=random.randint(0, (e - s).days))).isoformat()


def rand_datetime(start: str, end: str) -> str:
    s = datetime.fromisoformat(start)
    e = datetime.fromisoformat(end)
    delta_secs = int((e - s).total_seconds())
    return (s + timedelta(seconds=random.randint(0, delta_secs))).isoformat()


# ─────────────────────────────────────────────────────────────
# 1. Plants
# ─────────────────────────────────────────────────────────────
def generate_plants():
    rows = [
        {"plant_id": "P001", "name": "Northgate Assembly Plant", "location": "Detroit, MI", "country": "USA", "established": "2008-03-01", "capacity": 500},
        {"plant_id": "P002", "name": "Eastside Manufacturing Hub",  "location": "Cleveland, OH", "country": "USA", "established": "2012-07-15", "capacity": 350},
        {"plant_id": "P003", "name": "Southern Components Facility", "location": "Nashville, TN", "country": "USA", "established": "2018-01-20", "capacity": 280},
    ]
    write_csv("plants.csv", rows)
    print(f"  ✓ plants.csv ({len(rows)} rows)")


# ─────────────────────────────────────────────────────────────
# 2. Production Lines
# ─────────────────────────────────────────────────────────────
def generate_production_lines():
    rows = []
    line_names = {
        "L001": "Assembly Line A", "L002": "Assembly Line B", "L003": "Paint Line",
        "L004": "Battery Assembly", "L005": "Quality Control Line",
        "L006": "Welding Line", "L007": "Grinding Line", "L008": "Packaging Line",
    }
    for pid, lids in LINE_IDS_BY_PLANT.items():
        for lid in lids:
            rows.append({
                "line_id": lid,
                "name": line_names[lid],
                "plant_id": pid,
                "line_type": random.choice(LINE_TYPES),
                "capacity_per_hour": random.randint(20, 120),
                "status": random.choices(["active", "maintenance", "idle"], weights=[80, 10, 10])[0],
            })
    write_csv("production_lines.csv", rows)
    print(f"  ✓ production_lines.csv ({len(rows)} rows)")


# ─────────────────────────────────────────────────────────────
# 3. Suppliers
# ─────────────────────────────────────────────────────────────
def generate_suppliers():
    countries = ["USA", "Germany", "Japan", "South Korea", "Italy", "Canada"]
    rows = []
    for sid in SUPPLIER_IDS:
        rows.append({
            "supplier_id": sid,
            "name": f"{fake.company()} Industries",
            "country": random.choice(countries),
            "contact_name": fake.name(),
            "email": fake.company_email(),
            "rating": round(random.uniform(3.0, 5.0), 1),
            "tier": random.choices([1, 2, 3], weights=[50, 35, 15])[0],
        })
    write_csv("suppliers.csv", rows)
    print(f"  ✓ suppliers.csv ({len(rows)} rows)")


# ─────────────────────────────────────────────────────────────
# 4. Materials
# ─────────────────────────────────────────────────────────────
def generate_materials():
    rows = []
    for mid in MATERIAL_IDS:
        category = random.choice(MATERIAL_CATEGORIES)
        supplier = random.choice(SUPPLIER_IDS)
        rows.append({
            "material_id": mid,
            "name": f"{category} {fake.bothify('##??').upper()}",
            "category": category,
            "unit": random.choice(["piece", "kg", "litre", "meter"]),
            "unit_cost": round(random.uniform(5.0, 2500.0), 2),
            "lead_time_days": random.randint(3, 45),
            "supplier_id": supplier,
        })
    write_csv("materials.csv", rows)
    print(f"  ✓ materials.csv ({len(rows)} rows)")


# ─────────────────────────────────────────────────────────────
# 5. Machines
# ─────────────────────────────────────────────────────────────
def generate_machines():
    manufacturers = {
        "CNC": ["FANUC", "Haas", "DMG Mori"],
        "Robot Arm": ["KUKA", "ABB", "Fanuc Robotics"],
        "Conveyor": ["Dorner", "Hytrol", "Lewco"],
        "Compressor": ["Atlas Copco", "Kaeser", "Ingersoll Rand"],
        "Hydraulic Press": ["Schuler", "Enerpac", "Greenerd"],
        "Welding Robot": ["Lincoln Electric", "Miller", "ESAB"],
        "Grinding Machine": ["Studer", "Okamoto", "Kellenberger"],
    }
    rows = []
    for mid in MACHINE_IDS:
        mtype = random.choice(MACHINE_TYPES)
        manufacturer = random.choice(manufacturers[mtype])
        rows.append({
            "machine_id": mid,
            "name": f"{mtype} Unit {mid}",
            "machine_type": mtype,
            "plant_id": machine_plant_map[mid],
            "line_id": machine_line_map[mid],
            "supplier_id": machine_supplier_map[mid],
            "manufacturer": manufacturer,
            "model_number": fake.bothify("??-####-??").upper(),
            "installation_date": rand_date("2015-01-01", "2023-12-31"),
            "status": random.choices(["operational", "maintenance", "fault", "idle"], weights=[75, 12, 5, 8])[0],
        })
    write_csv("machines.csv", rows)
    print(f"  ✓ machines.csv ({len(rows)} rows)")


# ─────────────────────────────────────────────────────────────
# 6. Sensors
# ─────────────────────────────────────────────────────────────
def generate_sensors():
    thresholds = {
        "temperature": (20.0, 85.0),
        "vibration":   (0.0, 12.0),
        "pressure":    (1.0, 10.0),
        "current":     (0.0, 50.0),
        "speed":       (0.0, 3000.0),
        "humidity":    (20.0, 90.0),
    }
    units = {
        "temperature": "°C", "vibration": "mm/s", "pressure": "bar",
        "current": "A", "speed": "RPM", "humidity": "%",
    }
    rows = []
    for sid in SENSOR_IDS:
        stype = random.choice(SENSOR_TYPES)
        lo, hi = thresholds[stype]
        rows.append({
            "sensor_id": sid,
            "machine_id": sensor_machine_map[sid],
            "sensor_type": stype,
            "unit": units[stype],
            "min_threshold": lo,
            "max_threshold": hi,
            "location_tag": random.choice(["bearing_front", "bearing_rear", "motor_housing", "coolant_port", "spindle", "gearbox"]),
            "status": random.choices(["active", "faulty", "calibrating"], weights=[90, 5, 5])[0],
        })
    write_csv("sensors.csv", rows)
    print(f"  ✓ sensors.csv ({len(rows)} rows)")


# ─────────────────────────────────────────────────────────────
# 7. Employees
# ─────────────────────────────────────────────────────────────
def generate_employees():
    rows = []
    for eid in EMPLOYEE_IDS:
        role = random.choice(EMPLOYEE_ROLES)
        dept_map = {
            "Operator": "Production", "Maintenance Engineer": "Maintenance",
            "Production Manager": "Operations", "Quality Engineer": "Quality",
            "Safety Officer": "HSE",
        }
        rows.append({
            "employee_id": eid,
            "name": fake.name(),
            "role": role,
            "department": dept_map[role],
            "plant_id": employee_plant_map[eid],
            "email": fake.company_email(),
            "hire_date": rand_date("2010-01-01", "2024-01-01"),
        })
    write_csv("employees.csv", rows)
    print(f"  ✓ employees.csv ({len(rows)} rows)")


# ─────────────────────────────────────────────────────────────
# 8. Production Orders
# ─────────────────────────────────────────────────────────────
def generate_production_orders():
    products = ["Vehicle Body Panel", "Engine Block", "Battery Module", "Transmission Assembly",
                "Door Frame", "Suspension Component", "Brake Assembly", "Exhaust System",
                "Steering Column", "Dashboard Assembly"]
    rows = []
    for oid in ORDER_IDS:
        lid = random.choice(ALL_LINE_IDS)
        pid = next(p for p, ls in LINE_IDS_BY_PLANT.items() if lid in ls)
        start = rand_date("2023-01-01", "2024-12-01")
        end   = (date.fromisoformat(start) + timedelta(days=random.randint(1, 30))).isoformat()
        rows.append({
            "order_id": oid,
            "product_name": random.choice(products),
            "line_id": lid,
            "plant_id": pid,
            "quantity": random.randint(50, 2000),
            "start_date": start,
            "end_date": end,
            "status": random.choices(["completed", "in_progress", "planned", "cancelled"], weights=[55, 25, 15, 5])[0],
            "priority": random.choices(["low", "normal", "high", "critical"], weights=[15, 55, 25, 5])[0],
        })
    write_csv("production_orders.csv", rows)
    print(f"  ✓ production_orders.csv ({len(rows)} rows)")


# ─────────────────────────────────────────────────────────────
# 9. Maintenance Events
# ─────────────────────────────────────────────────────────────
def generate_maintenance_events():
    event_types = ["preventive", "corrective", "emergency"]
    root_causes = [
        "Bearing wear", "Lubrication failure", "Overheating", "Electrical fault",
        "Sensor drift", "Vibration misalignment", "Seal leak", "Software fault",
        "Scheduled PM", "Operator error",
    ]
    parts = ["Bearing assembly", "Lubricant replenishment", "Sensor replacement",
             "Belt replacement", "Filter replacement", "Motor brushes", "Seal kit"]
    rows = []
    maint_ids = [f"ME-{str(i).zfill(5)}" for i in range(1, 201)]
    technicians = [e for e in EMPLOYEE_IDS[:50]]  # First 50 employees are maintenance

    for evid in maint_ids:
        mid = random.choice(MACHINE_IDS)
        etype = random.choices(event_types, weights=[50, 35, 15])[0]
        start_ts = rand_datetime("2023-01-01T06:00:00", "2024-12-31T22:00:00")
        duration = round(random.uniform(0.5, 12.0), 2)
        end_ts = (datetime.fromisoformat(start_ts) + timedelta(hours=duration)).isoformat()
        rows.append({
            "event_id": evid,
            "machine_id": mid,
            "event_type": etype,
            "description": f"{random.choice(root_causes)} detected on {mid}",
            "technician_id": random.choice(technicians),
            "start_time": start_ts,
            "end_time": end_ts,
            "duration_hours": duration,
            "root_cause": random.choice(root_causes),
            "parts_replaced": random.choice(parts),
            "cost": round(random.uniform(200.0, 15000.0), 2),
        })
    write_csv("maintenance_events.csv", rows)
    print(f"  ✓ maintenance_events.csv ({len(rows)} rows)")


# ─────────────────────────────────────────────────────────────
# 10. Quality Events
# ─────────────────────────────────────────────────────────────
def generate_quality_events():
    inspection_types = ["incoming", "in-process", "final", "supplier-audit"]
    defect_types = ["dimensional", "surface-finish", "material-composition",
                    "welding-defect", "coating-failure", "functional-test-fail", "none"]
    rows = []
    quality_ids = [f"QE-{str(i).zfill(5)}" for i in range(1, 151)]
    inspectors = EMPLOYEE_IDS[70:]  # Last 30 employees are quality engineers

    for qid in quality_ids:
        defect = random.choices(defect_types, weights=[10, 10, 8, 12, 8, 7, 45])[0]
        result = "fail" if defect != "none" else random.choices(["pass", "conditional"], weights=[90, 10])[0]
        rows.append({
            "quality_id": qid,
            "order_id": random.choice(ORDER_IDS),
            "machine_id": random.choice(MACHINE_IDS),
            "inspector_id": random.choice(inspectors),
            "inspection_type": random.choice(inspection_types),
            "result": result,
            "defect_type": defect,
            "defect_count": random.randint(1, 20) if defect != "none" else 0,
            "notes": fake.sentence(nb_words=12) if result != "pass" else "",
            "inspection_time": rand_datetime("2023-01-01T08:00:00", "2024-12-31T18:00:00"),
        })
    write_csv("quality_events.csv", rows)
    print(f"  ✓ quality_events.csv ({len(rows)} rows)")


# ─────────────────────────────────────────────────────────────
# 11. Telemetry (10,000 records)
# ─────────────────────────────────────────────────────────────
def generate_telemetry():
    thresholds = {
        "temperature": (20.0, 85.0),
        "vibration":   (0.0, 12.0),
        "pressure":    (1.0, 10.0),
        "current":     (0.0, 50.0),
        "speed":       (0.0, 3000.0),
        "humidity":    (20.0, 90.0),
    }
    units_map = {
        "temperature": "°C", "vibration": "mm/s", "pressure": "bar",
        "current": "A", "speed": "RPM", "humidity": "%",
    }

    # Build sensor type map
    import csv as _csv
    sensor_type_map: dict[str, tuple[str, float, float]] = {}
    sensor_rows_path = RAW_DIR / "sensors.csv"
    if sensor_rows_path.exists():
        with open(sensor_rows_path) as f:
            for row in _csv.DictReader(f):
                stype = row["sensor_type"]
                lo, hi = thresholds[stype]
                sensor_type_map[row["sensor_id"]] = (stype, lo, hi)

    rows = []
    for i in range(10_000):
        sid = random.choice(SENSOR_IDS)
        mid = sensor_machine_map[sid]
        if sid in sensor_type_map:
            stype, lo, hi = sensor_type_map[sid]
        else:
            stype = random.choice(list(thresholds.keys()))
            lo, hi = thresholds[stype]
        # 5% chance of anomaly (exceeds threshold)
        is_anomaly = random.random() < 0.05
        if is_anomaly:
            value = round(random.uniform(hi * 1.02, hi * 1.25), 4)
        else:
            value = round(random.uniform(lo, hi * 0.95), 4)
        rows.append({
            "sensor_id": sid,
            "machine_id": mid,
            "value": value,
            "unit": units_map.get(stype, ""),
            "is_anomaly": is_anomaly,
            "threshold_exceeded": value > hi or value < lo,
            "recorded_at": rand_datetime("2024-01-01T00:00:00", "2024-12-31T23:59:00"),
        })

    write_csv("telemetry.csv", rows)
    print(f"  ✓ telemetry.csv ({len(rows)} rows)")


# ─────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────
def write_csv(filename: str, rows: list[dict]) -> None:
    if not rows:
        return
    path = RAW_DIR / filename
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n[ESCE] Generating synthetic enterprise datasets -> {RAW_DIR}\n")
    generate_plants()
    generate_production_lines()
    generate_suppliers()
    generate_materials()
    generate_machines()
    generate_sensors()
    generate_employees()
    generate_production_orders()
    generate_maintenance_events()
    generate_quality_events()
    generate_telemetry()
    print(f"\n[ESCE] All datasets generated in {RAW_DIR}\n")
