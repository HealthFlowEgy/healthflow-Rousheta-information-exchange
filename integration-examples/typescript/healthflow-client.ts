/**
 * HealthFlow Information Exchange TypeScript Client
 * Example integration for TypeScript/Node.js microservices
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios';

interface HealthFlowConfig {
  baseURL: string;
  apiKey: string;
  timeout?: number;
}

interface Medication {
  medicine_eda_registration: string;
  medicine_trade_name: string;
  medicine_trade_name_ar: string;
  dosage: string;
  frequency: string;
  frequency_ar: string;
  duration: string;
  quantity: number;
  instructions: string;
  instructions_ar: string;
}

interface PrescriptionSubmitRequest {
  prescription_number: string;
  doctor_id: string;
  doctor_syndicate_number: string;
  doctor_eda_license: string;
  patient_id: string;
  diagnosis: string;
  diagnosis_ar: string;
  medications: Medication[];
  notes?: string;
  notes_ar?: string;
}

interface DispensingRecordRequest {
  prescription_tx_id: string;
  pharmacy_id: string;
  pharmacy_name: string;
  pharmacy_license: string;
  pharmacist_id: string;
  pharmacist_name: string;
  pharmacist_license: string;
  medications_dispensed: Medication[];
  total_amount: number;
  patient_paid: number;
  insurance_covered: number;
  notes?: string;
}

export class HealthFlowClient {
  private client: AxiosInstance;

  constructor(config: HealthFlowConfig) {
    this.client = axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': config.apiKey,
      },
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('HealthFlow API Error:', error.response?.data || error.message);
        throw error;
      }
    );
  }

  // ============================================================================
  // PRESCRIPTION SUBMISSION
  // ============================================================================

  async submitPrescription(prescription: PrescriptionSubmitRequest): Promise<any> {
    const response = await this.client.post('/api/prescriptions/submit', prescription);
    return response.data;
  }

  async getSubmissionStatus(submissionId: string): Promise<any> {
    const response = await this.client.get(`/api/prescriptions/status/${submissionId}`);
    return response.data;
  }

  // ============================================================================
  // PHARMACY RETRIEVAL
  // ============================================================================

  async getPrescription(txId: string, pharmacyId: string): Promise<any> {
    const response = await this.client.get(`/api/pharmacy/prescription/${txId}`, {
      params: { pharmacy_id: pharmacyId },
    });
    return response.data;
  }

  async searchPrescriptionsByPatient(
    patientId: string,
    pharmacyId: string,
    status?: string
  ): Promise<any> {
    const response = await this.client.get(`/api/pharmacy/search/patient/${patientId}`, {
      params: { pharmacy_id: pharmacyId, status },
    });
    return response.data;
  }

  async getPendingPrescriptions(pharmacyId: string, limit: number = 50): Promise<any> {
    const response = await this.client.get('/api/pharmacy/pending', {
      params: { pharmacy_id: pharmacyId, limit },
    });
    return response.data;
  }

  // ============================================================================
  // DISPENSING
  // ============================================================================

  async recordDispensation(dispensation: DispensingRecordRequest): Promise<any> {
    const response = await this.client.post('/api/dispensing/record', dispensation);
    return response.data;
  }

  async getDispensation(dispenseId: string): Promise<any> {
    const response = await this.client.get(`/api/dispensing/${dispenseId}`);
    return response.data;
  }

  async getPharmacyDispensations(
    pharmacyId: string,
    startDate?: string,
    endDate?: string,
    limit: number = 100
  ): Promise<any> {
    const response = await this.client.get(`/api/dispensing/pharmacy/${pharmacyId}`, {
      params: { start_date: startDate, end_date: endDate, limit },
    });
    return response.data;
  }

  // ============================================================================
  // REGULATOR
  // ============================================================================

  async getDashboardStatistics(regulatorId: string, period: string = '30d'): Promise<any> {
    const response = await this.client.get('/api/regulator/dashboard/statistics', {
      params: { regulator_id: regulatorId, period },
    });
    return response.data;
  }

  async getPrescriptionForRegulator(txId: string, regulatorId: string): Promise<any> {
    const response = await this.client.get(`/api/regulator/prescription/${txId}`, {
      params: { regulator_id: regulatorId },
    });
    return response.data;
  }

  async generateReport(
    reportType: string,
    regulatorId: string,
    startDate: string,
    endDate: string
  ): Promise<any> {
    const response = await this.client.get(`/api/regulator/reports/${reportType}`, {
      params: {
        regulator_id: regulatorId,
        start_date: startDate,
        end_date: endDate,
      },
    });
    return response.data;
  }

  async getDoctorActivity(
    doctorId: string,
    regulatorId: string,
    startDate?: string,
    endDate?: string
  ): Promise<any> {
    const response = await this.client.get(`/api/regulator/doctor/${doctorId}/activity`, {
      params: {
        regulator_id: regulatorId,
        start_date: startDate,
        end_date: endDate,
      },
    });
    return response.data;
  }

  async getPharmacyActivity(
    pharmacyId: string,
    regulatorId: string,
    startDate?: string,
    endDate?: string
  ): Promise<any> {
    const response = await this.client.get(`/api/regulator/pharmacy/${pharmacyId}/activity`, {
      params: {
        regulator_id: regulatorId,
        start_date: startDate,
        end_date: endDate,
      },
    });
    return response.data;
  }

  // ============================================================================
  // HEALTH CHECK
  // ============================================================================

  async healthCheck(): Promise<any> {
    const response = await this.client.get('/health');
    return response.data;
  }
}

// ============================================================================
// USAGE EXAMPLE
// ============================================================================

async function example() {
  // Initialize client
  const client = new HealthFlowClient({
    baseURL: 'http://localhost:8000',
    apiKey: process.env.HEALTHFLOW_API_KEY || 'dev-api-key',
  });

  try {
    // Health check
    const health = await client.healthCheck();
    console.log('Health:', health);

    // Submit prescription
    const prescription: PrescriptionSubmitRequest = {
      prescription_number: 'RX-2025-ABC123',
      doctor_id: '28501011234567',
      doctor_syndicate_number: 'EMS-12345',
      doctor_eda_license: 'EDA-2025-001234',
      patient_id: '29012011234567',
      diagnosis: 'Hypertension',
      diagnosis_ar: 'ارتفاع ضغط الدم',
      medications: [
        {
          medicine_eda_registration: 'EDA-MED-12345',
          medicine_trade_name: 'Aspirin 100mg',
          medicine_trade_name_ar: 'أسبرين 100 ملجم',
          dosage: '1 tablet',
          frequency: 'once daily',
          frequency_ar: 'مرة واحدة يوميا',
          duration: '30 days',
          quantity: 30,
          instructions: 'Take with food',
          instructions_ar: 'يؤخذ مع الطعام',
        },
      ],
    };

    const result = await client.submitPrescription(prescription);
    console.log('Prescription submitted:', result);

    // Retrieve prescription
    const retrieved = await client.getPrescription('RX-2025-ABC123', 'PHARM-001');
    console.log('Retrieved prescription:', retrieved);
  } catch (error) {
    console.error('Error:', error);
  }
}

// Export for use in other modules
export default HealthFlowClient;
