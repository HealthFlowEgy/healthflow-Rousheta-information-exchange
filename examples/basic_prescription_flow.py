"""
Example: Basic Prescription Flow
Demonstrates creating a prescription using NCPDP SCRIPT and converting to FHIR
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from prescribing.eprescribing_service import (
    NCPDPScriptBuilder,
    Prescriber,
    Patient,
    Medication,
    Pharmacy
)

from integrations.fhir_integration import FHIRResourceBuilder


def create_ncpdp_prescription():
    """Create a prescription using NCPDP SCRIPT standard"""
    
    print("=" * 80)
    print("NCPDP SCRIPT Prescription Creation Example")
    print("=" * 80)
    
    # Initialize builder
    builder = NCPDPScriptBuilder()
    
    # Create prescriber
    prescriber = Prescriber(
        npi="1234567890",
        dea="AB1234563",
        state_license="MD12345",
        first_name="John",
        last_name="Smith",
        phone="5551234567",
        fax="5551234568",
        address_line1="123 Medical Plaza",
        city="Boston",
        state="MA",
        zip_code="02101",
        email="dr.smith@example.com"
    )
    
    # Create patient
    patient = Patient(
        first_name="Jane",
        last_name="Doe",
        dob="19800115",
        gender="F",
        address_line1="456 Main St",
        city="Boston",
        state="MA",
        zip_code="02101",
        phone="5559876543",
        email="jane.doe@example.com"
    )
    
    # Create medication
    medication = Medication(
        drug_description="Lisinopril 10mg Tablet",
        drug_coded="00093314501",  # NDC code
        quantity=30.0,
        quantity_qualifier="C38288",  # Each
        days_supply=30,
        refills=3,
        substitutions="1",  # Substitution allowed
        sig="Take 1 tablet by mouth once daily",
        note="For blood pressure control",
        diagnosis="I10"  # ICD-10 for Essential Hypertension
    )
    
    # Create pharmacy
    pharmacy = Pharmacy(
        ncpdp_id="1234567",
        npi="9876543210",
        name="CVS Pharmacy #1234",
        address_line1="789 Pharmacy Ave",
        city="Boston",
        state="MA",
        zip_code="02101",
        phone="5551112222",
        fax="5551112223"
    )
    
    # Build NewRx message
    print("\nBuilding NEWRX message...")
    newrx_xml = builder.build_newrx(
        prescriber=prescriber,
        patient=patient,
        medication=medication,
        pharmacy=pharmacy,
        written_date="20250130"
    )
    
    print("\nGenerated NCPDP SCRIPT XML:")
    print("-" * 80)
    print(newrx_xml[:500] + "..." if len(newrx_xml) > 500 else newrx_xml)
    print("-" * 80)
    
    return {
        "prescriber": prescriber,
        "patient": patient,
        "medication": medication,
        "pharmacy": pharmacy
    }


def create_fhir_prescription(data):
    """Convert prescription to FHIR format"""
    
    print("\n" + "=" * 80)
    print("FHIR R4 MedicationRequest Creation Example")
    print("=" * 80)
    
    # Initialize FHIR builder
    fhir_builder = FHIRResourceBuilder(organization_id="healthflow-org")
    
    # Build Patient resource
    print("\nBuilding FHIR Patient resource...")
    patient = fhir_builder.build_patient_resource(
        patient_id="patient-123",
        first_name=data["patient"].first_name,
        last_name=data["patient"].last_name,
        dob="1980-01-15",
        gender="female",
        phone=data["patient"].phone,
        email=data["patient"].email,
        address={
            "street": data["patient"].address_line1,
            "city": data["patient"].city,
            "state": data["patient"].state,
            "zip": data["patient"].zip_code
        }
    )
    
    # Build Practitioner resource
    print("Building FHIR Practitioner resource...")
    practitioner = fhir_builder.build_practitioner_resource(
        practitioner_id="practitioner-456",
        first_name=data["prescriber"].first_name,
        last_name=data["prescriber"].last_name,
        npi=data["prescriber"].npi,
        specialty="Cardiology",
        phone=data["prescriber"].phone
    )
    
    # Build MedicationRequest
    print("Building FHIR MedicationRequest resource...")
    med_request = fhir_builder.build_medication_request(
        request_id="prescription-789",
        patient_reference="Patient/patient-123",
        practitioner_reference="Practitioner/practitioner-456",
        medication_name=data["medication"].drug_description,
        medication_code="314076",  # RxNorm code for Lisinopril 10mg
        dosage_instruction=data["medication"].sig,
        quantity=int(data["medication"].quantity),
        refills=data["medication"].refills,
        notes=data["medication"].note
    )
    
    print("\nGenerated FHIR MedicationRequest:")
    print("-" * 80)
    fhir_json = med_request.json(indent=2)
    print(fhir_json[:500] + "..." if len(fhir_json) > 500 else fhir_json)
    print("-" * 80)
    
    return {
        "patient": patient,
        "practitioner": practitioner,
        "medication_request": med_request
    }


def main():
    """Run the complete example"""
    
    print("\n" + "=" * 80)
    print("HealthFlow Information Exchange - Basic Prescription Flow Example")
    print("=" * 80)
    
    # Step 1: Create NCPDP prescription
    prescription_data = create_ncpdp_prescription()
    
    # Step 2: Convert to FHIR
    fhir_resources = create_fhir_prescription(prescription_data)
    
    print("\n" + "=" * 80)
    print("Example completed successfully!")
    print("=" * 80)
    print("\nThis example demonstrated:")
    print("1. Creating a prescription using NCPDP SCRIPT standard")
    print("2. Converting prescription data to FHIR R4 format")
    print("3. Building Patient, Practitioner, and MedicationRequest resources")
    print("\nFor more examples, see the examples/ directory")
    print("=" * 80)


if __name__ == "__main__":
    main()
