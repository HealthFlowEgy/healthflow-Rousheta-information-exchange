"""
Pytest configuration and fixtures
"""

import pytest
from datetime import datetime, timedelta
from typing import Dict
import uuid


@pytest.fixture
def sample_egyptian_doctor() -> Dict:
    """Sample Egyptian doctor data"""
    return {
        "national_id": "28501011234567",
        "syndicate_number": "EMS-12345",
        "eda_license": "EDA-2025-001234",
        "full_name": "Dr. Ahmed Mohamed",
        "full_name_ar": "د. أحمد محمد",
        "specialty": "Cardiology",
        "specialty_ar": "أمراض القلب",
        "governorate": "cairo",
        "phone": "+201234567890",
        "email": "ahmed.mohamed@example.com"
    }


@pytest.fixture
def sample_egyptian_patient() -> Dict:
    """Sample Egyptian patient data"""
    return {
        "national_id": "29012011234567",
        "full_name": "Mohamed Ali",
        "full_name_ar": "محمد علي",
        "date_of_birth": "1990-01-20",
        "gender": "male",
        "phone": "+201234567891",
        "governorate": "cairo",
        "insurance_number": "INS-123456"
    }


@pytest.fixture
def sample_medication() -> Dict:
    """Sample medication item"""
    return {
        "medicine_eda_registration": "EDA-MED-12345",
        "medicine_trade_name": "Aspirin 100mg",
        "medicine_trade_name_ar": "أسبرين 100 ملجم",
        "dosage": "1 tablet",
        "frequency": "once daily",
        "frequency_ar": "مرة واحدة يوميا",
        "duration": "30 days",
        "quantity": 30,
        "instructions": "Take with food",
        "instructions_ar": "يؤخذ مع الطعام"
    }


@pytest.fixture
def sample_prescription(sample_egyptian_doctor, sample_egyptian_patient, sample_medication) -> Dict:
    """Sample prescription data"""
    return {
        "prescription_number": f"RX-2025-{uuid.uuid4().hex[:6].upper()}",
        "doctor_id": sample_egyptian_doctor["national_id"],
        "doctor_syndicate_number": sample_egyptian_doctor["syndicate_number"],
        "doctor_eda_license": sample_egyptian_doctor["eda_license"],
        "patient_id": sample_egyptian_patient["national_id"],
        "diagnosis": "Hypertension",
        "diagnosis_ar": "ارتفاع ضغط الدم",
        "medications": [sample_medication],
        "prescription_date": datetime.utcnow().isoformat(),
        "expiry_date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "notes": "Monitor blood pressure regularly",
        "notes_ar": "مراقبة ضغط الدم بانتظام"
    }


@pytest.fixture
def sample_pharmacy() -> Dict:
    """Sample pharmacy data"""
    return {
        "pharmacy_id": "PHARM-001",
        "pharmacy_name": "Cairo Central Pharmacy",
        "pharmacy_name_ar": "صيدلية القاهرة المركزية",
        "license_number": "EPL-12345",
        "syndicate_number": "EPS-54321",
        "governorate": "cairo",
        "address": "123 Tahrir Square, Cairo",
        "address_ar": "123 ميدان التحرير، القاهرة",
        "phone": "+201234567892",
        "email": "info@cairopharmacy.com"
    }


@pytest.fixture
def sample_pharmacist() -> Dict:
    """Sample pharmacist data"""
    return {
        "national_id": "28701011234567",
        "syndicate_number": "EPS-67890",
        "full_name": "Sara Hassan",
        "full_name_ar": "سارة حسن",
        "license_number": "EPL-67890",
        "phone": "+201234567893",
        "email": "sara.hassan@example.com"
    }


@pytest.fixture
def sample_dispensation(sample_prescription, sample_pharmacy, sample_pharmacist, sample_medication) -> Dict:
    """Sample dispensation data"""
    return {
        "prescription_tx_id": sample_prescription["prescription_number"],
        "pharmacy_id": sample_pharmacy["pharmacy_id"],
        "pharmacy_name": sample_pharmacy["pharmacy_name"],
        "pharmacy_license": sample_pharmacy["license_number"],
        "pharmacist_id": sample_pharmacist["national_id"],
        "pharmacist_name": sample_pharmacist["full_name"],
        "pharmacist_license": sample_pharmacist["license_number"],
        "medications_dispensed": [sample_medication],
        "total_amount": 150.00,
        "patient_paid": 50.00,
        "insurance_covered": 100.00,
        "notes": "Patient counseled on medication usage"
    }


@pytest.fixture
def sample_regulator() -> Dict:
    """Sample regulator data"""
    return {
        "regulator_id": "REG-001",
        "full_name": "Dr. Fatma Ibrahim",
        "full_name_ar": "د. فاطمة إبراهيم",
        "authority": "EDA",
        "role": "inspector"
    }
