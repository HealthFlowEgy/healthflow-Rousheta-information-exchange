"""
E-Prescription Submission Gateway API
Provides REST API endpoints for submitting electronic prescriptions in standard formats
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import logging
import uuid

logger = logging.getLogger(__name__)


class PrescriptionFormat(Enum):
    """Supported prescription formats"""
    NCPDP_SCRIPT = "ncpdp_script"
    FHIR_R4 = "fhir_r4"
    HL7_V2 = "hl7_v2"
    JSON = "json"


class SubmissionStatus(Enum):
    """Prescription submission status"""
    RECEIVED = "received"
    VALIDATED = "validated"
    PROCESSING = "processing"
    TRANSMITTED = "transmitted"
    ERROR = "error"
    REJECTED = "rejected"


@dataclass
class SubmissionResponse:
    """Response from prescription submission"""
    submission_id: str
    prescription_tx_id: str
    status: SubmissionStatus
    message: str
    timestamp: datetime
    errors: Optional[List[Dict]] = None


class PrescriptionSubmissionGateway:
    """
    Gateway for receiving and processing e-prescription submissions
    Validates format, stores in central database, and forwards to pharmacy
    """
    
    def __init__(self, database_connection, validation_service=None):
        """
        Initialize submission gateway
        
        Args:
            database_connection: Database connection for central storage
            validation_service: Optional validation service
        """
        self.db = database_connection
        self.validation_service = validation_service
    
    def submit_prescription(
        self,
        prescription_data: Dict,
        format: PrescriptionFormat,
        submitter_id: str,
        submitter_type: str = "doctor"
    ) -> SubmissionResponse:
        """
        Submit a new e-prescription
        
        Args:
            prescription_data: Prescription data in specified format
            format: Data format (NCPDP_SCRIPT, FHIR_R4, HL7_V2, JSON)
            submitter_id: ID of the submitting doctor/provider
            submitter_type: Type of submitter (doctor, system, etc.)
        
        Returns:
            SubmissionResponse with status and prescription transaction ID
        """
        submission_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        logger.info(f"Received prescription submission {submission_id} from {submitter_id}")
        
        try:
            # Step 1: Validate format
            validation_result = self._validate_prescription(prescription_data, format)
            
            if not validation_result["valid"]:
                return SubmissionResponse(
                    submission_id=submission_id,
                    prescription_tx_id="",
                    status=SubmissionStatus.REJECTED,
                    message="Validation failed",
                    timestamp=timestamp,
                    errors=validation_result.get("errors", [])
                )
            
            # Step 2: Convert to standard internal format
            normalized_data = self._normalize_prescription(prescription_data, format)
            
            # Step 3: Generate prescription transaction ID
            prescription_tx_id = self._generate_tx_id()
            
            # Step 4: Store in central database
            self._store_prescription(
                prescription_tx_id=prescription_tx_id,
                prescription_data=normalized_data,
                submitter_id=submitter_id,
                submitter_type=submitter_type,
                original_format=format.value,
                submission_id=submission_id
            )
            
            # Step 5: Forward to pharmacy (async)
            self._forward_to_pharmacy(prescription_tx_id, normalized_data)
            
            logger.info(f"Prescription {prescription_tx_id} submitted successfully")
            
            return SubmissionResponse(
                submission_id=submission_id,
                prescription_tx_id=prescription_tx_id,
                status=SubmissionStatus.TRANSMITTED,
                message="Prescription submitted and transmitted successfully",
                timestamp=timestamp
            )
            
        except Exception as e:
            logger.error(f"Error submitting prescription: {str(e)}")
            return SubmissionResponse(
                submission_id=submission_id,
                prescription_tx_id="",
                status=SubmissionStatus.ERROR,
                message=f"Submission error: {str(e)}",
                timestamp=timestamp,
                errors=[{"error": str(e)}]
            )
    
    def _validate_prescription(
        self,
        prescription_data: Dict,
        format: PrescriptionFormat
    ) -> Dict:
        """
        Validate prescription data based on format
        
        Args:
            prescription_data: Prescription data
            format: Data format
        
        Returns:
            Validation result dictionary
        """
        errors = []
        
        # Basic validation
        if format == PrescriptionFormat.JSON:
            required_fields = [
                "doctor_id", "doctor_name", "patient_id", "patient_name",
                "medications", "diagnosis"
            ]
            for field in required_fields:
                if field not in prescription_data:
                    errors.append({
                        "field": field,
                        "error": "Required field missing"
                    })
            
            # Validate medications
            if "medications" in prescription_data:
                if not isinstance(prescription_data["medications"], list):
                    errors.append({
                        "field": "medications",
                        "error": "Must be a list"
                    })
                elif len(prescription_data["medications"]) == 0:
                    errors.append({
                        "field": "medications",
                        "error": "At least one medication required"
                    })
        
        elif format == PrescriptionFormat.NCPDP_SCRIPT:
            # Validate NCPDP SCRIPT XML structure
            if not prescription_data.get("xml_content"):
                errors.append({
                    "field": "xml_content",
                    "error": "NCPDP SCRIPT XML content required"
                })
        
        elif format == PrescriptionFormat.FHIR_R4:
            # Validate FHIR R4 structure
            if not prescription_data.get("resourceType"):
                errors.append({
                    "field": "resourceType",
                    "error": "FHIR resourceType required"
                })
        
        # Use validation service if available
        if self.validation_service and not errors:
            service_result = self.validation_service.validate(prescription_data, format)
            if not service_result["valid"]:
                errors.extend(service_result.get("errors", []))
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _normalize_prescription(
        self,
        prescription_data: Dict,
        format: PrescriptionFormat
    ) -> Dict:
        """
        Convert prescription to standard internal format
        
        Args:
            prescription_data: Prescription in original format
            format: Original format
        
        Returns:
            Normalized prescription data
        """
        if format == PrescriptionFormat.JSON:
            # Already in standard format
            return prescription_data
        
        elif format == PrescriptionFormat.NCPDP_SCRIPT:
            # Parse NCPDP SCRIPT XML and convert to JSON
            # Implementation would use XML parser
            return self._parse_ncpdp_to_json(prescription_data)
        
        elif format == PrescriptionFormat.FHIR_R4:
            # Convert FHIR R4 to internal JSON format
            return self._parse_fhir_to_json(prescription_data)
        
        elif format == PrescriptionFormat.HL7_V2:
            # Parse HL7 v2 message and convert to JSON
            return self._parse_hl7_to_json(prescription_data)
        
        return prescription_data
    
    def _generate_tx_id(self) -> str:
        """
        Generate unique prescription transaction ID
        
        Returns:
            Transaction ID (e.g., RX-20250130-ABC123)
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"RX-{timestamp}-{unique_id}"
    
    def _store_prescription(
        self,
        prescription_tx_id: str,
        prescription_data: Dict,
        submitter_id: str,
        submitter_type: str,
        original_format: str,
        submission_id: str
    ):
        """
        Store prescription in central database
        
        Args:
            prescription_tx_id: Prescription transaction ID
            prescription_data: Normalized prescription data
            submitter_id: Submitter ID
            submitter_type: Submitter type
            original_format: Original data format
            submission_id: Submission ID
        """
        logger.info(f"Storing prescription {prescription_tx_id} in central database")
        
        # Implementation would insert into database
        # This is a template structure
        prescription_record = {
            "prescription_tx_id": prescription_tx_id,
            "submission_id": submission_id,
            "doctor_id": prescription_data.get("doctor_id"),
            "doctor_name": prescription_data.get("doctor_name"),
            "doctor_license": prescription_data.get("doctor_license"),
            "patient_id": prescription_data.get("patient_id"),
            "patient_name": prescription_data.get("patient_name"),
            "diagnosis": prescription_data.get("diagnosis"),
            "medications": prescription_data.get("medications"),
            "prescription_date": prescription_data.get("prescription_date", datetime.utcnow().isoformat()),
            "expiry_date": prescription_data.get("expiry_date"),
            "status": "active",
            "is_dispensed": False,
            "submitter_id": submitter_id,
            "submitter_type": submitter_type,
            "original_format": original_format,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Database insert would happen here
        # self.db.insert("prescriptions", prescription_record)
    
    def _forward_to_pharmacy(self, prescription_tx_id: str, prescription_data: Dict):
        """
        Forward prescription to designated pharmacy
        
        Args:
            prescription_tx_id: Prescription transaction ID
            prescription_data: Prescription data
        """
        pharmacy_id = prescription_data.get("pharmacy_id")
        
        if pharmacy_id:
            logger.info(f"Forwarding prescription {prescription_tx_id} to pharmacy {pharmacy_id}")
            # Implementation would send notification to pharmacy
            # This could be via webhook, message queue, or direct API call
        else:
            logger.info(f"Prescription {prescription_tx_id} stored, awaiting pharmacy retrieval")
    
    def _parse_ncpdp_to_json(self, ncpdp_data: Dict) -> Dict:
        """Parse NCPDP SCRIPT XML to JSON format"""
        # Implementation would parse XML
        return {}
    
    def _parse_fhir_to_json(self, fhir_data: Dict) -> Dict:
        """Parse FHIR R4 to JSON format"""
        # Implementation would convert FHIR resources
        return {}
    
    def _parse_hl7_to_json(self, hl7_data: Dict) -> Dict:
        """Parse HL7 v2 message to JSON format"""
        # Implementation would parse HL7 segments
        return {}
    
    def get_submission_status(self, submission_id: str) -> Dict:
        """
        Get status of a prescription submission
        
        Args:
            submission_id: Submission ID
        
        Returns:
            Status information
        """
        logger.info(f"Retrieving status for submission {submission_id}")
        
        # Query database for submission status
        # Implementation would query database
        
        return {
            "submission_id": submission_id,
            "status": "transmitted",
            "prescription_tx_id": "RX-20250130-ABC123",
            "timestamp": datetime.utcnow().isoformat()
        }
