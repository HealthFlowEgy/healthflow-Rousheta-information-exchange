# HealthFlow Information Exchange Documentation

## Table of Contents

### Getting Started
- [Installation Guide](installation.md)
- [Quick Start](quickstart.md)
- [Configuration](configuration.md)

### Modules

#### Prescribing
- [E-Prescribing Overview](prescribing.md)
- [NCPDP SCRIPT Implementation](ncpdp_script.md)
- [Prescription Lifecycle](prescription_lifecycle.md)

#### Dispensing
- [Pharmacy Routing](pharmacy_routing.md)
- [Prescription Tracking](prescription_tracking.md)
- [Fulfillment Workflow](fulfillment_workflow.md)

#### Regulator
- [Regulator API Overview](regulator_api.md)
- [Data Access Patterns](data_access.md)
- [Audit Logging](audit_logging.md)

#### Integrations
- [FHIR R4 Integration](fhir_integration.md)
- [HL7 v2.x Integration](hl7_integration.md)
- [EHR Integration](ehr_integration.md)
- [Surescripts Integration](surescripts.md)

### Standards & Compliance
- [Healthcare Standards](standards.md)
- [HIPAA Compliance](hipaa_compliance.md)
- [Security Best Practices](security.md)

### API Reference
- [Complete API Reference](api_reference.md)
- [Data Models](data_models.md)
- [Error Codes](error_codes.md)

### Development
- [Contributing Guidelines](contributing.md)
- [Testing Guide](testing.md)
- [Deployment](deployment.md)

## Overview

The HealthFlow Information Exchange library provides a comprehensive set of tools for healthcare data exchange, focusing on three primary domains:

1. **Prescribing**: Electronic prescription creation, modification, and transmission using industry-standard protocols
2. **Dispensing**: Pharmacy network management, routing, and prescription fulfillment tracking
3. **Regulatory Oversight**: Secure, audited access to prescription and dispensation data for regulatory bodies

## Key Features

- **Standards-Based**: Full implementation of NCPDP SCRIPT, HL7 FHIR R4, and HL7 v2.x
- **Interoperable**: Seamless integration with EHR systems, pharmacy networks, and regulatory platforms
- **Secure**: HIPAA-compliant with comprehensive audit logging
- **Scalable**: Designed for high-volume healthcare operations
- **Well-Documented**: Extensive documentation and examples

## Architecture

The library is organized into modular components:

```
src/
├── prescribing/          # E-prescribing functionality
├── dispensing/           # Pharmacy and dispensing services
├── regulator/            # Regulatory oversight APIs
├── integrations/         # Standards-based integrations
├── models/               # Data models and schemas
└── utils/                # Shared utilities
```

Each module is independent and can be used separately or in combination.

## Support

For technical support or questions:
- Email: support@healthflow.ai
- Documentation: https://docs.healthflow.ai
- GitHub Issues: https://github.com/HealthFlowEgy/healthflow-information-exchange/issues

## Version History

- **v1.0.0** (2025-01-30): Initial release
  - NCPDP SCRIPT 2017071 support
  - FHIR R4 integration
  - HL7 v2.x support
  - Pharmacy routing
  - Regulator API
