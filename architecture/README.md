# Architecture Documentation

This folder contains comprehensive Mermaid diagrams documenting the Credit Approval System architecture.

##  Available Diagrams

### 1. [System Architecture](./system-architecture.md)
High-level overview of the entire system showing Docker services, data flow, and component interactions.

**Topics Covered:**
- Docker environment structure
- Service dependencies
- Data layer organization
- Client-server communication

### 2. [API Flow Diagram](./api-flow.md)
Detailed sequence diagrams for all API endpoints showing request-response cycles.

**Topics Covered:**
- Customer registration flow
- Eligibility checking process
- Loan creation workflow
- Data retrieval operations

### 3. [Credit Score Algorithm](./credit-score-algorithm.md)
Flowchart explaining the credit score calculation with all 5 components.

**Topics Covered:**
- Component weighting (40-20-20-10-10)
- Decision logic for each component
- Score normalization
- Edge case handling

### 4. [Loan Approval Decision Flow](./loan-approval-flow.md)
Decision tree showing the complete loan approval logic.

**Topics Covered:**
- Credit score thresholds
- Interest rate correction rules
- Rejection criteria
- Approval conditions

### 5. [Data Flow Diagram](./data-flow.md)
End-to-end data movement from Excel files to API responses.

**Topics Covered:**
- Data ingestion process
- Database operations
- Business logic execution
- Response generation

### 6. [Docker Container Architecture](./docker-architecture.md)
Detailed view of Docker containers, networks, and startup sequence.

**Topics Covered:**
- Container dependencies
- Health check mechanisms
- Volume management
- Network configuration

### 7. [Database ERD](./database-erd.md)
Entity-relationship diagram showing database schema.

**Topics Covered:**
- Table structures
- Relationships and constraints
- Indexes
- Business rules

### 8. [API Request-Response Flow](./api-request-response.md)
Sequence diagram for API request processing.

**Topics Covered:**
- Middleware processing
- Serialization/validation
- Business logic execution
- Error handling

### 9. [Deployment Flow](./deployment-flow.md)
Complete deployment process from `docker compose up` to running system.

**Topics Covered:**
- Image building
- Container orchestration
- Startup sequence
- Health verification


