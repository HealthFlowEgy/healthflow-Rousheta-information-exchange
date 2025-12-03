"""
Unit tests for Egyptian models and validation
"""

import pytest
from src.models.egyptian_models import (
    validate_egyptian_national_id,
    validate_prescription_number,
    validate_eda_registration,
    EgyptianGovernorate,
    ControlledSubstanceSchedule
)


class TestEgyptianNationalIDValidation:
    """Test Egyptian National ID validation"""
    
    def test_valid_national_id(self):
        """Test valid National ID"""
        assert validate_egyptian_national_id("28501011234567") == True
        assert validate_egyptian_national_id("29012011234567") == True
        assert validate_egyptian_national_id("30101011234567") == True
    
    def test_invalid_length(self):
        """Test invalid length"""
        assert validate_egyptian_national_id("123") == False
        assert validate_egyptian_national_id("123456789012345") == False
    
    def test_invalid_format(self):
        """Test invalid format"""
        assert validate_egyptian_national_id("abcd1234567890") == False
        assert validate_egyptian_national_id("12-34-56-78-90-12") == False
    
    def test_invalid_century(self):
        """Test invalid century digit"""
        assert validate_egyptian_national_id("18501011234567") == False
        assert validate_egyptian_national_id("48501011234567") == False
    
    def test_invalid_governorate_code(self):
        """Test invalid governorate code"""
        assert validate_egyptian_national_id("28501010034567") == False  # 00 invalid
        assert validate_egyptian_national_id("28501013634567") == False  # 36 invalid


class TestPrescriptionNumberValidation:
    """Test prescription number validation"""
    
    def test_valid_prescription_number(self):
        """Test valid prescription numbers"""
        assert validate_prescription_number("RX-2025-ABC123") == True
        assert validate_prescription_number("RX-2024-XYZ789") == True
        assert validate_prescription_number("RX-2025-123456") == True
    
    def test_invalid_prefix(self):
        """Test invalid prefix"""
        assert validate_prescription_number("PX-2025-ABC123") == False
        assert validate_prescription_number("RX2025-ABC123") == False
    
    def test_invalid_year(self):
        """Test invalid year format"""
        assert validate_prescription_number("RX-25-ABC123") == False
        assert validate_prescription_number("RX-ABCD-ABC123") == False
    
    def test_invalid_sequence(self):
        """Test invalid sequence"""
        assert validate_prescription_number("RX-2025-") == False
        assert validate_prescription_number("RX-2025") == False


class TestEDARegistrationValidation:
    """Test EDA registration validation"""
    
    def test_valid_eda_registration(self):
        """Test valid EDA registration"""
        assert validate_eda_registration("EDA-MED-12345") == True
        assert validate_eda_registration("EDA-2025-001234") == True
    
    def test_invalid_eda_registration(self):
        """Test invalid EDA registration"""
        assert validate_eda_registration("") == False
        assert validate_eda_registration("ABC") == False


class TestEgyptianGovernorate:
    """Test Egyptian governorate enum"""
    
    def test_governorate_values(self):
        """Test governorate enum values"""
        assert EgyptianGovernorate.CAIRO.value == "cairo"
        assert EgyptianGovernorate.GIZA.value == "giza"
        assert EgyptianGovernorate.ALEXANDRIA.value == "alexandria"
    
    def test_governorate_count(self):
        """Test total number of governorates"""
        assert len(EgyptianGovernorate) == 27


class TestControlledSubstanceSchedule:
    """Test controlled substance schedule enum"""
    
    def test_schedule_values(self):
        """Test schedule enum values"""
        assert ControlledSubstanceSchedule.SCHEDULE_1.value == "schedule_1"
        assert ControlledSubstanceSchedule.SCHEDULE_5.value == "schedule_5"
        assert ControlledSubstanceSchedule.NOT_CONTROLLED.value == "not_controlled"
    
    def test_schedule_count(self):
        """Test total number of schedules"""
        assert len(ControlledSubstanceSchedule) == 6
