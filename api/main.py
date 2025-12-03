"""
FastAPI REST API Wrapper
Exposes HealthFlow Information Exchange functions as REST endpoints
"""

from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="HealthFlow Information Exchange API",
    description="Egyptian E-Prescription Information Exchange REST API",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection (to be implemented)
# from api.database import get_db
# For now, we'll use a placeholder
def get_db():
    """Get database connection"""
    # TODO: Implement actual database connection
    return None


# Pydantic models for request/response

class MedicationItem(BaseModel):
    medicine_eda_registration: str
    medicine_trade_name: str
    medicine_trade_name_ar: str
    dosage: str
    frequency: str
    frequency_ar: str
    duration: str
    quantity: int
    instructions: str
    instructions_ar: str


class PrescriptionSubmitRequest(BaseModel):
    prescription_number: str = Field(..., pattern=r"^RX-\d{4}-[A-Z0-9]+$")
    doctor_id: str = Field(..., min_length=14, max_length=14)
    doctor_syndicate_number: str
    doctor_eda_license: str
    patient_id: str = Field(..., min_length=14, max_length=14)
    diagnosis: str
    diagnosis_ar: str
    medications: List[MedicationItem]
    notes: Optional[str] = None
    notes_ar: Optional[str] = None


class DispensingRecordRequest(BaseModel):
    prescription_tx_id: str
    pharmacy_id: str
    pharmacy_name: str
    pharmacy_license: str
    pharmacist_id: str = Field(..., min_length=14, max_length=14)
    pharmacist_name: str
    pharmacist_license: str
    medications_dispensed: List[MedicationItem]
    total_amount: float
    patient_paid: float
    insurance_covered: float
    notes: Optional[str] = None


# Authentication dependency
async def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key from header"""
    # TODO: Implement proper API key verification
    expected_key = os.getenv("API_KEY", "dev-api-key")
    if x_api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return x_api_key


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "healthflow-information-exchange",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# PRESCRIPTION SUBMISSION ENDPOINTS
# ============================================================================

@app.post("/api/prescriptions/submit", tags=["Prescription Submission"])
async def submit_prescription(
    request: PrescriptionSubmitRequest,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """
    Submit a new e-prescription
    
    - **prescription_number**: Egyptian format RX-YYYY-XXXXXX
    - **doctor_id**: Egyptian National ID (14 digits)
    - **patient_id**: Egyptian National ID (14 digits)
    - **medications**: List of prescribed medications
    """
    try:
        from src.gateway.prescription_submission_api import PrescriptionSubmissionGateway, PrescriptionFormat
        
        gateway = PrescriptionSubmissionGateway(db)
        
        result = gateway.submit_prescription(
            prescription_data=request.dict(),
            format=PrescriptionFormat.JSON,
            submitter_id=request.doctor_id,
            submitter_type="doctor"
        )
        
        return result
    except Exception as e:
        logger.error(f"Error submitting prescription: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/prescriptions/status/{submission_id}", tags=["Prescription Submission"])
async def get_submission_status(
    submission_id: str,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """Get prescription submission status"""
    try:
        from src.gateway.prescription_submission_api import PrescriptionSubmissionGateway
        
        gateway = PrescriptionSubmissionGateway(db)
        result = gateway.get_submission_status(submission_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail="Submission not found")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting submission status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PHARMACY RETRIEVAL ENDPOINTS
# ============================================================================

@app.get("/api/pharmacy/prescription/{tx_id}", tags=["Pharmacy Retrieval"])
async def get_prescription(
    tx_id: str,
    pharmacy_id: str,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """
    Retrieve prescription by transaction ID
    
    - **tx_id**: Prescription transaction ID (RX-YYYY-XXXXXX)
    - **pharmacy_id**: Pharmacy identifier
    """
    try:
        from src.apis.pharmacy_retrieval_api import PharmacyRetrievalAPI
        
        api = PharmacyRetrievalAPI(db)
        result = api.get_prescription_by_tx_id(tx_id, pharmacy_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail="Prescription not found")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving prescription: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pharmacy/search/patient/{patient_id}", tags=["Pharmacy Retrieval"])
async def search_by_patient(
    patient_id: str,
    pharmacy_id: str,
    status: Optional[str] = None,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """
    Search prescriptions by patient National ID
    
    - **patient_id**: Egyptian National ID (14 digits)
    - **pharmacy_id**: Pharmacy identifier
    - **status**: Optional status filter
    """
    try:
        from src.apis.pharmacy_retrieval_api import PharmacyRetrievalAPI
        
        api = PharmacyRetrievalAPI(db)
        result = api.search_prescriptions_by_patient(
            patient_id=patient_id,
            pharmacy_id=pharmacy_id,
            status=status
        )
        
        return result
    except Exception as e:
        logger.error(f"Error searching prescriptions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pharmacy/pending", tags=["Pharmacy Retrieval"])
async def get_pending_prescriptions(
    pharmacy_id: str,
    limit: int = 50,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """Get pending prescriptions for pharmacy"""
    try:
        from src.apis.pharmacy_retrieval_api import PharmacyRetrievalAPI
        
        api = PharmacyRetrievalAPI(db)
        result = api.get_pending_prescriptions(pharmacy_id, limit)
        
        return result
    except Exception as e:
        logger.error(f"Error getting pending prescriptions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DISPENSING ENDPOINTS
# ============================================================================

@app.post("/api/dispensing/record", tags=["Dispensing"])
async def record_dispensation(
    request: DispensingRecordRequest,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """
    Record prescription dispensation
    
    - **prescription_tx_id**: Prescription transaction ID
    - **pharmacy_id**: Pharmacy identifier
    - **pharmacist_id**: Pharmacist National ID
    - **medications_dispensed**: List of dispensed medications
    """
    try:
        from src.apis.dispensing_api import DispensingAPI
        
        api = DispensingAPI(db)
        result = api.record_dispensation(
            prescription_tx_id=request.prescription_tx_id,
            pharmacy_id=request.pharmacy_id,
            pharmacy_name=request.pharmacy_name,
            pharmacy_license=request.pharmacy_license,
            pharmacist_id=request.pharmacist_id,
            pharmacist_name=request.pharmacist_name,
            pharmacist_license=request.pharmacist_license,
            medications_dispensed=[m.dict() for m in request.medications_dispensed],
            total_amount=request.total_amount,
            patient_paid=request.patient_paid,
            insurance_covered=request.insurance_covered,
            notes=request.notes
        )
        
        return result
    except Exception as e:
        logger.error(f"Error recording dispensation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dispensing/{dispense_id}", tags=["Dispensing"])
async def get_dispensation(
    dispense_id: str,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """Get dispensation record by ID"""
    try:
        from src.apis.dispensing_api import DispensingAPI
        
        api = DispensingAPI(db)
        result = api.get_dispensation(dispense_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail="Dispensation not found")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting dispensation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dispensing/pharmacy/{pharmacy_id}", tags=["Dispensing"])
async def get_pharmacy_dispensations(
    pharmacy_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """Get dispensations for a pharmacy"""
    try:
        from src.apis.dispensing_api import DispensingAPI
        
        api = DispensingAPI(db)
        
        # Parse dates if provided
        start = datetime.fromisoformat(start_date) if start_date else None
        end = datetime.fromisoformat(end_date) if end_date else None
        
        result = api.get_pharmacy_dispensations(
            pharmacy_id=pharmacy_id,
            start_date=start,
            end_date=end,
            limit=limit
        )
        
        return result
    except Exception as e:
        logger.error(f"Error getting pharmacy dispensations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# REGULATOR ENDPOINTS
# ============================================================================

@app.get("/api/regulator/dashboard/statistics", tags=["Regulator"])
async def get_dashboard_statistics(
    regulator_id: str,
    period: str = "30d",
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """
    Get dashboard statistics for regulatory oversight
    
    - **regulator_id**: Regulator identifier
    - **period**: Time period (7d, 30d, 90d, 1y)
    """
    try:
        from src.regulator.regulator_central_api import RegulatorCentralAPI
        
        api = RegulatorCentralAPI(db)
        result = api.get_dashboard_statistics(regulator_id, period)
        
        return result
    except Exception as e:
        logger.error(f"Error getting dashboard statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/regulator/prescription/{tx_id}", tags=["Regulator"])
async def get_prescription_regulator(
    tx_id: str,
    regulator_id: str,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """Get prescription details for regulator"""
    try:
        from src.regulator.regulator_central_api import RegulatorCentralAPI
        
        api = RegulatorCentralAPI(db)
        result = api.get_prescription(tx_id, regulator_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail="Prescription not found")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting prescription: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/regulator/reports/{report_type}", tags=["Regulator"])
async def generate_report(
    report_type: str,
    regulator_id: str,
    start_date: str,
    end_date: str,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """
    Generate analytics report
    
    - **report_type**: Type of report (prescription_volume, dispensation_activity, compliance, quality_metrics, regulatory_overview)
    - **regulator_id**: Regulator identifier
    - **start_date**: Report start date (ISO format)
    - **end_date**: Report end date (ISO format)
    """
    try:
        from src.regulator.regulator_central_api import RegulatorCentralAPI
        
        api = RegulatorCentralAPI(db)
        
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        result = api.get_analytics_report(
            regulator_id=regulator_id,
            report_type=report_type,
            start_date=start,
            end_date=end
        )
        
        return result
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/regulator/doctor/{doctor_id}/activity", tags=["Regulator"])
async def get_doctor_activity(
    doctor_id: str,
    regulator_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """Get doctor prescribing activity"""
    try:
        from src.regulator.regulator_central_api import RegulatorCentralAPI
        
        api = RegulatorCentralAPI(db)
        
        start = datetime.fromisoformat(start_date) if start_date else None
        end = datetime.fromisoformat(end_date) if end_date else None
        
        result = api.get_doctor_activity(
            regulator_id=regulator_id,
            doctor_id=doctor_id,
            start_date=start,
            end_date=end
        )
        
        return result
    except Exception as e:
        logger.error(f"Error getting doctor activity: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/regulator/pharmacy/{pharmacy_id}/activity", tags=["Regulator"])
async def get_pharmacy_activity(
    pharmacy_id: str,
    regulator_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db)
):
    """Get pharmacy dispensing activity"""
    try:
        from src.regulator.regulator_central_api import RegulatorCentralAPI
        
        api = RegulatorCentralAPI(db)
        
        start = datetime.fromisoformat(start_date) if start_date else None
        end = datetime.fromisoformat(end_date) if end_date else None
        
        result = api.get_pharmacy_activity(
            regulator_id=regulator_id,
            pharmacy_id=pharmacy_id,
            start_date=start,
            end_date=end
        )
        
        return result
    except Exception as e:
        logger.error(f"Error getting pharmacy activity: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
