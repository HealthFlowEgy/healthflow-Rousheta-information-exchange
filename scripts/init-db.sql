-- Initialize HealthFlow EPX Database
-- This script is run automatically when the PostgreSQL container starts

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create indexes for full-text search
-- (Tables will be created by SQLAlchemy/Alembic)

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE healthflow_epx TO healthflow;
