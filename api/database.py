"""
Database Configuration and Models
SQLAlchemy models for PostgreSQL database
"""

from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://healthflow:healthflow@localhost:5432/healthflow_epx"
)

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency for FastAPI
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# DATABASE MODELS
# ============================================================================

class Prescription(Base):
    """Prescription model"""
    __tablename__ = "prescriptions"
    
    id = Column(String(36), primary_key=True)
    prescription_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Doctor information
    doctor_id = Column(String(14), nullable=False, index=True)
    doctor_syndicate_number = Column(String(50), nullable=False)
    doctor_eda_license = Column(String(50), nullable=False)
    doctor_name = Column(String(200), nullable=False)
    doctor_name_ar = Column(String(200))
    
    # Patient information
    patient_id = Column(String(14), nullable=False, index=True)
    patient_name = Column(String(200), nullable=False)
    patient_name_ar = Column(String(200))
    
    # Prescription details
    diagnosis = Column(Text, nullable=False)
    diagnosis_ar = Column(Text)
    medications = Column(JSON, nullable=False)  # List of medication items
    
    # Dates
    prescription_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    status = Column(String(50), nullable=False, default="active", index=True)
    
    # Additional fields
    notes = Column(Text)
    notes_ar = Column(Text)
    is_controlled_substance = Column(Boolean, default=False)
    requires_special_approval = Column(Boolean, default=False)
    digital_signature = Column(Text)
    qr_code = Column(Text)
    
    # Relationships
    dispensations = relationship("Dispensation", back_populates="prescription")
    audit_logs = relationship("AuditLog", back_populates="prescription")
    
    # Indexes
    __table_args__ = (
        Index('idx_prescription_doctor', 'doctor_id'),
        Index('idx_prescription_patient', 'patient_id'),
        Index('idx_prescription_date', 'prescription_date'),
        Index('idx_prescription_status', 'status'),
    )


class Dispensation(Base):
    """Dispensation model"""
    __tablename__ = "dispensations"
    
    id = Column(String(36), primary_key=True)
    prescription_id = Column(String(36), ForeignKey("prescriptions.id"), nullable=False, index=True)
    prescription_number = Column(String(50), nullable=False, index=True)
    
    # Pharmacy information
    pharmacy_id = Column(String(50), nullable=False, index=True)
    pharmacy_name = Column(String(200), nullable=False)
    pharmacy_name_ar = Column(String(200))
    pharmacy_license = Column(String(50), nullable=False)
    
    # Pharmacist information
    pharmacist_id = Column(String(14), nullable=False, index=True)
    pharmacist_name = Column(String(200), nullable=False)
    pharmacist_name_ar = Column(String(200))
    pharmacist_license = Column(String(50), nullable=False)
    
    # Dispensation details
    medications_dispensed = Column(JSON, nullable=False)
    dispense_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Financial information
    total_amount = Column(Float, nullable=False)
    patient_paid = Column(Float, nullable=False)
    insurance_covered = Column(Float, nullable=False)
    
    # Additional fields
    notes = Column(Text)
    notes_ar = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    prescription = relationship("Prescription", back_populates="dispensations")
    
    # Indexes
    __table_args__ = (
        Index('idx_dispensation_pharmacy', 'pharmacy_id'),
        Index('idx_dispensation_pharmacist', 'pharmacist_id'),
        Index('idx_dispensation_date', 'dispense_date'),
    )


class Doctor(Base):
    """Doctor model"""
    __tablename__ = "doctors"
    
    id = Column(String(36), primary_key=True)
    national_id = Column(String(14), unique=True, nullable=False, index=True)
    syndicate_number = Column(String(50), unique=True, nullable=False, index=True)
    eda_license = Column(String(50), unique=True, nullable=False)
    
    # Personal information
    full_name = Column(String(200), nullable=False)
    full_name_ar = Column(String(200))
    specialty = Column(String(100), nullable=False)
    specialty_ar = Column(String(100))
    
    # Contact information
    phone = Column(String(20), nullable=False)
    email = Column(String(100))
    
    # Location
    governorate = Column(String(50), nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class Patient(Base):
    """Patient model"""
    __tablename__ = "patients"
    
    id = Column(String(36), primary_key=True)
    national_id = Column(String(14), unique=True, nullable=False, index=True)
    
    # Personal information
    full_name = Column(String(200), nullable=False)
    full_name_ar = Column(String(200))
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(String(10), nullable=False)
    
    # Contact information
    phone = Column(String(20), nullable=False)
    
    # Location
    governorate = Column(String(50), nullable=False)
    
    # Insurance
    insurance_number = Column(String(50))
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class Pharmacy(Base):
    """Pharmacy model"""
    __tablename__ = "pharmacies"
    
    id = Column(String(36), primary_key=True)
    pharmacy_id = Column(String(50), unique=True, nullable=False, index=True)
    license_number = Column(String(50), unique=True, nullable=False)
    syndicate_number = Column(String(50), unique=True, nullable=False)
    
    # Information
    pharmacy_name = Column(String(200), nullable=False)
    pharmacy_name_ar = Column(String(200))
    
    # Location
    governorate = Column(String(50), nullable=False, index=True)
    address = Column(Text, nullable=False)
    address_ar = Column(Text)
    
    # Contact
    phone = Column(String(20), nullable=False)
    email = Column(String(100))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class Medicine(Base):
    """Medicine model"""
    __tablename__ = "medicines"
    
    id = Column(String(36), primary_key=True)
    eda_registration = Column(String(50), unique=True, nullable=False, index=True)
    
    # Names
    trade_name = Column(String(200), nullable=False)
    trade_name_ar = Column(String(200))
    generic_name = Column(String(200), nullable=False)
    generic_name_ar = Column(String(200))
    
    # Manufacturer
    manufacturer = Column(String(200), nullable=False)
    manufacturer_ar = Column(String(200))
    
    # Pricing (EGP)
    public_price = Column(Float, nullable=False)
    pharmacy_price = Column(Float, nullable=False)
    
    # Classification
    is_controlled = Column(Boolean, default=False)
    control_schedule = Column(String(20))
    requires_prescription = Column(Boolean, default=True)
    
    # Form and strength
    form = Column(String(50), nullable=False)  # tablet, capsule, syrup, etc.
    strength = Column(String(50), nullable=False)  # e.g., "500mg"
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    """Audit log model"""
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True)
    
    # Entity information
    entity_type = Column(String(50), nullable=False, index=True)
    entity_id = Column(String(50), nullable=False, index=True)
    
    # Action
    action = Column(String(50), nullable=False, index=True)
    
    # Actor
    actor_id = Column(String(50), nullable=False, index=True)
    actor_type = Column(String(50), nullable=False)
    
    # Details
    details = Column(JSON)
    
    # Timestamp
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Relationships
    prescription_id = Column(String(36), ForeignKey("prescriptions.id"), nullable=True)
    prescription = relationship("Prescription", back_populates="audit_logs")
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_entity', 'entity_type', 'entity_id'),
        Index('idx_audit_actor', 'actor_type', 'actor_id'),
        Index('idx_audit_timestamp', 'timestamp'),
    )


class SubmissionLog(Base):
    """Prescription submission log"""
    __tablename__ = "submission_logs"
    
    id = Column(String(36), primary_key=True)
    submission_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Submission details
    prescription_number = Column(String(50), nullable=False, index=True)
    submitter_id = Column(String(50), nullable=False)
    submitter_type = Column(String(50), nullable=False)
    
    # Status
    status = Column(String(50), nullable=False, default="pending", index=True)
    format = Column(String(20), nullable=False)
    
    # Validation
    validation_errors = Column(JSON)
    
    # Timestamps
    submitted_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    processed_at = Column(DateTime)
    
    # Indexes
    __table_args__ = (
        Index('idx_submission_status', 'status'),
        Index('idx_submission_date', 'submitted_at'),
    )


# Create all tables
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully!")
