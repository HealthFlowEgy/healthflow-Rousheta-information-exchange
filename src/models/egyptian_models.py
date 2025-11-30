"""
Egyptian Healthcare Models
Data models specific to Egyptian healthcare system requirements
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal


class EgyptianGovernorate(Enum):
    """Egyptian Governorates"""
    CAIRO = "cairo"
    GIZA = "giza"
    ALEXANDRIA = "alexandria"
    DAKAHLIA = "dakahlia"
    RED_SEA = "red_sea"
    BEHEIRA = "beheira"
    FAYOUM = "fayoum"
    GHARBIA = "gharbia"
    ISMAILIA = "ismailia"
    MENOFIA = "menofia"
    MINYA = "minya"
    QALIUBIYA = "qaliubiya"
    NEW_VALLEY = "new_valley"
    SUEZ = "suez"
    ASWAN = "aswan"
    ASSIUT = "assiut"
    BENI_SUEF = "beni_suef"
    PORT_SAID = "port_said"
    DAMIETTA = "damietta"
    SHARKIA = "sharkia"
    SOUTH_SINAI = "south_sinai"
    KAFR_EL_SHEIKH = "kafr_el_sheikh"
    MATROUH = "matrouh"
    LUXOR = "luxor"
    QENA = "qena"
    NORTH_SINAI = "north_sinai"
    SOHAG = "sohag"


class ControlledSubstanceSchedule(Enum):
    """Egyptian controlled substance schedules"""
    SCHEDULE_1 = "schedule_1"  # Most restricted
    SCHEDULE_2 = "schedule_2"
    SCHEDULE_3 = "schedule_3"
    SCHEDULE_4 = "schedule_4"
    SCHEDULE_5 = "schedule_5"  # Least restricted
    NOT_CONTROLLED = "not_controlled"


@dataclass
class EgyptianDoctor:
    """Egyptian doctor/prescriber model"""
    national_id: str  # 14-digit Egyptian National ID
    syndicate_number: str  # Egyptian Medical Syndicate number (e.g., EMS-12345)
    eda_license: str  # Egyptian Drug Authority prescriber license
    full_name: str
    full_name_ar: str  # Arabic name
    specialty: str
    specialty_ar: str  # Arabic specialty
    governorate: EgyptianGovernorate
    phone: str
    email: Optional[str] = None


@dataclass
class EgyptianPatient:
    """Egyptian patient model"""
    national_id: str  # 14-digit Egyptian National ID
    full_name: str
    full_name_ar: str  # Arabic name
    date_of_birth: str  # ISO format
    gender: str  # male, female
    phone: str
    governorate: EgyptianGovernorate
    insurance_number: Optional[str] = None  # Egyptian health insurance


@dataclass
class EgyptianMedicine:
    """Egyptian medicine model"""
    eda_registration: str  # EDA registration number
    trade_name: str
    trade_name_ar: str  # Arabic trade name
    generic_name: str
    generic_name_ar: str  # Arabic generic name
    manufacturer: str
    manufacturer_ar: str
    public_price: Decimal  # EGP
    pharmacy_price: Decimal  # EGP
    is_controlled: bool
    control_schedule: ControlledSubstanceSchedule
    requires_prescription: bool
    form: str  # tablet, capsule, syrup, injection, etc.
    strength: str  # e.g., "500mg"


@dataclass
class EgyptianPrescriptionItem:
    """Single medication item in Egyptian prescription"""
    medicine_eda_registration: str
    medicine_trade_name: str
    medicine_trade_name_ar: str
    dosage: str  # e.g., "1 tablet"
    frequency: str  # e.g., "twice daily"
    frequency_ar: str  # Arabic frequency
    duration: str  # e.g., "7 days"
    quantity: int  # Number of units
    instructions: str
    instructions_ar: str  # Arabic instructions


@dataclass
class EgyptianPrescription:
    """
    Egyptian E-Prescription Model
    Follows Egyptian healthcare standards and EDA requirements
    """
    prescription_number: str  # Format: RX-2025-XXXXXX
    doctor: EgyptianDoctor
    patient: EgyptianPatient
    diagnosis: str
    diagnosis_ar: str  # Arabic diagnosis
    medications: List[EgyptianPrescriptionItem]
    prescription_date: str  # ISO format
    expiry_date: str  # ISO format
    notes: Optional[str] = None
    notes_ar: Optional[str] = None  # Arabic notes
    is_controlled_substance: bool = False
    requires_special_approval: bool = False
    digital_signature: Optional[str] = None  # Doctor's digital signature
    qr_code: Optional[str] = None  # QR code for verification


@dataclass
class EgyptianPharmacy:
    """Egyptian pharmacy model"""
    pharmacy_id: str
    pharmacy_name: str
    pharmacy_name_ar: str  # Arabic name
    license_number: str  # Egyptian pharmacy license
    syndicate_number: str  # Egyptian Pharmacists Syndicate number
    governorate: EgyptianGovernorate
    address: str
    address_ar: str  # Arabic address
    phone: str
    email: Optional[str] = None


@dataclass
class EgyptianPharmacist:
    """Egyptian pharmacist model"""
    national_id: str  # 14-digit Egyptian National ID
    syndicate_number: str  # Egyptian Pharmacists Syndicate number
    full_name: str
    full_name_ar: str  # Arabic name
    license_number: str
    phone: str
    email: Optional[str] = None


@dataclass
class EgyptianDispensation:
    """
    Egyptian Dispensation Record
    Records when a prescription is filled at a pharmacy
    """
    dispensation_id: str
    prescription_number: str  # RX-2025-XXXXXX
    pharmacy: EgyptianPharmacy
    pharmacist: EgyptianPharmacist
    dispense_date: str  # ISO format
    medications_dispensed: List[EgyptianPrescriptionItem]
    total_amount: Decimal  # Total cost in EGP
    patient_paid: Decimal  # Amount paid by patient in EGP
    insurance_covered: Decimal  # Amount covered by insurance in EGP
    notes: Optional[str] = None
    notes_ar: Optional[str] = None  # Arabic notes


@dataclass
class EgyptianRegulator:
    """Egyptian regulatory authority user"""
    regulator_id: str
    full_name: str
    full_name_ar: str
    authority: str  # e.g., "EDA", "Ministry of Health"
    role: str  # e.g., "inspector", "analyst", "administrator"
    governorate: Optional[EgyptianGovernorate] = None  # Regional regulators


# Validation functions

def validate_egyptian_national_id(national_id: str) -> bool:
    """
    Validate Egyptian National ID format
    
    Args:
        national_id: 14-digit national ID
    
    Returns:
        True if valid format
    """
    if not national_id or len(national_id) != 14:
        return False
    
    if not national_id.isdigit():
        return False
    
    # First digit should be 2 or 3 (century)
    if national_id[0] not in ['2', '3']:
        return False
    
    # Governorate code (positions 7-8) should be 01-35
    governorate_code = int(national_id[7:9])
    if governorate_code < 1 or governorate_code > 35:
        return False
    
    return True


def validate_prescription_number(prescription_number: str) -> bool:
    """
    Validate Egyptian prescription number format
    
    Args:
        prescription_number: Prescription number (RX-YYYY-XXXXXX)
    
    Returns:
        True if valid format
    """
    if not prescription_number:
        return False
    
    parts = prescription_number.split('-')
    if len(parts) != 3:
        return False
    
    if parts[0] != 'RX':
        return False
    
    # Year should be 4 digits
    if not parts[1].isdigit() or len(parts[1]) != 4:
        return False
    
    # Sequence should be alphanumeric
    if not parts[2].isalnum():
        return False
    
    return True


def validate_eda_registration(eda_registration: str) -> bool:
    """
    Validate EDA medicine registration number format
    
    Args:
        eda_registration: EDA registration number
    
    Returns:
        True if valid format
    """
    # EDA registration numbers typically follow a specific format
    # This is a placeholder - actual validation would depend on EDA standards
    if not eda_registration or len(eda_registration) < 5:
        return False
    
    return True
