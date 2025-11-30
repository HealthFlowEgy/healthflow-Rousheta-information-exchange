"""
Dispensing API
Provides REST API endpoints for recording prescription dispensation
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
import logging
import uuid

logger = logging.getLogger(__name__)


@dataclass
class DispenseResponse:
    """Response from dispensation recording"""
    success: bool
    dispense_id: str
    prescription_tx_id: str
    message: str
    timestamp: datetime


class DispensingAPI:
    """
    API for pharmacies to record prescription dispensation
    """
    
    def __init__(self, database_connection):
        """
        Initialize dispensing API
        
        Args:
            database_connection: Database connection
        """
        self.db = database_connection
    
    def record_dispensation(
        self,
        prescription_tx_id: str,
        pharmacy_id: str,
        pharmacy_name: str,
        pharmacy_license: str,
        pharmacist_id: str,
        pharmacist_name: str,
        pharmacist_license: str,
        medications_dispensed: List[Dict],
        notes: Optional[str] = None
    ) -> DispenseResponse:
        """
        Record a prescription dispensation
        
        Args:
            prescription_tx_id: Prescription transaction ID
            pharmacy_id: Pharmacy ID
            pharmacy_name: Pharmacy name
            pharmacy_license: Pharmacy license number
            pharmacist_id: Pharmacist ID
            pharmacist_name: Pharmacist name
            pharmacist_license: Pharmacist license number
            medications_dispensed: List of medications dispensed
            notes: Optional dispensation notes
        
        Returns:
            DispenseResponse
        """
        logger.info(f"Recording dispensation for prescription {prescription_tx_id} by pharmacy {pharmacy_id}")
        
        try:
            # Validate prescription exists and is not already dispensed
            prescription = self._get_prescription(prescription_tx_id)
            
            if not prescription:
                return DispenseResponse(
                    success=False,
                    dispense_id="",
                    prescription_tx_id=prescription_tx_id,
                    message="Prescription not found",
                    timestamp=datetime.utcnow()
                )
            
            if prescription.get("is_dispensed"):
                return DispenseResponse(
                    success=False,
                    dispense_id="",
                    prescription_tx_id=prescription_tx_id,
                    message="Prescription already dispensed",
                    timestamp=datetime.utcnow()
                )
            
            # Validate medications match prescription
            validation_result = self._validate_medications(
                prescription.get("medications", []),
                medications_dispensed
            )
            
            if not validation_result["valid"]:
                return DispenseResponse(
                    success=False,
                    dispense_id="",
                    prescription_tx_id=prescription_tx_id,
                    message=f"Medication validation failed: {validation_result['message']}",
                    timestamp=datetime.utcnow()
                )
            
            # Generate dispense ID
            dispense_id = str(uuid.uuid4())
            
            # Record dispensation in database
            self._store_dispensation(
                dispense_id=dispense_id,
                prescription_id=prescription.get("id"),
                prescription_tx_id=prescription_tx_id,
                pharmacy_id=pharmacy_id,
                pharmacy_name=pharmacy_name,
                pharmacy_license=pharmacy_license,
                pharmacist_id=pharmacist_id,
                pharmacist_name=pharmacist_name,
                pharmacist_license=pharmacist_license,
                medications_dispensed=medications_dispensed,
                notes=notes
            )
            
            # Update prescription status
            self._mark_prescription_dispensed(prescription_tx_id)
            
            # Log for audit
            self._log_dispensation(dispense_id, prescription_tx_id, pharmacy_id)
            
            logger.info(f"Dispensation {dispense_id} recorded successfully")
            
            return DispenseResponse(
                success=True,
                dispense_id=dispense_id,
                prescription_tx_id=prescription_tx_id,
                message="Dispensation recorded successfully",
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error recording dispensation: {str(e)}")
            return DispenseResponse(
                success=False,
                dispense_id="",
                prescription_tx_id=prescription_tx_id,
                message=f"Dispensation error: {str(e)}",
                timestamp=datetime.utcnow()
            )
    
    def get_dispensation(
        self,
        dispense_id: str
    ) -> Dict:
        """
        Get dispensation record by ID
        
        Args:
            dispense_id: Dispensation ID
        
        Returns:
            Dispensation record
        """
        logger.info(f"Retrieving dispensation {dispense_id}")
        
        try:
            dispensation = self._get_dispensation_from_db(dispense_id)
            
            if not dispensation:
                return {
                    "success": False,
                    "message": "Dispensation not found",
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            return {
                "success": True,
                "dispensation": dispensation,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error retrieving dispensation: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def get_pharmacy_dispensations(
        self,
        pharmacy_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict:
        """
        Get dispensations for a pharmacy
        
        Args:
            pharmacy_id: Pharmacy ID
            start_date: Start date filter
            end_date: End date filter
            limit: Maximum number of results
            offset: Pagination offset
        
        Returns:
            Dictionary with dispensation list
        """
        logger.info(f"Retrieving dispensations for pharmacy {pharmacy_id}")
        
        try:
            dispensations = self._get_pharmacy_dispensations_db(
                pharmacy_id=pharmacy_id,
                start_date=start_date,
                end_date=end_date,
                limit=limit,
                offset=offset
            )
            
            return {
                "success": True,
                "count": len(dispensations),
                "dispensations": dispensations,
                "pagination": {
                    "limit": limit,
                    "offset": offset,
                    "has_more": len(dispensations) == limit
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error retrieving pharmacy dispensations: {str(e)}")
            return {
                "success": False,
                "count": 0,
                "dispensations": [],
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _get_prescription(self, prescription_tx_id: str) -> Optional[Dict]:
        """Get prescription from database"""
        # Implementation would query database
        return None
    
    def _validate_medications(
        self,
        prescribed_medications: List[Dict],
        dispensed_medications: List[Dict]
    ) -> Dict:
        """
        Validate that dispensed medications match prescription
        
        Args:
            prescribed_medications: Medications from prescription
            dispensed_medications: Medications being dispensed
        
        Returns:
            Validation result
        """
        # Basic validation - check all prescribed medications are dispensed
        if len(dispensed_medications) != len(prescribed_medications):
            return {
                "valid": False,
                "message": "Number of dispensed medications does not match prescription"
            }
        
        # More detailed validation would check medication codes, quantities, etc.
        
        return {
            "valid": True,
            "message": "Medications validated"
        }
    
    def _store_dispensation(
        self,
        dispense_id: str,
        prescription_id: str,
        prescription_tx_id: str,
        pharmacy_id: str,
        pharmacy_name: str,
        pharmacy_license: str,
        pharmacist_id: str,
        pharmacist_name: str,
        pharmacist_license: str,
        medications_dispensed: List[Dict],
        notes: Optional[str]
    ):
        """Store dispensation in database"""
        logger.info(f"Storing dispensation {dispense_id} in central database")
        
        dispensation_record = {
            "id": dispense_id,
            "prescription_id": prescription_id,
            "prescription_tx_id": prescription_tx_id,
            "pharmacy_id": pharmacy_id,
            "pharmacy_name": pharmacy_name,
            "pharmacy_license": pharmacy_license,
            "pharmacist_id": pharmacist_id,
            "pharmacist_name": pharmacist_name,
            "pharmacist_license": pharmacist_license,
            "dispense_date": datetime.utcnow().isoformat(),
            "medications_dispensed": medications_dispensed,
            "notes": notes,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Database insert would happen here
        # self.db.insert("dispensations", dispensation_record)
    
    def _mark_prescription_dispensed(self, prescription_tx_id: str):
        """Mark prescription as dispensed"""
        logger.info(f"Marking prescription {prescription_tx_id} as dispensed")
        # Database update would happen here
        # self.db.update("prescriptions", {"is_dispensed": True}, {"prescription_tx_id": prescription_tx_id})
    
    def _get_dispensation_from_db(self, dispense_id: str) -> Optional[Dict]:
        """Get dispensation from database"""
        # Implementation would query database
        return None
    
    def _get_pharmacy_dispensations_db(
        self,
        pharmacy_id: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        limit: int,
        offset: int
    ) -> List[Dict]:
        """Get pharmacy dispensations from database"""
        # Implementation would query database
        return []
    
    def _log_dispensation(self, dispense_id: str, prescription_tx_id: str, pharmacy_id: str):
        """Log dispensation for audit"""
        logger.info(f"Audit: Dispensation {dispense_id} for prescription {prescription_tx_id} by pharmacy {pharmacy_id}")
        # Implementation would insert audit log
