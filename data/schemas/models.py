"""
SQLAlchemy ORM models for the enterprise manufacturing database.
Maps all 10 tables defined in scripts/init_db.sql.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import (
    BigInteger, Boolean, Column, Date, DateTime, ForeignKey,
    Integer, Numeric, String, Text, func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


# ─────────────────────────────────────────────────────────────
# Plant
# ─────────────────────────────────────────────────────────────
class Plant(Base):
    __tablename__ = "plants"

    plant_id:    Mapped[str]           = mapped_column(String(10), primary_key=True)
    name:        Mapped[str]           = mapped_column(String(100), nullable=False)
    location:    Mapped[Optional[str]] = mapped_column(String(100))
    country:     Mapped[Optional[str]] = mapped_column(String(50))
    established: Mapped[Optional[date]] = mapped_column(Date)
    capacity:    Mapped[Optional[int]]  = mapped_column(Integer)
    created_at:  Mapped[datetime]       = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    production_lines: Mapped[List["ProductionLine"]] = relationship(back_populates="plant")
    machines:         Mapped[List["Machine"]]         = relationship(back_populates="plant")
    employees:        Mapped[List["Employee"]]         = relationship(back_populates="plant")

    def __repr__(self) -> str:
        return f"<Plant {self.plant_id}: {self.name}>"


# ─────────────────────────────────────────────────────────────
# ProductionLine
# ─────────────────────────────────────────────────────────────
class ProductionLine(Base):
    __tablename__ = "production_lines"

    line_id:           Mapped[str]           = mapped_column(String(10), primary_key=True)
    name:              Mapped[str]           = mapped_column(String(100), nullable=False)
    plant_id:          Mapped[Optional[str]] = mapped_column(ForeignKey("plants.plant_id"))
    line_type:         Mapped[Optional[str]] = mapped_column(String(50))
    capacity_per_hour: Mapped[Optional[int]] = mapped_column(Integer)
    status:            Mapped[str]           = mapped_column(String(20), default="active")
    created_at:        Mapped[datetime]      = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    plant:             Mapped[Optional["Plant"]]          = relationship(back_populates="production_lines")
    machines:          Mapped[List["Machine"]]             = relationship(back_populates="line")
    production_orders: Mapped[List["ProductionOrder"]]    = relationship(back_populates="line")

    def __repr__(self) -> str:
        return f"<ProductionLine {self.line_id}: {self.name}>"


# ─────────────────────────────────────────────────────────────
# Supplier
# ─────────────────────────────────────────────────────────────
class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id:  Mapped[str]             = mapped_column(String(10), primary_key=True)
    name:         Mapped[str]             = mapped_column(String(100), nullable=False)
    country:      Mapped[Optional[str]]   = mapped_column(String(50))
    contact_name: Mapped[Optional[str]]   = mapped_column(String(100))
    email:        Mapped[Optional[str]]   = mapped_column(String(150))
    rating:       Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 1))
    tier:         Mapped[int]             = mapped_column(Integer, default=1)
    created_at:   Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    machines:   Mapped[List["Machine"]]  = relationship(back_populates="supplier")
    materials:  Mapped[List["Material"]] = relationship(back_populates="supplier")

    def __repr__(self) -> str:
        return f"<Supplier {self.supplier_id}: {self.name}>"


# ─────────────────────────────────────────────────────────────
# Material
# ─────────────────────────────────────────────────────────────
class Material(Base):
    __tablename__ = "materials"

    material_id:    Mapped[str]             = mapped_column(String(10), primary_key=True)
    name:           Mapped[str]             = mapped_column(String(100), nullable=False)
    category:       Mapped[Optional[str]]   = mapped_column(String(50))
    unit:           Mapped[Optional[str]]   = mapped_column(String(20))
    unit_cost:      Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    lead_time_days: Mapped[Optional[int]]   = mapped_column(Integer)
    supplier_id:    Mapped[Optional[str]]   = mapped_column(ForeignKey("suppliers.supplier_id"))
    created_at:     Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    supplier: Mapped[Optional["Supplier"]] = relationship(back_populates="materials")

    def __repr__(self) -> str:
        return f"<Material {self.material_id}: {self.name}>"


# ─────────────────────────────────────────────────────────────
# Machine
# ─────────────────────────────────────────────────────────────
class Machine(Base):
    __tablename__ = "machines"

    machine_id:        Mapped[str]           = mapped_column(String(10), primary_key=True)
    name:              Mapped[str]           = mapped_column(String(100), nullable=False)
    machine_type:      Mapped[Optional[str]] = mapped_column(String(50))
    plant_id:          Mapped[Optional[str]] = mapped_column(ForeignKey("plants.plant_id"))
    line_id:           Mapped[Optional[str]] = mapped_column(ForeignKey("production_lines.line_id"))
    supplier_id:       Mapped[Optional[str]] = mapped_column(ForeignKey("suppliers.supplier_id"))
    manufacturer:      Mapped[Optional[str]] = mapped_column(String(100))
    model_number:      Mapped[Optional[str]] = mapped_column(String(50))
    installation_date: Mapped[Optional[date]] = mapped_column(Date)
    status:            Mapped[str]           = mapped_column(String(20), default="operational")
    created_at:        Mapped[datetime]      = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    plant:              Mapped[Optional["Plant"]]            = relationship(back_populates="machines")
    line:               Mapped[Optional["ProductionLine"]]   = relationship(back_populates="machines")
    supplier:           Mapped[Optional["Supplier"]]         = relationship(back_populates="machines")
    sensors:            Mapped[List["Sensor"]]               = relationship(back_populates="machine")
    maintenance_events: Mapped[List["MaintenanceEvent"]]     = relationship(back_populates="machine")
    quality_events:     Mapped[List["QualityEvent"]]         = relationship(back_populates="machine")
    telemetry:          Mapped[List["Telemetry"]]            = relationship(back_populates="machine")

    def __repr__(self) -> str:
        return f"<Machine {self.machine_id}: {self.name} ({self.machine_type})>"


# ─────────────────────────────────────────────────────────────
# Sensor
# ─────────────────────────────────────────────────────────────
class Sensor(Base):
    __tablename__ = "sensors"

    sensor_id:    Mapped[str]             = mapped_column(String(10), primary_key=True)
    machine_id:   Mapped[Optional[str]]   = mapped_column(ForeignKey("machines.machine_id"))
    sensor_type:  Mapped[Optional[str]]   = mapped_column(String(50))
    unit:         Mapped[Optional[str]]   = mapped_column(String(20))
    min_threshold: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 3))
    max_threshold: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 3))
    location_tag: Mapped[Optional[str]]   = mapped_column(String(50))
    status:       Mapped[str]             = mapped_column(String(20), default="active")
    created_at:   Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    machine:   Mapped[Optional["Machine"]] = relationship(back_populates="sensors")
    telemetry: Mapped[List["Telemetry"]]   = relationship(back_populates="sensor")

    def __repr__(self) -> str:
        return f"<Sensor {self.sensor_id}: {self.sensor_type} on {self.machine_id}>"


# ─────────────────────────────────────────────────────────────
# Employee
# ─────────────────────────────────────────────────────────────
class Employee(Base):
    __tablename__ = "employees"

    employee_id: Mapped[str]           = mapped_column(String(10), primary_key=True)
    name:        Mapped[str]           = mapped_column(String(100), nullable=False)
    role:        Mapped[Optional[str]] = mapped_column(String(50))
    department:  Mapped[Optional[str]] = mapped_column(String(50))
    plant_id:    Mapped[Optional[str]] = mapped_column(ForeignKey("plants.plant_id"))
    email:       Mapped[Optional[str]] = mapped_column(String(150))
    hire_date:   Mapped[Optional[date]] = mapped_column(Date)
    created_at:  Mapped[datetime]      = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    plant:              Mapped[Optional["Plant"]]        = relationship(back_populates="employees")
    maintenance_events: Mapped[List["MaintenanceEvent"]] = relationship(back_populates="technician")
    quality_events:     Mapped[List["QualityEvent"]]     = relationship(back_populates="inspector")

    def __repr__(self) -> str:
        return f"<Employee {self.employee_id}: {self.name} ({self.role})>"


# ─────────────────────────────────────────────────────────────
# ProductionOrder
# ─────────────────────────────────────────────────────────────
class ProductionOrder(Base):
    __tablename__ = "production_orders"

    order_id:     Mapped[str]           = mapped_column(String(15), primary_key=True)
    product_name: Mapped[str]           = mapped_column(String(100), nullable=False)
    line_id:      Mapped[Optional[str]] = mapped_column(ForeignKey("production_lines.line_id"))
    plant_id:     Mapped[Optional[str]] = mapped_column(ForeignKey("plants.plant_id"))
    quantity:     Mapped[Optional[int]] = mapped_column(Integer)
    start_date:   Mapped[Optional[date]] = mapped_column(Date)
    end_date:     Mapped[Optional[date]] = mapped_column(Date)
    status:       Mapped[str]           = mapped_column(String(20), default="planned")
    priority:     Mapped[str]           = mapped_column(String(10), default="normal")
    created_at:   Mapped[datetime]      = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    line:           Mapped[Optional["ProductionLine"]] = relationship(back_populates="production_orders")
    quality_events: Mapped[List["QualityEvent"]]       = relationship(back_populates="order")

    def __repr__(self) -> str:
        return f"<ProductionOrder {self.order_id}: {self.product_name}>"


# ─────────────────────────────────────────────────────────────
# MaintenanceEvent
# ─────────────────────────────────────────────────────────────
class MaintenanceEvent(Base):
    __tablename__ = "maintenance_events"

    event_id:       Mapped[str]             = mapped_column(String(15), primary_key=True)
    machine_id:     Mapped[Optional[str]]   = mapped_column(ForeignKey("machines.machine_id"))
    event_type:     Mapped[Optional[str]]   = mapped_column(String(30))
    description:    Mapped[Optional[str]]   = mapped_column(Text)
    technician_id:  Mapped[Optional[str]]   = mapped_column(ForeignKey("employees.employee_id"))
    start_time:     Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    end_time:       Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    duration_hours: Mapped[Optional[Decimal]]  = mapped_column(Numeric(5, 2))
    root_cause:     Mapped[Optional[str]]   = mapped_column(String(200))
    parts_replaced: Mapped[Optional[str]]   = mapped_column(String(200))
    cost:           Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    created_at:     Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    machine:    Mapped[Optional["Machine"]]  = relationship(back_populates="maintenance_events")
    technician: Mapped[Optional["Employee"]] = relationship(back_populates="maintenance_events")

    def __repr__(self) -> str:
        return f"<MaintenanceEvent {self.event_id}: {self.event_type} on {self.machine_id}>"


# ─────────────────────────────────────────────────────────────
# QualityEvent
# ─────────────────────────────────────────────────────────────
class QualityEvent(Base):
    __tablename__ = "quality_events"

    quality_id:      Mapped[str]           = mapped_column(String(15), primary_key=True)
    order_id:        Mapped[Optional[str]] = mapped_column(ForeignKey("production_orders.order_id"))
    machine_id:      Mapped[Optional[str]] = mapped_column(ForeignKey("machines.machine_id"))
    inspector_id:    Mapped[Optional[str]] = mapped_column(ForeignKey("employees.employee_id"))
    inspection_type: Mapped[Optional[str]] = mapped_column(String(30))
    result:          Mapped[Optional[str]] = mapped_column(String(20))
    defect_type:     Mapped[Optional[str]] = mapped_column(String(100))
    defect_count:    Mapped[int]           = mapped_column(Integer, default=0)
    notes:           Mapped[Optional[str]] = mapped_column(Text)
    inspection_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at:      Mapped[datetime]      = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    machine:   Mapped[Optional["Machine"]]          = relationship(back_populates="quality_events")
    order:     Mapped[Optional["ProductionOrder"]]  = relationship(back_populates="quality_events")
    inspector: Mapped[Optional["Employee"]]         = relationship(back_populates="quality_events")

    def __repr__(self) -> str:
        return f"<QualityEvent {self.quality_id}: {self.result} ({self.inspection_type})>"


# ─────────────────────────────────────────────────────────────
# Telemetry
# ─────────────────────────────────────────────────────────────
class Telemetry(Base):
    __tablename__ = "telemetry"

    id:                  Mapped[int]           = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sensor_id:           Mapped[Optional[str]] = mapped_column(ForeignKey("sensors.sensor_id"))
    machine_id:          Mapped[Optional[str]] = mapped_column(ForeignKey("machines.machine_id"))
    value:               Mapped[Decimal]       = mapped_column(Numeric(12, 4), nullable=False)
    unit:                Mapped[Optional[str]] = mapped_column(String(20))
    is_anomaly:          Mapped[bool]          = mapped_column(Boolean, default=False)
    threshold_exceeded:  Mapped[bool]          = mapped_column(Boolean, default=False)
    recorded_at:         Mapped[datetime]      = mapped_column(DateTime(timezone=True), nullable=False)
    created_at:          Mapped[datetime]      = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    sensor:  Mapped[Optional["Sensor"]]  = relationship(back_populates="telemetry")
    machine: Mapped[Optional["Machine"]] = relationship(back_populates="telemetry")

    def __repr__(self) -> str:
        return f"<Telemetry sensor={self.sensor_id} value={self.value} at={self.recorded_at}>"
