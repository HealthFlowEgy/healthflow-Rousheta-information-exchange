"""
HealthFlow Information Exchange Python Client
Example integration for Python applications
"""

import requests
from typing import Dict, List, Optional
import os


class HealthFlowClient:
    """Python client for HealthFlow Information Exchange API"""
    
    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        """
        Initialize HealthFlow client
        
        Args:
            base_url: Base URL of the API (e.g., http://localhost:8000)
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make HTTP request"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"HealthFlow API Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise
    
    # ========================================================================
    # PRESCRIPTION SUBMISSION
    # ========================================================================
    
    def submit_prescription(self, prescription: Dict) -> Dict:
        """
        Submit a new e-prescription
        
        Args:
            prescription: Prescription data dictionary
        
        Returns:
            Response dictionary
        """
        return self._request('POST', '/api/prescriptions/submit', json=prescription)
    
    def get_submission_status(self, submission_id: str) -> Dict:
        """Get prescription submission status"""
        return self._request('GET', f'/api/prescriptions/status/{submission_id}')
    
    # ========================================================================
    # PHARMACY RETRIEVAL
    # ========================================================================
    
    def get_prescription(self, tx_id: str, pharmacy_id: str) -> Dict:
        """
        Retrieve prescription by transaction ID
        
        Args:
            tx_id: Prescription transaction ID
            pharmacy_id: Pharmacy identifier
        
        Returns:
            Prescription data
        """
        return self._request(
            'GET',
            f'/api/pharmacy/prescription/{tx_id}',
            params={'pharmacy_id': pharmacy_id}
        )
    
    def search_prescriptions_by_patient(
        self,
        patient_id: str,
        pharmacy_id: str,
        status: Optional[str] = None
    ) -> Dict:
        """Search prescriptions by patient National ID"""
        params = {'pharmacy_id': pharmacy_id}
        if status:
            params['status'] = status
        
        return self._request(
            'GET',
            f'/api/pharmacy/search/patient/{patient_id}',
            params=params
        )
    
    def get_pending_prescriptions(self, pharmacy_id: str, limit: int = 50) -> Dict:
        """Get pending prescriptions for pharmacy"""
        return self._request(
            'GET',
            '/api/pharmacy/pending',
            params={'pharmacy_id': pharmacy_id, 'limit': limit}
        )
    
    # ========================================================================
    # DISPENSING
    # ========================================================================
    
    def record_dispensation(self, dispensation: Dict) -> Dict:
        """
        Record prescription dispensation
        
        Args:
            dispensation: Dispensation data dictionary
        
        Returns:
            Response dictionary
        """
        return self._request('POST', '/api/dispensing/record', json=dispensation)
    
    def get_dispensation(self, dispense_id: str) -> Dict:
        """Get dispensation record by ID"""
        return self._request('GET', f'/api/dispensing/{dispense_id}')
    
    def get_pharmacy_dispensations(
        self,
        pharmacy_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100
    ) -> Dict:
        """Get dispensations for a pharmacy"""
        params = {'limit': limit}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        return self._request(
            'GET',
            f'/api/dispensing/pharmacy/{pharmacy_id}',
            params=params
        )
    
    # ========================================================================
    # REGULATOR
    # ========================================================================
    
    def get_dashboard_statistics(self, regulator_id: str, period: str = '30d') -> Dict:
        """Get dashboard statistics for regulatory oversight"""
        return self._request(
            'GET',
            '/api/regulator/dashboard/statistics',
            params={'regulator_id': regulator_id, 'period': period}
        )
    
    def get_prescription_for_regulator(self, tx_id: str, regulator_id: str) -> Dict:
        """Get prescription details for regulator"""
        return self._request(
            'GET',
            f'/api/regulator/prescription/{tx_id}',
            params={'regulator_id': regulator_id}
        )
    
    def generate_report(
        self,
        report_type: str,
        regulator_id: str,
        start_date: str,
        end_date: str
    ) -> Dict:
        """Generate analytics report"""
        return self._request(
            'GET',
            f'/api/regulator/reports/{report_type}',
            params={
                'regulator_id': regulator_id,
                'start_date': start_date,
                'end_date': end_date
            }
        )
    
    def get_doctor_activity(
        self,
        doctor_id: str,
        regulator_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """Get doctor prescribing activity"""
        params = {'regulator_id': regulator_id}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        return self._request(
            'GET',
            f'/api/regulator/doctor/{doctor_id}/activity',
            params=params
        )
    
    def get_pharmacy_activity(
        self,
        pharmacy_id: str,
        regulator_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """Get pharmacy dispensing activity"""
        params = {'regulator_id': regulator_id}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        return self._request(
            'GET',
            f'/api/regulator/pharmacy/{pharmacy_id}/activity',
            params=params
        )
    
    # ========================================================================
    # HEALTH CHECK
    # ========================================================================
    
    def health_check(self) -> Dict:
        """Check API health status"""
        return self._request('GET', '/health')


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

def example():
    """Example usage of the HealthFlow client"""
    
    # Initialize client
    client = HealthFlowClient(
        base_url='http://localhost:8000',
        api_key=os.getenv('HEALTHFLOW_API_KEY', 'dev-api-key')
    )
    
    try:
        # Health check
        health = client.health_check()
        print('Health:', health)
        
        # Submit prescription
        prescription = {
            'prescription_number': 'RX-2025-ABC123',
            'doctor_id': '28501011234567',
            'doctor_syndicate_number': 'EMS-12345',
            'doctor_eda_license': 'EDA-2025-001234',
            'patient_id': '29012011234567',
            'diagnosis': 'Hypertension',
            'diagnosis_ar': 'ارتفاع ضغط الدم',
            'medications': [
                {
                    'medicine_eda_registration': 'EDA-MED-12345',
                    'medicine_trade_name': 'Aspirin 100mg',
                    'medicine_trade_name_ar': 'أسبرين 100 ملجم',
                    'dosage': '1 tablet',
                    'frequency': 'once daily',
                    'frequency_ar': 'مرة واحدة يوميا',
                    'duration': '30 days',
                    'quantity': 30,
                    'instructions': 'Take with food',
                    'instructions_ar': 'يؤخذ مع الطعام'
                }
            ]
        }
        
        result = client.submit_prescription(prescription)
        print('Prescription submitted:', result)
        
        # Retrieve prescription
        retrieved = client.get_prescription('RX-2025-ABC123', 'PHARM-001')
        print('Retrieved prescription:', retrieved)
        
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    example()
