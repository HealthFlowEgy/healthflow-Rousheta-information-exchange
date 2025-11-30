# HealthFlow Information Exchange Library

**Egyptian E-Prescription Information Exchange - Python Library**

A comprehensive Python library for electronic prescription information exchange in Egypt's national digital prescription infrastructure. This library provides the core APIs and data models for prescription submission, pharmacy retrieval, dispensing, and regulatory oversight.

---

## Overview

The HealthFlow Information Exchange library provides standardized interfaces for:

- **Prescription Submission Gateway**: APIs for doctors to submit e-prescriptions in Egyptian format
- **Pharmacy Retrieval APIs**: APIs for pharmacies to retrieve prescriptions from central database
- **Dispensing APIs**: APIs to record prescription dispensation
- **Regulator Central Database**: National prescription registry with analytics for EDA oversight
- **Egyptian Healthcare Standards**: Full support for Egyptian identifiers, governorates, and regulations

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  INFORMATION EXCHANGE ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      DOCTOR EMR / PORTAL                              │  │
│  └──────────────────────────┬───────────────────────────────────────────┘  │
│                             │                                               │
│                             ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │             PRESCRIPTION SUBMISSION GATEWAY                           │  │
│  │  • Validate Egyptian format (RX-2025-XXXXXX)                          │  │
│  │  • Verify doctor credentials (EMS, EDA)                               │  │
│  │  • Store in central database                                          │  │
│  │  • Generate QR code                                                   │  │
│  └──────────────────────────┬───────────────────────────────────────────┘  │
│                             │                                               │
│                             ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                  CENTRAL PRESCRIPTION DATABASE                        │  │
│  │              (National Registry - Single Source of Truth)             │  │
│  │  • All prescriptions nationally                                       │  │
│  │  • Egyptian identifiers (National ID, EMS, EDA)                       │  │
│  │  • Complete audit trail                                               │  │
│  └──────────────────────────┬───────────────────────────────────────────┘  │
│                             │                                               │
│       ┌─────────────────────┼─────────────────────┐                        │
│       ▼                     ▼                     ▼                        │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐             │
│  │  PHARMACY    │  │   DISPENSING     │  │    REGULATOR     │             │
│  │  RETRIEVAL   │  │      API         │  │   CENTRAL API    │             │
│  │     API      │  │                  │  │                  │             │
│  │──────────────│  │──────────────────│  │──────────────────│             │
│  │ • Search by  │  │ • Record         │  │ • Dashboard      │             │
│  │   patient ID │  │   dispensation   │  │   statistics     │             │
│  │ • Scan QR    │  │ • Update         │  │ • Analytics      │             │
│  │ • Verify Rx  │  │   inventory      │  │   reports        │             │
│  │              │  │ • Audit log      │  │ • Compliance     │             │
│  └──────────────┘  └──────────────────┘  └──────────────────┘             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```
healthflow-information-exchange/
├── src/
│   ├── gateway/                      # Prescription submission gateway
│   │   ├── prescription_submission_api.py
│   │   └── prescription_tracking_service.py
│   │
│   ├── apis/                         # Pharmacy and dispensing APIs
│   │   ├── pharmacy_retrieval_api.py
│   │   └── dispensing_api.py
│   │
│   ├── regulator/                    # Regulatory oversight APIs
│   │   ├── regulator_api.py
│   │   └── regulator_central_api.py
│   │
│   ├── database/                     # Central database models
│   │   └── models.py
│   │
│   ├── models/                       # Egyptian-specific models
│   │   └── egyptian_models.py
│   │
│   ├── analytics/                    # Analytics and reporting
│   │   ├── analytics_service.py
│   │   ├── analytics_engine.py
│   │   └── reporting_service.py
│   │
│   ├── integrations/                 # Healthcare standards
│   │   ├── fhir_integration.py
│   │   ├── hl7_integration.py
│   │   └── ehr_integration.py
│   │
│   └── prescribing/                  # E-prescribing services
│       └── eprescribing_service.py
│
├── docs/                             # Documentation
├── examples/                         # Usage examples
├── tests/                            # Unit and integration tests
├── requirements.txt                  # Python dependencies
└── README.md
```

---

## Egyptian Healthcare Standards

### National Identifiers

- **National ID**: 14-digit Egyptian National ID (validated format)
- **Doctor Syndicate Number**: Egyptian Medical Syndicate (EMS) registration
- **EDA License**: Egyptian Drug Authority prescriber license
- **Pharmacy License**: Egyptian Pharmacists Syndicate number
- **Prescription Number**: `RX-YYYY-XXXXXX` format

### Governorates

Supports all 27 Egyptian governorates:
- Cairo, Giza, Alexandria
- Dakahlia, Red Sea, Beheira
- And 21 more...

### Controlled Substances

Egyptian controlled substance schedules (Schedule 1-5) per EDA regulations.

---

## Key Features

### 1. Prescription Submission Gateway

```python
from src.gateway.prescription_submission_api import PrescriptionSubmissionGateway, PrescriptionFormat

gateway = PrescriptionSubmissionGateway(database_connection)

response = gateway.submit_prescription(
    prescription_data={
        "prescription_number": "RX-2025-ABC123",
        "doctor_id": "28501011234567",  # Egyptian National ID
        "doctor_syndicate_number": "EMS-12345",
        "patient_id": "29012011234567",
        "medications": [...]
    },
    format=PrescriptionFormat.JSON,
    submitter_id="28501011234567",
    submitter_type="doctor"
)
```

### 2. Pharmacy Retrieval API

```python
from src.apis.pharmacy_retrieval_api import PharmacyRetrievalAPI

retrieval_api = PharmacyRetrievalAPI(database_connection)

# Retrieve prescription by transaction ID
result = retrieval_api.get_prescription_by_tx_id(
    prescription_tx_id="RX-2025-ABC123",
    pharmacy_id="PHARM-001"
)

# Search by patient
prescriptions = retrieval_api.search_prescriptions_by_patient(
    patient_id="29012011234567",
    pharmacy_id="PHARM-001"
)
```

### 3. Dispensing API

```python
from src.apis.dispensing_api import DispensingAPI

dispensing_api = DispensingAPI(database_connection)

response = dispensing_api.record_dispensation(
    prescription_tx_id="RX-2025-ABC123",
    pharmacy_id="PHARM-001",
    pharmacy_name="Cairo Pharmacy",
    pharmacy_license="EPL-12345",
    pharmacist_id="28701011234567",
    pharmacist_name="Ahmed Mohamed",
    pharmacist_license="EPS-67890",
    medications_dispensed=[...]
)
```

### 4. Regulator Central API

```python
from src.regulator.regulator_central_api import RegulatorCentralAPI

regulator_api = RegulatorCentralAPI(
    central_database=db,
    analytics_service=analytics,
    reporting_service=reporting
)

# Get dashboard statistics
stats = regulator_api.get_dashboard_statistics(
    regulator_id="REG-001",
    period="30d"
)

# Generate compliance report
report = regulator_api.get_analytics_report(
    regulator_id="REG-001",
    report_type="compliance",
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 1, 31)
)

# Monitor doctor activity
activity = regulator_api.get_doctor_activity(
    regulator_id="REG-001",
    doctor_id="28501011234567"
)
```

### 5. Egyptian Models

```python
from src.models.egyptian_models import (
    EgyptianDoctor,
    EgyptianPatient,
    EgyptianPrescription,
    EgyptianMedicine,
    EgyptianDispensation,
    validate_egyptian_national_id,
    validate_prescription_number
)

# Validate Egyptian National ID
is_valid = validate_egyptian_national_id("28501011234567")

# Validate prescription number format
is_valid = validate_prescription_number("RX-2025-ABC123")
```

---

## Analytics and Reporting

### Prescription Analytics

- Volume metrics and trends
- Accuracy and quality metrics
- Performance analysis
- Error pattern detection

### ML-Powered Analytics

- Adverse event pattern detection
- Safety signal identification
- Anomaly detection
- Risk prediction and scoring

### Comprehensive Reporting

- Prescription volume reports
- Dispensation activity reports
- Provider and pharmacy performance
- Compliance and quality metrics
- Regulatory overview reports

---

## Installation

```bash
pip install -r requirements.txt
```

### Requirements

- Python 3.11+
- PostgreSQL (for central database)
- Redis (optional, for caching)

### Dependencies

```
# Core dependencies
requests>=2.31.0
python-dateutil>=2.8.2

# Analytics and ML
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
joblib>=1.3.0

# Data visualization (optional)
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0

# Healthcare standards
fhir.resources>=7.0.0
hl7apy>=1.3.4
```

---

## Integration with TypeScript Microservices

This Python library is designed to be used alongside the TypeScript-based HealthFlow EPX microservices:

```typescript
// Call Python library from Node.js
import { spawn } from 'child_process';

const python = spawn('python3', [
  'submit_prescription.py',
  '--prescription-id', 'RX-2025-ABC123'
]);
```

Or via REST API wrapper:

```python
# Flask/FastAPI wrapper for Python library
from fastapi import FastAPI
from src.gateway.prescription_submission_api import PrescriptionSubmissionGateway

app = FastAPI()

@app.post("/api/prescriptions/submit")
async def submit_prescription(prescription: dict):
    gateway = PrescriptionSubmissionGateway(db)
    return gateway.submit_prescription(prescription)
```

---

## License

Proprietary - HealthFlow Egypt

---

## Version

**v2.0.0** - Egyptian EPX Edition

### Changelog

- ✅ Egyptian healthcare identifiers (National ID, EMS, EDA)
- ✅ Prescription format: RX-YYYY-XXXXXX
- ✅ 27 Egyptian governorates support
- ✅ Egyptian controlled substance schedules
- ✅ Arabic language support for all models
- ✅ Prescription submission gateway
- ✅ Pharmacy retrieval APIs
- ✅ Dispensing APIs
- ✅ Regulator central database with analytics
- ✅ ML-powered analytics engine
- ✅ Comprehensive reporting services

---

## Contact

For questions or support, contact the HealthFlow development team.
