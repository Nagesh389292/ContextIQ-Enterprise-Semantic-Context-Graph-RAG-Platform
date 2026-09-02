"""
Pydantic v2 schemas for request/response validation across the API.
Mirrors the SQLAlchemy ORM models but is serialization-layer-only.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr


# ─────────────────────────────────────────────────────────────
# Shared base — all response models use model_validate
# ─────────────────────────────────────────────────────────────
class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────
# Plant
# ─────────────────────────────────────────────────────────────
class PlantBase(BaseModel):
    name:        str
    location:    Optional[str] = None
    country:     Optional[str] = None
    established: Optional[date] = None
    capacity:    Optional[int] = Field(None, ge=0)

class PlantCreate(PlantBase):
    plant_id: str = Field(..., min_length=2, max_length=10)

class PlantResponse(PlantBase, ORMBase):
    plant_id:   str
    created_at: datetime


# ─────────────────────────────────────────────────────────────
# ProductionLine
# ─────────────────────────────────────────────────────────────
class ProductionLineBase(BaseModel):
    name:              str
    plant_id:          Optional[str] = None
    line_type:         Optional[str] = None
    capacity_per_hour: Optional[int] = Field(None, ge=0)
    status:            str = "active"

class ProductionLineCreate(ProductionLineBase):
    line_id: str

class ProductionLineResponse(ProductionLineBase, ORMBase):
    line_id:    str
    created_at: datetime


# ─────────────────────────────────────────────────────────────
# Supplier
# ─────────────────────────────────────────────────────────────
class SupplierBase(BaseModel):
    name:         str
    country:      Optional[str] = None
    contact_name: Optional[str] = None
    email:        Optional[str] = None
    rating:       Optional[Decimal] = Field(None, ge=0, le=5)
    tier:         int = Field(1, ge=1, le=3)

class SupplierCreate(SupplierBase):
    supplier_id: str

class SupplierResponse(SupplierBase, ORMBase):
    supplier_id: str
    created_at:  datetime


# ─────────────────────────────────────────────────────────────
# Material
# ─────────────────────────────────────────────────────────────
class MaterialBase(BaseModel):
    name:           str
    category:       Optional[str] = None
    unit:           Optional[str] = None
    unit_cost:      Optional[Decimal] = Field(None, ge=0)
    lead_time_days: Optional[int] = Field(None, ge=0)
    supplier_id:    Optional[str] = None

class MaterialCreate(MaterialBase):
    material_id: str

class MaterialResponse(MaterialBase, ORMBase):
    material_id: str
    created_at:  datetime


# ─────────────────────────────────────────────────────────────
# Machine
# ─────────────────────────────────────────────────────────────
class MachineBase(BaseModel):
    name:              str
    machine_type:      Optional[str] = None
    plant_id:          Optional[str] = None
    line_id:           Optional[str] = None
    supplier_id:       Optional[str] = None
    manufacturer:      Optional[str] = None
    model_number:      Optional[str] = None
    installation_date: Optional[date] = None
    status:            str = "operational"

class MachineCreate(MachineBase):
    machine_id: str

class MachineResponse(MachineBase, ORMBase):
    machine_id: str
    created_at: datetime

class MachineDetail(MachineResponse):
    """Machine with related entity counts."""
    sensor_count:            int = 0
    maintenance_event_count: int = 0
    quality_event_count:     int = 0


# ─────────────────────────────────────────────────────────────
# Sensor
# ─────────────────────────────────────────────────────────────
class SensorBase(BaseModel):
    machine_id:    Optional[str] = None
    sensor_type:   Optional[str] = None
    unit:          Optional[str] = None
    min_threshold: Optional[Decimal] = None
    max_threshold: Optional[Decimal] = None
    location_tag:  Optional[str] = None
    status:        str = "active"

class SensorCreate(SensorBase):
    sensor_id: str

class SensorResponse(SensorBase, ORMBase):
    sensor_id:  str
    created_at: datetime


# ─────────────────────────────────────────────────────────────
# Employee
# ─────────────────────────────────────────────────────────────
class EmployeeBase(BaseModel):
    name:       str
    role:       Optional[str] = None
    department: Optional[str] = None
    plant_id:   Optional[str] = None
    email:      Optional[str] = None
    hire_date:  Optional[date] = None

class EmployeeCreate(EmployeeBase):
    employee_id: str

class EmployeeResponse(EmployeeBase, ORMBase):
    employee_id: str
    created_at:  datetime


# ─────────────────────────────────────────────────────────────
# ProductionOrder
# ─────────────────────────────────────────────────────────────
class ProductionOrderBase(BaseModel):
    product_name: str
    line_id:      Optional[str] = None
    plant_id:     Optional[str] = None
    quantity:     Optional[int] = Field(None, ge=0)
    start_date:   Optional[date] = None
    end_date:     Optional[date] = None
    status:       str = "planned"
    priority:     str = "normal"

class ProductionOrderCreate(ProductionOrderBase):
    order_id: str

class ProductionOrderResponse(ProductionOrderBase, ORMBase):
    order_id:   str
    created_at: datetime


# ─────────────────────────────────────────────────────────────
# MaintenanceEvent
# ─────────────────────────────────────────────────────────────
class MaintenanceEventBase(BaseModel):
    machine_id:     Optional[str] = None
    event_type:     Optional[str] = None
    description:    Optional[str] = None
    technician_id:  Optional[str] = None
    start_time:     Optional[datetime] = None
    end_time:       Optional[datetime] = None
    duration_hours: Optional[Decimal] = Field(None, ge=0)
    root_cause:     Optional[str] = None
    parts_replaced: Optional[str] = None
    cost:           Optional[Decimal] = Field(None, ge=0)

class MaintenanceEventCreate(MaintenanceEventBase):
    event_id: str

class MaintenanceEventResponse(MaintenanceEventBase, ORMBase):
    event_id:   str
    created_at: datetime


# ─────────────────────────────────────────────────────────────
# QualityEvent
# ─────────────────────────────────────────────────────────────
class QualityEventBase(BaseModel):
    order_id:        Optional[str] = None
    machine_id:      Optional[str] = None
    inspector_id:    Optional[str] = None
    inspection_type: Optional[str] = None
    result:          Optional[str] = None
    defect_type:     Optional[str] = None
    defect_count:    int = 0
    notes:           Optional[str] = None
    inspection_time: Optional[datetime] = None

class QualityEventCreate(QualityEventBase):
    quality_id: str

class QualityEventResponse(QualityEventBase, ORMBase):
    quality_id: str
    created_at: datetime


# ─────────────────────────────────────────────────────────────
# Telemetry
# ─────────────────────────────────────────────────────────────
class TelemetryBase(BaseModel):
    sensor_id:          Optional[str] = None
    machine_id:         Optional[str] = None
    value:              Decimal
    unit:               Optional[str] = None
    is_anomaly:         bool = False
    threshold_exceeded: bool = False
    recorded_at:        datetime

class TelemetryResponse(TelemetryBase, ORMBase):
    id:         int
    created_at: datetime


# ─────────────────────────────────────────────────────────────
# Generic response wrappers
# ─────────────────────────────────────────────────────────────
class PaginatedResponse(BaseModel):
    total:   int
    page:    int
    size:    int
    items:   list


class EntityStats(BaseModel):
    """High-level entity counts for the dashboard."""
    plants:             int
    production_lines:   int
    suppliers:          int
    materials:          int
    machines:           int
    sensors:            int
    employees:          int
    production_orders:  int
    maintenance_events: int
    quality_events:     int
    telemetry_records:  int
    total_entities:     int
