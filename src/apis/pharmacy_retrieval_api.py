"""
Pharmacy Prescription Retrieval API
Provides REST API endpoints for pharmacies to retrieve prescriptions
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class PrescriptionRetrievalResult:
    """Result from prescription retrieval"""
    success: bool
    prescription: Optional[Dict]
    message: str
    timestamp: datetime


class PharmacyRetrievalAPI:
    """
    API for pharmacies to retrieve prescriptions from central database
    """
    
    def __init__(self, database_connection):
        """
        Initialize pharmacy retrieval API
        
        Args:
            database_connection: Database connection
        """
        self.db = database_connection
    
    def get_prescription_by_tx_id(
        self,
        prescription_tx_id: str,
        pharmacy_id: str
    ) -> PrescriptionRetrievalResult:
        """
        Retrieve prescription by transaction ID
        
        Args:
            prescription_tx_id: Prescription transaction ID
            pharmacy_id: Requesting pharmacy ID
        
        Returns:
            PrescriptionRetrievalResult
        """
        logger.info(f"Pharmacy {pharmacy_id} retrieving prescription {prescription_tx_id}")
        
        try:
            # Query prescription from database
            prescription = self._get_prescription_from_db(prescription_tx_id)
            
            if not prescription:
                return PrescriptionRetrievalResult(
                    success=False,
                    prescription=None,
                    message=f"Prescription {prescription_tx_id} not found",
                    timestamp=datetime.utcnow()
                )
            
            # Check if already dispensed
            if prescription.get("is_dispensed"):
                return PrescriptionRetrievalResult(
                    success=False,
                    prescription=None,
                    message="Prescription already dispensed",
                    timestamp=datetime.utcnow()
                )
            
            # Check if expired
            if self._is_expired(prescription):
                return PrescriptionRetrievalResult(
                    success=False,
                    prescription=None,
                    message="Prescription has expired",
                    timestamp=datetime.utcnow()
                )
            
            # Log retrieval for audit
            self._log_retrieval(prescription_tx_id, pharmacy_id)
            
            return PrescriptionRetrievalResult(
                success=True,
                prescription=prescription,
                message="Prescription retrieved successfully",
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error retrieving prescription: {str(e)}")
            return PrescriptionRetrievalResult(
                success=False,
                prescription=None,
                message=f"Retrieval error: {str(e)}",
                timestamp=datetime.utcnow()
            )
    
    def search_prescriptions_by_patient(
        self,
        patient_id: str,
        pharmacy_id: str,
        status: Optional[str] = "active"
    ) -> Dict:
        """
        Search prescriptions by patient ID
        
        Args:
            patient_id: Patient ID
            pharmacy_id: Requesting pharmacy ID
            status: Prescription status filter
        
        Returns:
            Dictionary with prescription list
        """
        logger.info(f"Pharmacy {pharmacy_id} searching prescriptions for patient {patient_id}")
        
        try:
            # Query prescriptions from database
            prescriptions = self._search_prescriptions_db(
                patient_id=patient_id,
                status=status
            )
            
            # Log search for audit
            self._log_search(patient_id, pharmacy_id)
            
            return {
                "success": True,
                "count": len(prescriptions),
                "prescriptions": prescriptions,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error searching prescriptions: {str(e)}")
            return {
                "success": False,
                "count": 0,
                "prescriptions": [],
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def get_pending_prescriptions(
        self,
        pharmacy_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> Dict:
        """
        Get pending prescriptions for a pharmacy
        
        Args:
            pharmacy_id: Pharmacy ID
            limit: Maximum number of results
            offset: Pagination offset
        
        Returns:
            Dictionary with pending prescriptions
        """
        logger.info(f"Retrieving pending prescriptions for pharmacy {pharmacy_id}")
        
        try:
            # Query pending prescriptions
            prescriptions = self._get_pending_prescriptions_db(
                pharmacy_id=pharmacy_id,
                limit=limit,
                offset=offset
            )
            
            return {
                "success": True,
                "count": len(prescriptions),
                "prescriptions": prescriptions,
                "pagination": {
                    "limit": limit,
                    "offset": offset,
                    "has_more": len(prescriptions) == limit
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error retrieving pending prescriptions: {str(e)}")
            return {
                "success": False,
                "count": 0,
                "prescriptions": [],
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _get_prescription_from_db(self, prescription_tx_id: str) -> Optional[Dict]:
        """Query prescription from database"""
        # Implementation would query database
        # This is a template structure
        return None
    
    def _search_prescriptions_db(
        self,
        patient_id: str,
        status: Optional[str] = None
    ) -> List[Dict]:
        """Search prescriptions in database"""
        # Implementation would query database
        return []
    
    def _get_pending_prescriptions_db(
        self,
        pharmacy_id: str,
        limit: int,
        offset: int
    ) -> List[Dict]:
        """Get pending prescriptions from database"""
        # Implementation would query database
        return []
    
    def _is_expired(self, prescription: Dict) -> bool:
        """Check if prescription is expired"""
        expiry_date_str = prescription.get("expiry_date")
        if not expiry_date_str:
            return False
        
        try:
            expiry_date = datetime.fromisoformat(expiry_date_str)
            return datetime.utcnow() > expiry_date
        except:
            return False
    
    def _log_retrieval(self, prescription_tx_id: str, pharmacy_id: str):
        """Log prescription retrieval for audit"""
        logger.info(f"Audit: Pharmacy {pharmacy_id} retrieved prescription {prescription_tx_id}")
        # Implementation would insert audit log
    
    def _log_search(self, patient_id: str, pharmacy_id: str):
        """Log prescription search for audit"""
        logger.info(f"Audit: Pharmacy {pharmacy_id} searched prescriptions for patient {patient_id}")
        # Implementation would insert audit log
