# HealthFlow Information Exchange API Documentation

## Overview

The HealthFlow Information Exchange API provides REST endpoints for Egypt's national digital prescription infrastructure. This API enables secure information exchange between doctors, pharmacies, and regulators.

**Base URL**: `http://localhost:8000` (development)  
**API Version**: 2.0.0  
**Authentication**: API Key (Header: `X-API-Key`)

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## Authentication

All API endpoints (except `/health`) require an API key passed in the request header:

```http
X-API-Key: your-api-key-here
```

## Endpoints

### Health Check

#### GET /health

Check API health status.

**No authentication required**

**Response**:
```json
{
  "status": "healthy",
  "service": "healthflow-information-exchange",
  "version": "2.0.0",
  "timestamp": "2025-01-30T12:00:00Z"
}
```

---

## Prescription Submission

### POST /api/prescriptions/submit

Submit a new e-prescription to the central database.

**Request Body**:
```json
{
  "prescription_number": "RX-2025-ABC123",
  "doctor_id": "28501011234567",
  "doctor_syndicate_number": "EMS-12345",
  "doctor_eda_license": "EDA-2025-001234",
  "patient_id": "29012011234567",
  "diagnosis": "Hypertension",
  "diagnosis_ar": "ارتفاع ضغط الدم",
  "medications": [
    {
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
  ],
  "notes": "Monitor blood pressure regularly",
  "notes_ar": "مراقبة ضغط الدم بانتظام"
}
```

**Response**:
```json
{
  "success": true,
  "submission_id": "SUB-123456",
  "prescription_number": "RX-2025-ABC123",
  "message": "Prescription submitted successfully"
}
```

**Status Codes**:
- `200`: Success
- `401`: Unauthorized (invalid API key)
- `422`: Validation error
- `500`: Server error

### GET /api/prescriptions/status/{submission_id}

Get prescription submission status.

**Parameters**:
- `submission_id` (path): Submission identifier

**Response**:
```json
{
  "success": true,
  "submission_id": "SUB-123456",
  "status": "processed",
  "prescription_number": "RX-2025-ABC123"
}
```

---

## Pharmacy Retrieval

### GET /api/pharmacy/prescription/{tx_id}

Retrieve prescription by transaction ID.

**Parameters**:
- `tx_id` (path): Prescription transaction ID (e.g., RX-2025-ABC123)
- `pharmacy_id` (query): Pharmacy identifier

**Response**:
```json
{
  "success": true,
  "prescription": {
    "prescription_number": "RX-2025-ABC123",
    "doctor_name": "Dr. Ahmed Mohamed",
    "patient_name": "Mohamed Ali",
    "medications": [...],
    "status": "active"
  }
}
```

### GET /api/pharmacy/search/patient/{patient_id}

Search prescriptions by patient National ID.

**Parameters**:
- `patient_id` (path): Egyptian National ID (14 digits)
- `pharmacy_id` (query): Pharmacy identifier
- `status` (query, optional): Filter by status

**Response**:
```json
{
  "success": true,
  "count": 5,
  "prescriptions": [...]
}
```

### GET /api/pharmacy/pending

Get pending prescriptions for pharmacy.

**Parameters**:
- `pharmacy_id` (query): Pharmacy identifier
- `limit` (query, optional): Maximum results (default: 50)

**Response**:
```json
{
  "success": true,
  "count": 10,
  "prescriptions": [...]
}
```

---

## Dispensing

### POST /api/dispensing/record

Record prescription dispensation.

**Request Body**:
```json
{
  "prescription_tx_id": "RX-2025-ABC123",
  "pharmacy_id": "PHARM-001",
  "pharmacy_name": "Cairo Central Pharmacy",
  "pharmacy_license": "EPL-12345",
  "pharmacist_id": "28701011234567",
  "pharmacist_name": "Sara Hassan",
  "pharmacist_license": "EPL-67890",
  "medications_dispensed": [...],
  "total_amount": 150.00,
  "patient_paid": 50.00,
  "insurance_covered": 100.00,
  "notes": "Patient counseled on medication usage"
}
```

**Response**:
```json
{
  "success": true,
  "dispense_id": "DISP-123456",
  "message": "Dispensation recorded successfully"
}
```

### GET /api/dispensing/{dispense_id}

Get dispensation record by ID.

**Parameters**:
- `dispense_id` (path): Dispensation identifier

**Response**:
```json
{
  "success": true,
  "dispensation": {...}
}
```

### GET /api/dispensing/pharmacy/{pharmacy_id}

Get dispensations for a pharmacy.

**Parameters**:
- `pharmacy_id` (path): Pharmacy identifier
- `start_date` (query, optional): Start date (ISO format)
- `end_date` (query, optional): End date (ISO format)
- `limit` (query, optional): Maximum results (default: 100)

**Response**:
```json
{
  "success": true,
  "count": 25,
  "dispensations": [...]
}
```

---

## Regulator

### GET /api/regulator/dashboard/statistics

Get dashboard statistics for regulatory oversight.

**Parameters**:
- `regulator_id` (query): Regulator identifier
- `period` (query, optional): Time period (7d, 30d, 90d, 1y) (default: 30d)

**Response**:
```json
{
  "success": true,
  "statistics": {
    "total_prescriptions": 15000,
    "total_dispensations": 12000,
    "active_doctors": 500,
    "active_pharmacies": 200,
    "controlled_substances": 1500
  }
}
```

### GET /api/regulator/prescription/{tx_id}

Get prescription details for regulator.

**Parameters**:
- `tx_id` (path): Prescription transaction ID
- `regulator_id` (query): Regulator identifier

**Response**:
```json
{
  "success": true,
  "prescription": {...},
  "audit_trail": [...]
}
```

### GET /api/regulator/reports/{report_type}

Generate analytics report.

**Parameters**:
- `report_type` (path): Type of report
  - `prescription_volume`
  - `dispensation_activity`
  - `compliance`
  - `quality_metrics`
  - `regulatory_overview`
- `regulator_id` (query): Regulator identifier
- `start_date` (query): Report start date (ISO format)
- `end_date` (query): Report end date (ISO format)

**Response**:
```json
{
  "success": true,
  "report": {...}
}
```

### GET /api/regulator/doctor/{doctor_id}/activity

Get doctor prescribing activity.

**Parameters**:
- `doctor_id` (path): Doctor National ID
- `regulator_id` (query): Regulator identifier
- `start_date` (query, optional): Start date (ISO format)
- `end_date` (query, optional): End date (ISO format)

**Response**:
```json
{
  "success": true,
  "doctor_id": "28501011234567",
  "activity": {...}
}
```

### GET /api/regulator/pharmacy/{pharmacy_id}/activity

Get pharmacy dispensing activity.

**Parameters**:
- `pharmacy_id` (path): Pharmacy identifier
- `regulator_id` (query): Regulator identifier
- `start_date` (query, optional): Start date (ISO format)
- `end_date` (query, optional): End date (ISO format)

**Response**:
```json
{
  "success": true,
  "pharmacy_id": "PHARM-001",
  "activity": {...}
}
```

---

## Error Responses

All endpoints return consistent error responses:

```json
{
  "success": false,
  "message": "Error description"
}
```

**Common Status Codes**:
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

---

## Rate Limiting

API requests are rate-limited to prevent abuse:
- **Default**: 60 requests per minute per API key
- **Burst**: Up to 100 requests in a short period

Rate limit headers:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1643558400
```

---

## Data Formats

### Egyptian National ID
- Format: 14 digits
- Example: `28501011234567`
- Validation: Century code, governorate code, checksum

### Prescription Number
- Format: `RX-YYYY-XXXXXX`
- Example: `RX-2025-ABC123`
- Year: 4 digits
- Sequence: Alphanumeric

### Dates
- Format: ISO 8601
- Example: `2025-01-30T12:00:00Z`

### Currency
- Currency: EGP (Egyptian Pounds)
- Format: Decimal (e.g., 150.00)

---

## Egyptian Standards

### Governorates (27 total)
Cairo, Giza, Alexandria, Dakahlia, Red Sea, Beheira, Fayoum, Gharbia, Ismailia, Menofia, Minya, Qaliubiya, New Valley, Suez, Aswan, Assiut, Beni Suef, Port Said, Damietta, Sharkia, South Sinai, Kafr El Sheikh, Matrouh, Luxor, Qena, North Sinai, Sohag

### Controlled Substance Schedules
- Schedule 1 (most restricted)
- Schedule 2
- Schedule 3
- Schedule 4
- Schedule 5 (least restricted)
- Not controlled

---

## Security Best Practices

1. **API Keys**: Store securely, never commit to version control
2. **HTTPS**: Always use HTTPS in production
3. **Input Validation**: All inputs are validated server-side
4. **Rate Limiting**: Respect rate limits
5. **Audit Logging**: All actions are logged for compliance

---

## Support

For API support, contact the HealthFlow development team or visit the documentation at `/api/docs`.
