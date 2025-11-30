# HealthFlow Information Exchange

A dedicated library for healthcare information exchange functions supporting prescribing, dispensing, and regulatory oversight operations. This repository contains only the core information exchange logic without any portal or UI components.

## Overview

The HealthFlow Information Exchange library provides standardized interfaces and implementations for:

- **Prescribing Functions**: Electronic prescription creation, modification, and transmission
- **Dispensing Functions**: Pharmacy routing, prescription tracking, and fulfillment
- **Regulator Functions**: Read-only access to prescription and dispensation data for regulatory oversight
- **Analytics Functions**: Advanced analytics, reporting, and ML-powered insights
- **Integration Standards**: FHIR R4, HL7 v2.x, NCPDP SCRIPT, and EHR integrations

## Architecture

```
healthflow-information-exchange/
├── src/
│   ├── prescribing/          # E-prescribing services
│   │   └── eprescribing_service.py
│   ├── dispensing/           # Pharmacy and dispensing services
│   │   ├── pharmacy_routing_service.py
│   │   └── prescription_tracking_service.py
│   ├── regulator/            # Regulatory oversight APIs
│   │   └── regulator_api.py
│   ├── analytics/            # Analytics and reporting services
│   │   ├── analytics_service.py
│   │   ├── analytics_engine.py
│   │   └── reporting_service.py
│   ├── integrations/         # Healthcare standards integrations
│   │   ├── fhir_integration.py
│   │   ├── hl7_integration.py
│   │   └── ehr_integration.py
│   ├── models/               # Data models and schemas
│   ├── utils/                # Utility functions
│   └── __init__.py
├── docs/                     # Documentation
├── tests/                    # Unit and integration tests
├── examples/                 # Usage examples
└── README.md
```

## Features

### Prescribing Module

- **NCPDP SCRIPT Support**: Full implementation of NCPDP SCRIPT 2017071 standard
  - NewRx (New Prescription)
  - RxChange (Prescription Change)
  - RxFill (Fill Notification)
  - Status Messages
  - Error Messages
  - Refill Requests/Responses
  - Cancellation

- **Prescription Management**:
  - Create and validate prescriptions
  - Modify existing prescriptions
  - Track prescription status
  - Handle controlled substances

### Dispensing Module

- **Pharmacy Network Management**:
  - Pharmacy directory and lookup
  - Network routing (Surescripts, Direct, Retail Chain, Mail Order, Specialty)
  - Geographic-based pharmacy search
  - Pharmacy availability and status tracking

- **Prescription Tracking**:
  - Real-time prescription status updates
  - Fill notifications
  - Pickup tracking
  - Patient notifications

### Regulator Module

- **Read-Only Access APIs**:
  - Query prescriptions by various filters
  - Access dispensation records
  - Generate statistics and reports
  - Audit trail logging

- **Data Access**:
  - Prescription records with full metadata
  - Dispensation records with pharmacist information
  - Doctor and pharmacy activity tracking
  - Compliance monitoring

### Analytics Module

- **Prescription Analytics**:
  - Volume metrics and trends
  - Accuracy and quality metrics
  - Performance analysis
  - Error pattern detection

- **ML-Powered Analytics**:
  - Adverse event pattern detection
  - Safety signal identification
  - Anomaly detection
  - Risk prediction and scoring

- **Comprehensive Reporting**:
  - Prescription volume reports
  - Dispensation activity reports
  - Provider and pharmacy performance
  - Compliance and quality metrics
  - Regulatory overview reports

### Integration Module

- **FHIR R4 Integration**:
  - MedicationRequest resources
  - Patient resources
  - Practitioner resources
  - Organization resources
  - Bundle creation and parsing

- **HL7 v2.x Integration**:
  - RDE^O11 (Pharmacy/Treatment Encoded Order)
  - ACK (General Acknowledgment)
  - Message parsing and validation

- **EHR Integration**:
  - Standardized EHR connectivity
  - Patient data synchronization
  - Clinical data exchange

## Standards Compliance

This library implements the following healthcare interoperability standards:

- **NCPDP SCRIPT 2017071**: Electronic prescribing standard
- **HL7 FHIR R4**: Fast Healthcare Interoperability Resources
- **HL7 v2.5+**: Health Level Seven messaging protocol
- **Surescripts**: E-prescribing network protocol
- **HIPAA**: Health Insurance Portability and Accountability Act compliance

## Installation

```bash
# Clone the repository
git clone https://github.com/HealthFlowEgy/healthflow-information-exchange.git

# Install dependencies
cd healthflow-information-exchange
pip install -r requirements.txt
```

## Usage Examples

### Creating a New Prescription (NCPDP SCRIPT)

```python
from src.prescribing.eprescribing_service import (
    NCPDPScriptBuilder,
    Prescriber,
    Patient,
    Medication,
    Pharmacy
)

# Initialize builder
builder = NCPDPScriptBuilder()

# Create prescription entities
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

medication = Medication(
    drug_description="Lisinopril 10mg Tablet",
    drug_coded="00093314501",
    quantity=30.0,
    quantity_qualifier="C38288",
    days_supply=30,
    refills=3,
    substitutions="1",
    sig="Take 1 tablet by mouth once daily",
    note="For blood pressure control",
    diagnosis="I10"
)

pharmacy = Pharmacy(
    ncpdp_id="1234567",
    npi="9876543210",
    name="CVS Pharmacy",
    address_line1="789 Pharmacy Ave",
    city="Boston",
    state="MA",
    zip_code="02101",
    phone="5551112222",
    fax="5551112223"
)

# Build NewRx message
newrx_xml = builder.build_newrx(
    prescriber=prescriber,
    patient=patient,
    medication=medication,
    pharmacy=pharmacy,
    written_date="20250130"
)

print(newrx_xml)
```

### Creating FHIR MedicationRequest

```python
from src.integrations.fhir_integration import FHIRResourceBuilder

# Initialize builder
fhir_builder = FHIRResourceBuilder(organization_id="healthflow-org")

# Build Patient resource
patient = fhir_builder.build_patient_resource(
    patient_id="patient-123",
    first_name="Jane",
    last_name="Doe",
    dob="1980-01-15",
    gender="female",
    phone="555-987-6543",
    email="jane.doe@example.com"
)

# Build Practitioner resource
practitioner = fhir_builder.build_practitioner_resource(
    practitioner_id="practitioner-456",
    first_name="John",
    last_name="Smith",
    npi="1234567890",
    specialty="Cardiology"
)

# Build MedicationRequest
med_request = fhir_builder.build_medication_request(
    request_id="prescription-789",
    patient_reference="Patient/patient-123",
    practitioner_reference="Practitioner/practitioner-456",
    medication_name="Lisinopril 10mg Tablet",
    medication_code="314076",
    dosage_instruction="Take 1 tablet by mouth once daily",
    quantity=30,
    refills=3
)

# Export to JSON
print(med_request.json(indent=2))
```

### Pharmacy Routing

```python
from src.dispensing.pharmacy_routing_service import (
    PharmacyRoutingService,
    RoutingPreferences,
    PharmacyNetwork
)

# Initialize routing service
routing_service = PharmacyRoutingService()

# Define patient preferences
preferences = RoutingPreferences(
    preferred_pharmacy_id=None,
    max_distance_miles=5.0,
    preferred_networks=[PharmacyNetwork.RETAIL_CHAIN],
    require_24_hour=False,
    require_drive_through=True,
    insurance_plan_id="plan-123"
)

# Find suitable pharmacies
pharmacies = routing_service.find_pharmacies(
    patient_latitude=42.3601,
    patient_longitude=-71.0589,
    preferences=preferences
)

for pharmacy in pharmacies:
    print(f"{pharmacy.name} - {pharmacy.distance_miles} miles")
```

### Regulator Data Access

```python
from src.regulator.regulator_api import RegulatorAPI
from datetime import datetime, timedelta

# Initialize regulator API
regulator_api = RegulatorAPI(database_connection=db)

# Query prescriptions
prescriptions = regulator_api.get_all_prescriptions(
    status="active",
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now(),
    limit=100,
    offset=0
)

# Get statistics
stats = regulator_api.get_statistics(
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now()
)

# Audit log access
regulator_api.audit_log_access(
    regulator_id="regulator-001",
    action="query",
    resource_type="prescription",
    resource_id="all",
    metadata={"filters": {"status": "active"}}
)
```

## Dependencies

```
# Core dependencies
python >= 3.8
fhir.resources >= 6.0.0
hl7apy >= 1.3.4
geopy >= 2.3.0
requests >= 2.28.0

# Optional dependencies
sqlalchemy >= 1.4.0  # For database integration
redis >= 4.0.0       # For caching
```

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/test_eprescribing.py

# Run with coverage
pytest --cov=src tests/
```

## Documentation

Detailed documentation for each module is available in the `docs/` directory:

- [Prescribing Module Documentation](docs/prescribing.md)
- [Dispensing Module Documentation](docs/dispensing.md)
- [Regulator Module Documentation](docs/regulator.md)
- [Integration Standards](docs/integrations.md)
- [API Reference](docs/api_reference.md)

## Contributing

This is an internal HealthFlow project. For contributions:

1. Create a feature branch from `main`
2. Implement changes with appropriate tests
3. Ensure all tests pass
4. Submit a pull request for review

## Security

This library handles sensitive healthcare information. Security considerations:

- All data transmission must use TLS 1.2 or higher
- PHI (Protected Health Information) must be encrypted at rest
- Access must be logged for audit trails
- Follow HIPAA compliance guidelines
- Implement proper authentication and authorization

## License

Copyright © 2025 HealthFlow. All rights reserved.

## Contact

For questions or support, contact the HealthFlow development team.

## Related Repositories

- [healthflow-regulator-dashboard](https://github.com/HealthFlowEgy/healthflow-regulator-dashboard) - Regulator portal UI
- [ai-prescription-validation-system](https://github.com/HealthFlowEgy/ai-prescription-validation-system) - AI-powered prescription validation
- [healthflow-digital-prescription-portals](https://github.com/HealthFlowEgy/healthflow-digital-prescription-portals) - Digital prescription portals for doctors and pharmacies
