"""
Regulator Central Database API
Provides comprehensive access to prescription and dispensation data with analytics
Integrates with central database and analytics services for regulatory oversight
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class RegulatorCentralAPI:
    """
    Comprehensive API for regulatory oversight
    Provides read-only access to central database with integrated analytics
    """
    
    def __init__(self, central_database, analytics_service=None, reporting_service=None):
        """
        Initialize Regulator Central API
        
        Args:
            central_database: CentralDatabase instance
            analytics_service: Optional PrescriptionAnalytics instance
            reporting_service: Optional HealthcareReportingService instance
        """
        self.db = central_database
        self.analytics = analytics_service
        self.reporting = reporting_service
    
    # Prescription Access
    
    def get_prescription(
        self,
        prescription_tx_id: str,
        regulator_id: str
    ) -> Dict:
        """
        Get prescription by transaction ID
        
        Args:
            prescription_tx_id: Prescription transaction ID
            regulator_id: Regulator ID for audit logging
        
        Returns:
            Prescription data dictionary
        """
        logger.info(f"Regulator {regulator_id} accessing prescription {prescription_tx_id}")
        
        prescription = self.db.get_prescription_by_tx_id(prescription_tx_id)
        
        # Log access for audit
        self._log_access(
            regulator_id=regulator_id,
            action="view_prescription",
            resource_type="prescription",
            resource_id=prescription_tx_id
        )
        
        if not prescription:
            return {
                "success": False,
                "message": "Prescription not found"
            }
        
        return {
            "success": True,
            "prescription": prescription.__dict__ if hasattr(prescription, '__dict__') else prescription
        }
    
    def search_prescriptions(
        self,
        regulator_id: str,
        patient_id: Optional[str] = None,
        doctor_id: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict:
        """
        Search prescriptions with filters
        
        Args:
            regulator_id: Regulator ID for audit logging
            patient_id: Filter by patient ID
            doctor_id: Filter by doctor ID
            status: Filter by status
            start_date: Filter by start date
            end_date: Filter by end date
            limit: Maximum results
            offset: Pagination offset
        
        Returns:
            Search results dictionary
        """
        logger.info(f"Regulator {regulator_id} searching prescriptions")
        
        prescriptions = self.db.search_prescriptions(
            patient_id=patient_id,
            doctor_id=doctor_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset
        )
        
        # Log search for audit
        self._log_access(
            regulator_id=regulator_id,
            action="search_prescriptions",
            resource_type="prescription",
            resource_id="search",
            metadata={
                "filters": {
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "status": status
                }
            }
        )
        
        return {
            "success": True,
            "count": len(prescriptions),
            "prescriptions": [p.__dict__ if hasattr(p, '__dict__') else p for p in prescriptions],
            "pagination": {
                "limit": limit,
                "offset": offset,
                "has_more": len(prescriptions) == limit
            }
        }
    
    # Dispensation Access
    
    def get_dispensation(
        self,
        dispense_id: str,
        regulator_id: str
    ) -> Dict:
        """
        Get dispensation by ID
        
        Args:
            dispense_id: Dispensation ID
            regulator_id: Regulator ID for audit logging
        
        Returns:
            Dispensation data dictionary
        """
        logger.info(f"Regulator {regulator_id} accessing dispensation {dispense_id}")
        
        dispensation = self.db.get_dispensation_by_id(dispense_id)
        
        # Log access for audit
        self._log_access(
            regulator_id=regulator_id,
            action="view_dispensation",
            resource_type="dispensation",
            resource_id=dispense_id
        )
        
        if not dispensation:
            return {
                "success": False,
                "message": "Dispensation not found"
            }
        
        return {
            "success": True,
            "dispensation": dispensation.__dict__ if hasattr(dispensation, '__dict__') else dispensation
        }
    
    def search_dispensations(
        self,
        regulator_id: str,
        pharmacy_id: Optional[str] = None,
        pharmacist_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict:
        """
        Search dispensations with filters
        
        Args:
            regulator_id: Regulator ID for audit logging
            pharmacy_id: Filter by pharmacy ID
            pharmacist_id: Filter by pharmacist ID
            start_date: Filter by start date
            end_date: Filter by end date
            limit: Maximum results
            offset: Pagination offset
        
        Returns:
            Search results dictionary
        """
        logger.info(f"Regulator {regulator_id} searching dispensations")
        
        dispensations = self.db.search_dispensations(
            pharmacy_id=pharmacy_id,
            pharmacist_id=pharmacist_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset
        )
        
        # Log search for audit
        self._log_access(
            regulator_id=regulator_id,
            action="search_dispensations",
            resource_type="dispensation",
            resource_id="search",
            metadata={
                "filters": {
                    "pharmacy_id": pharmacy_id,
                    "pharmacist_id": pharmacist_id
                }
            }
        )
        
        return {
            "success": True,
            "count": len(dispensations),
            "dispensations": [d.__dict__ if hasattr(d, '__dict__') else d for d in dispensations],
            "pagination": {
                "limit": limit,
                "offset": offset,
                "has_more": len(dispensations) == limit
            }
        }
    
    # Analytics and Statistics
    
    def get_dashboard_statistics(
        self,
        regulator_id: str,
        period: str = "30d"
    ) -> Dict:
        """
        Get dashboard statistics for regulatory oversight
        
        Args:
            regulator_id: Regulator ID for audit logging
            period: Time period (7d, 30d, 90d, 1y)
        
        Returns:
            Dashboard statistics dictionary
        """
        logger.info(f"Regulator {regulator_id} accessing dashboard statistics")
        
        # Calculate date range
        end_date = datetime.utcnow()
        days_map = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}
        days = days_map.get(period, 30)
        start_date = end_date - timedelta(days=days)
        
        # Get statistics from database
        prescription_stats = self.db.get_prescription_statistics(start_date, end_date)
        dispensation_stats = self.db.get_dispensation_statistics(start_date, end_date)
        
        # Log access for audit
        self._log_access(
            regulator_id=regulator_id,
            action="view_dashboard",
            resource_type="statistics",
            resource_id="dashboard"
        )
        
        return {
            "success": True,
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "days": days
            },
            "prescriptions": prescription_stats,
            "dispensations": dispensation_stats,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_analytics_report(
        self,
        regulator_id: str,
        report_type: str,
        start_date: datetime,
        end_date: datetime
    ) -> Dict:
        """
        Generate analytics report
        
        Args:
            regulator_id: Regulator ID for audit logging
            report_type: Type of report (volume, compliance, quality, etc.)
            start_date: Report start date
            end_date: Report end date
        
        Returns:
            Analytics report dictionary
        """
        logger.info(f"Regulator {regulator_id} generating {report_type} report")
        
        if not self.reporting:
            return {
                "success": False,
                "message": "Reporting service not available"
            }
        
        # Generate report based on type
        if report_type == "prescription_volume":
            report = self.reporting.generate_prescription_volume_report(start_date, end_date)
        elif report_type == "dispensation_activity":
            report = self.reporting.generate_dispensation_activity_report(start_date, end_date)
        elif report_type == "compliance":
            report = self.reporting.generate_compliance_report(start_date, end_date)
        elif report_type == "quality_metrics":
            report = self.reporting.generate_quality_metrics_report(start_date, end_date)
        elif report_type == "regulatory_overview":
            report = self.reporting.generate_regulatory_overview_report(start_date, end_date)
        else:
            return {
                "success": False,
                "message": f"Unknown report type: {report_type}"
            }
        
        # Log report generation for audit
        self._log_access(
            regulator_id=regulator_id,
            action="generate_report",
            resource_type="report",
            resource_id=report_type,
            metadata={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
        )
        
        return {
            "success": True,
            "report": report
        }
    
    def get_doctor_activity(
        self,
        regulator_id: str,
        doctor_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get doctor prescribing activity
        
        Args:
            regulator_id: Regulator ID for audit logging
            doctor_id: Doctor ID
            start_date: Start date filter
            end_date: End date filter
        
        Returns:
            Doctor activity dictionary
        """
        logger.info(f"Regulator {regulator_id} accessing activity for doctor {doctor_id}")
        
        prescriptions = self.db.search_prescriptions(
            doctor_id=doctor_id,
            start_date=start_date,
            end_date=end_date,
            limit=1000
        )
        
        # Calculate statistics
        total_prescriptions = len(prescriptions)
        medications = {}
        for p in prescriptions:
            for med in p.medications if hasattr(p, 'medications') else []:
                med_name = med.medication_name if hasattr(med, 'medication_name') else med.get('medication_name', 'Unknown')
                medications[med_name] = medications.get(med_name, 0) + 1
        
        # Log access for audit
        self._log_access(
            regulator_id=regulator_id,
            action="view_doctor_activity",
            resource_type="doctor",
            resource_id=doctor_id
        )
        
        return {
            "success": True,
            "doctor_id": doctor_id,
            "period": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None
            },
            "statistics": {
                "total_prescriptions": total_prescriptions,
                "top_medications": sorted(medications.items(), key=lambda x: x[1], reverse=True)[:10]
            }
        }
    
    def get_pharmacy_activity(
        self,
        regulator_id: str,
        pharmacy_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get pharmacy dispensing activity
        
        Args:
            regulator_id: Regulator ID for audit logging
            pharmacy_id: Pharmacy ID
            start_date: Start date filter
            end_date: End date filter
        
        Returns:
            Pharmacy activity dictionary
        """
        logger.info(f"Regulator {regulator_id} accessing activity for pharmacy {pharmacy_id}")
        
        dispensations = self.db.search_dispensations(
            pharmacy_id=pharmacy_id,
            start_date=start_date,
            end_date=end_date,
            limit=1000
        )
        
        # Calculate statistics
        total_dispensations = len(dispensations)
        
        # Log access for audit
        self._log_access(
            regulator_id=regulator_id,
            action="view_pharmacy_activity",
            resource_type="pharmacy",
            resource_id=pharmacy_id
        )
        
        return {
            "success": True,
            "pharmacy_id": pharmacy_id,
            "period": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None
            },
            "statistics": {
                "total_dispensations": total_dispensations
            }
        }
    
    # Audit Logging
    
    def _log_access(
        self,
        regulator_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        metadata: Optional[Dict] = None
    ):
        """
        Log regulator access for audit trail
        
        Args:
            regulator_id: Regulator ID
            action: Action performed
            resource_type: Type of resource accessed
            resource_id: Resource ID
            metadata: Additional metadata
        """
        from ..database.models import AuditLog
        import uuid
        
        audit_log = AuditLog(
            id=str(uuid.uuid4()),
            entity_type=resource_type,
            entity_id=resource_id,
            action=action,
            actor_id=regulator_id,
            actor_type="regulator",
            timestamp=datetime.utcnow().isoformat(),
            details=metadata
        )
        
        self.db.create_audit_log(audit_log)
        logger.info(f"Audit: Regulator {regulator_id} performed {action} on {resource_type}/{resource_id}")
