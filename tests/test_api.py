"""
API integration tests
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# Test API key for development
TEST_API_KEY = "dev-api-key"


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test health check returns success"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "healthflow-information-exchange"
        assert data["version"] == "2.0.0"


class TestPrescriptionSubmission:
    """Test prescription submission endpoints"""
    
    def test_submit_prescription_without_api_key(self, sample_prescription):
        """Test submission without API key fails"""
        response = client.post("/api/prescriptions/submit", json=sample_prescription)
        assert response.status_code == 422  # Missing required header
    
    def test_submit_prescription_with_invalid_api_key(self, sample_prescription):
        """Test submission with invalid API key fails"""
        response = client.post(
            "/api/prescriptions/submit",
            json=sample_prescription,
            headers={"X-API-Key": "invalid-key"}
        )
        assert response.status_code == 401
    
    def test_submit_prescription_invalid_prescription_number(self, sample_prescription):
        """Test submission with invalid prescription number"""
        sample_prescription["prescription_number"] = "INVALID-FORMAT"
        response = client.post(
            "/api/prescriptions/submit",
            json=sample_prescription,
            headers={"X-API-Key": TEST_API_KEY}
        )
        assert response.status_code == 422  # Validation error
    
    def test_submit_prescription_invalid_national_id(self, sample_prescription):
        """Test submission with invalid National ID"""
        sample_prescription["doctor_id"] = "123"  # Too short
        response = client.post(
            "/api/prescriptions/submit",
            json=sample_prescription,
            headers={"X-API-Key": TEST_API_KEY}
        )
        assert response.status_code == 422  # Validation error


class TestPharmacyRetrieval:
    """Test pharmacy retrieval endpoints"""
    
    def test_get_prescription_without_api_key(self):
        """Test retrieval without API key fails"""
        response = client.get("/api/pharmacy/prescription/RX-2025-ABC123?pharmacy_id=PHARM-001")
        assert response.status_code == 422
    
    def test_search_by_patient_without_api_key(self):
        """Test search without API key fails"""
        response = client.get("/api/pharmacy/search/patient/28501011234567?pharmacy_id=PHARM-001")
        assert response.status_code == 422
    
    def test_get_pending_prescriptions_without_api_key(self):
        """Test pending prescriptions without API key fails"""
        response = client.get("/api/pharmacy/pending?pharmacy_id=PHARM-001")
        assert response.status_code == 422


class TestDispensing:
    """Test dispensing endpoints"""
    
    def test_record_dispensation_without_api_key(self, sample_dispensation):
        """Test dispensation recording without API key fails"""
        response = client.post("/api/dispensing/record", json=sample_dispensation)
        assert response.status_code == 422
    
    def test_get_dispensation_without_api_key(self):
        """Test get dispensation without API key fails"""
        response = client.get("/api/dispensing/DISP-001")
        assert response.status_code == 422


class TestRegulator:
    """Test regulator endpoints"""
    
    def test_get_dashboard_statistics_without_api_key(self):
        """Test dashboard statistics without API key fails"""
        response = client.get("/api/regulator/dashboard/statistics?regulator_id=REG-001")
        assert response.status_code == 422
    
    def test_get_prescription_without_api_key(self):
        """Test get prescription without API key fails"""
        response = client.get("/api/regulator/prescription/RX-2025-ABC123?regulator_id=REG-001")
        assert response.status_code == 422
    
    def test_generate_report_without_api_key(self):
        """Test generate report without API key fails"""
        response = client.get(
            "/api/regulator/reports/compliance?regulator_id=REG-001&start_date=2025-01-01&end_date=2025-01-31"
        )
        assert response.status_code == 422
    
    def test_get_doctor_activity_without_api_key(self):
        """Test doctor activity without API key fails"""
        response = client.get("/api/regulator/doctor/28501011234567/activity?regulator_id=REG-001")
        assert response.status_code == 422


class TestAPIDocumentation:
    """Test API documentation endpoints"""
    
    def test_openapi_json(self):
        """Test OpenAPI JSON is accessible"""
        response = client.get("/api/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert data["info"]["title"] == "HealthFlow Information Exchange API"
        assert data["info"]["version"] == "2.0.0"
    
    def test_swagger_docs(self):
        """Test Swagger UI is accessible"""
        response = client.get("/api/docs")
        assert response.status_code == 200
    
    def test_redoc(self):
        """Test ReDoc is accessible"""
        response = client.get("/api/redoc")
        assert response.status_code == 200
