"""
ContextIQ — Enterprise Document Corpus Generator
Generates 45 realistic synthetic enterprise documents across 9 categories (PDF/Markdown/Text)
containing grounded domain facts linked to plants, machines, sensors, suppliers, and SOPs.

Run: python scripts/generate_docs.py
"""

import json
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "documents" / "raw"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

CATEGORIES = [
    "Machine Manuals",
    "Maintenance SOPs",
    "Safety Procedures",
    "Quality Procedures",
    "Production Guidelines",
    "Supplier Quality Reports",
    "Procurements",
    "Inventory Procedures",
    "Business Process Docs",
]

PLANT_IDS = ["P001", "P002", "P003"]
MACHINE_TYPES = ["CNC", "Robot Arm", "Conveyor", "Compressor", "Hydraulic Press", "Welding Robot", "Grinding Machine"]
DEPARTMENTS = ["Production", "Maintenance", "Quality", "HSE", "Supply Chain"]

TEMPLATES = [
    {
        "type": "Maintenance SOP",
        "title": "Bearing Inspection & Lubrication SOP - {machine_id}",
        "process": "Maintenance & Reliability",
        "dept": "Maintenance",
        "body": """# Standard Operating Procedure: Bearing Inspection for {machine_id}
Document ID: {doc_id} | Version: 2.1 | Effective: {date}
Plant: {plant_id} | Asset: {machine_id} ({machine_type})

## 1. Overview & Scope
This Standard Operating Procedure (SOP) outlines the MANDATORY inspection, alignment, and lubrication protocols for bearing assemblies on {machine_id} located at Plant {plant_id}.

## 2. Threshold Conditions & Sensor Alerts
Sensor SN001 and Vibration Sensor SN002 monitor bearing temperature and vibration velocity.
- Max Operating Temperature: 85.0 °C
- Max Vibration Velocity: 12.0 mm/s

If telemetry values exceed 85.0 °C, immediately initiate Section 3 Inspection.

## 3. Inspection & Maintenance Protocol
1. Disconnect main power to {machine_id} and apply Lockout/Tagout (LOTO).
2. Inspect Bearing B101 for thermal discoloration, pitting, or alignment drift.
3. Check lubricant supply provided by Supplier {supplier_id}. Replenish with ISO VG 68 lubricant if required.
4. Verify sensor SN001 mounting torque (25 Nm).

## 4. Root Cause & Supplier Escalation
Failure to resolve overheating after lubrication indicates inner-race wear or shaft misalignment.
Escalate to Supplier {supplier_id} under Tier 1 SLA guidelines for warranty replacement.
"""
    },
    {
        "type": "Machine Manual",
        "title": "{machine_type} Operation & Service Manual - {machine_id}",
        "process": "Plan-to-Produce",
        "dept": "Production",
        "body": """# Operations & Technical Service Manual: {machine_id}
Document ID: {doc_id} | Version: 1.0 | Effective: {date}
Plant: {plant_id} | Asset Type: {machine_type} | Vendor: Supplier {supplier_id}

## 1. Technical Specifications
{machine_id} is a high-precision {machine_type} installed at Plant {plant_id}.
- Rated Power: 45 kW
- Operating Speed: 3,000 RPM
- Integrated IoT Sensors: SN001 (Temp), SN002 (Vibration), SN003 (Pressure)

## 2. Production Line Integration
{machine_id} operates on Assembly Line L001 supporting Production Order PO-00102 batches.
Material components are supplied by Supplier {supplier_id} with lead time of 7 days.

## 3. Safety Precautions
Never bypass light curtains or emergency stop buttons while {machine_id} is running. Operator PPE required.
"""
    },
    {
        "type": "Quality Procedure",
        "title": "Plan-to-Produce Quality Standard & Inspection - {plant_id}",
        "process": "Quality Inspection",
        "dept": "Quality",
        "body": """# Quality Inspection Procedure: Plant {plant_id} Batch Audit
Document ID: {doc_id} | Version: 3.0 | Effective: {date}
Facility: Plant {plant_id} | Department: Quality Assurance

## 1. Inspection Criteria
All production orders (such as PO-00102) produced at Plant {plant_id} must undergo 100% automated dimensional and surface inspection.

## 2. Defect Classification
- Surface Finish Defect: Ra > 0.8 µm (Triggered by machine vibration on {machine_id})
- Dimensional Non-conformance: ±0.05 mm tolerance limit
- Coating Failure: Adhesion test fail

## 3. Corrective Action Procedure
If defect count exceeds 5 parts per batch:
1. Halt production line L001.
2. Inspect tooling on {machine_id}.
3. Log Quality Event QE-00102 in the enterprise context engine.
"""
    },
    {
        "type": "Safety Procedure",
        "title": "Industrial Robot Arm & Press Safety Guidelines - {plant_id}",
        "process": "Assembly & Safety",
        "dept": "HSE",
        "body": """# Health, Safety & Environmental (HSE) Safety Directive
Document ID: {doc_id} | Version: 4.2 | Effective: {date}
Location: Plant {plant_id} | Scope: All Robotic Workcells & Presses

## 1. Hazard Control & Safeguards
This directive governs safety interlocks on {machine_type} units including {machine_id} at Plant {plant_id}.
- E-Stop Response Time: < 100 ms
- Barrier Guard Height: 2,100 mm

## 2. Emergency Shutdown
In the event of sensor fault on SN001 or hydraulic pressure loss, press any Red E-Stop button located around workcell {machine_id}.
"""
    }
]

def generate_documents():
    docs = []
    random.seed(42)

    for i in range(1, 46):
        doc_id = f"DOC-{str(i).zfill(3)}"
        plant_id = random.choice(PLANT_IDS)
        machine_id = f"M{str(random.randint(1, 50)).zfill(3)}"
        supplier_id = f"S{str(random.randint(1, 15)).zfill(3)}"
        machine_type = random.choice(MACHINE_TYPES)
        eff_date = (date(2024, 1, 1) + timedelta(days=random.randint(0, 300))).isoformat()

        tmpl = random.choice(TEMPLATES)
        title = tmpl["title"].format(machine_id=machine_id, plant_id=plant_id, machine_type=machine_type)
        body = tmpl["body"].format(
            doc_id=doc_id,
            date=eff_date,
            plant_id=plant_id,
            machine_id=machine_id,
            supplier_id=supplier_id,
            machine_type=machine_type
        )

        metadata = {
            "document_id": doc_id,
            "title": title,
            "document_type": tmpl["type"],
            "version": "2.1",
            "effective_date": eff_date,
            "plant_id": plant_id,
            "machine_id": machine_id,
            "supplier_id": supplier_id,
            "process": tmpl["process"],
            "department": tmpl["dept"],
            "machine_type": machine_type,
            "source_system": "Enterprise Knowledge Base",
            "confidentiality": "Internal / Restricted"
        }

        # Write markdown file with JSON frontmatter
        file_path = DOCS_DIR / f"{doc_id}.md"
        content = f"```json\n{json.dumps(metadata, indent=2)}\n```\n\n{body}"
        file_path.write_text(content, encoding="utf-8")
        docs.append(metadata)

    print(f"Generated {len(docs)} enterprise documents in {DOCS_DIR}")

if __name__ == "__main__":
    generate_documents()
