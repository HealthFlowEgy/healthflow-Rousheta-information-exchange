# Integration Examples

This directory contains integration examples for connecting your TypeScript and Python microservices to the HealthFlow Information Exchange API.

## TypeScript Integration

### Installation

```bash
npm install axios
```

### Usage

```typescript
import HealthFlowClient from './healthflow-client';

const client = new HealthFlowClient({
  baseURL: 'http://localhost:8000',
  apiKey: process.env.HEALTHFLOW_API_KEY || 'dev-api-key',
});

// Submit prescription
const result = await client.submitPrescription({
  prescription_number: 'RX-2025-ABC123',
  doctor_id: '28501011234567',
  // ... other fields
});
```

### Integration with NestJS

```typescript
// healthflow.service.ts
import { Injectable } from '@nestjs/common';
import HealthFlowClient from './healthflow-client';

@Injectable()
export class HealthFlowService {
  private client: HealthFlowClient;

  constructor() {
    this.client = new HealthFlowClient({
      baseURL: process.env.HEALTHFLOW_API_URL,
      apiKey: process.env.HEALTHFLOW_API_KEY,
    });
  }

  async submitPrescription(prescription: any) {
    return await this.client.submitPrescription(prescription);
  }
}
```

### Integration with Express

```typescript
// routes/prescriptions.ts
import express from 'express';
import HealthFlowClient from './healthflow-client';

const router = express.Router();
const client = new HealthFlowClient({
  baseURL: process.env.HEALTHFLOW_API_URL,
  apiKey: process.env.HEALTHFLOW_API_KEY,
});

router.post('/submit', async (req, res) => {
  try {
    const result = await client.submitPrescription(req.body);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
```

## Python Integration

### Installation

```bash
pip install requests
```

### Usage

```python
from healthflow_client import HealthFlowClient

client = HealthFlowClient(
    base_url='http://localhost:8000',
    api_key=os.getenv('HEALTHFLOW_API_KEY', 'dev-api-key')
)

# Submit prescription
result = client.submit_prescription({
    'prescription_number': 'RX-2025-ABC123',
    'doctor_id': '28501011234567',
    # ... other fields
})
```

### Integration with FastAPI

```python
# main.py
from fastapi import FastAPI
from healthflow_client import HealthFlowClient
import os

app = FastAPI()
healthflow = HealthFlowClient(
    base_url=os.getenv('HEALTHFLOW_API_URL'),
    api_key=os.getenv('HEALTHFLOW_API_KEY')
)

@app.post("/prescriptions/submit")
async def submit_prescription(prescription: dict):
    return healthflow.submit_prescription(prescription)
```

### Integration with Flask

```python
# app.py
from flask import Flask, request, jsonify
from healthflow_client import HealthFlowClient
import os

app = Flask(__name__)
healthflow = HealthFlowClient(
    base_url=os.getenv('HEALTHFLOW_API_URL'),
    api_key=os.getenv('HEALTHFLOW_API_KEY')
)

@app.route('/prescriptions/submit', methods=['POST'])
def submit_prescription():
    try:
        result = healthflow.submit_prescription(request.json)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## Message Queue Integration

### RabbitMQ (Python)

```python
import pika
import json
from healthflow_client import HealthFlowClient

client = HealthFlowClient(
    base_url='http://localhost:8000',
    api_key='your-api-key'
)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='prescriptions')

def callback(ch, method, properties, body):
    prescription = json.loads(body)
    result = client.submit_prescription(prescription)
    print(f"Submitted: {result}")

channel.basic_consume(queue='prescriptions', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
```

### RabbitMQ (TypeScript)

```typescript
import amqp from 'amqplib';
import HealthFlowClient from './healthflow-client';

const client = new HealthFlowClient({
  baseURL: 'http://localhost:8000',
  apiKey: 'your-api-key',
});

async function consumePrescriptions() {
  const connection = await amqp.connect('amqp://localhost');
  const channel = await connection.createChannel();
  await channel.assertQueue('prescriptions');

  channel.consume('prescriptions', async (msg) => {
    if (msg) {
      const prescription = JSON.parse(msg.content.toString());
      const result = await client.submitPrescription(prescription);
      console.log('Submitted:', result);
      channel.ack(msg);
    }
  });
}

consumePrescriptions();
```

## Environment Variables

Create a `.env` file:

```env
HEALTHFLOW_API_URL=http://localhost:8000
HEALTHFLOW_API_KEY=your-api-key-here
```

## Error Handling

Both clients include built-in error handling:

### TypeScript

```typescript
try {
  const result = await client.submitPrescription(prescription);
} catch (error) {
  if (error.response) {
    console.error('API Error:', error.response.data);
  } else {
    console.error('Network Error:', error.message);
  }
}
```

### Python

```python
try:
    result = client.submit_prescription(prescription)
except requests.exceptions.HTTPError as e:
    print(f'API Error: {e.response.text}')
except requests.exceptions.RequestException as e:
    print(f'Network Error: {e}')
```

## Testing

### TypeScript (Jest)

```typescript
import HealthFlowClient from './healthflow-client';

describe('HealthFlowClient', () => {
  let client: HealthFlowClient;

  beforeAll(() => {
    client = new HealthFlowClient({
      baseURL: 'http://localhost:8000',
      apiKey: 'test-api-key',
    });
  });

  it('should submit prescription', async () => {
    const result = await client.submitPrescription(mockPrescription);
    expect(result.success).toBe(true);
  });
});
```

### Python (pytest)

```python
import pytest
from healthflow_client import HealthFlowClient

@pytest.fixture
def client():
    return HealthFlowClient(
        base_url='http://localhost:8000',
        api_key='test-api-key'
    )

def test_submit_prescription(client):
    result = client.submit_prescription(mock_prescription)
    assert result['success'] == True
```

## Production Considerations

1. **API Key Security**: Store API keys in environment variables or secret managers
2. **Timeouts**: Adjust timeout values based on your network conditions
3. **Retry Logic**: Implement retry mechanisms for transient failures
4. **Rate Limiting**: Respect API rate limits
5. **Logging**: Add comprehensive logging for debugging
6. **Monitoring**: Monitor API health and response times

## Support

For questions or issues, please contact the HealthFlow development team.
