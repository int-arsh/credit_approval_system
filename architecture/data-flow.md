# Data Flow Diagram

```mermaid
flowchart LR
    subgraph "Data Sources"
        CUSTOMER_XLS[customer_data.xlsx<br/>300 customers]
        LOAN_XLS[loan_data.xlsx<br/>782 loans]
    end

    subgraph "Import Process"
        IMPORT[Django Management<br/>Command:<br/>import_data]
        VALIDATE[Data Validation<br/>& Transformation]
    end

    subgraph "Database"
        CUST_TABLE[(customers table)]
        LOAN_TABLE[(loans table)]
        SEQ[PostgreSQL<br/>Sequences]
    end

    subgraph "API Layer"
        REGISTER[/register API]
        ELIGIBILITY[/check-eligibility API]
        CREATE[/create-loan API]
        VIEW[/view-loan API]
        VIEW_ALL[/view-loans API]
    end

    subgraph "Business Logic"
        CALC_SCORE[Calculate<br/>Credit Score]
        CALC_EMI[Calculate<br/>EMI]
        CHECK_ELIG[Check<br/>Eligibility]
        CORRECT_RATE[Correct<br/>Interest Rate]
    end

    subgraph "Responses"
        JSON[JSON Response]
    end

    CUSTOMER_XLS -->|Read| IMPORT
    LOAN_XLS -->|Read| IMPORT
    IMPORT -->|Parse & Clean| VALIDATE
    VALIDATE -->|Bulk Insert| CUST_TABLE
    VALIDATE -->|Bulk Insert| LOAN_TABLE
    VALIDATE -->|Reset| SEQ

    REGISTER -->|Insert| CUST_TABLE
    REGISTER -->|Read| CUST_TABLE
    
    ELIGIBILITY -->|Query| CUST_TABLE
    ELIGIBILITY -->|Query| LOAN_TABLE
    ELIGIBILITY --> CALC_SCORE
    ELIGIBILITY --> CHECK_ELIG
    ELIGIBILITY --> CORRECT_RATE
    ELIGIBILITY --> CALC_EMI
    
    CREATE -->|Query| CUST_TABLE
    CREATE -->|Query| LOAN_TABLE
    CREATE --> CHECK_ELIG
    CREATE -->|Insert| LOAN_TABLE
    CREATE -->|Update| CUST_TABLE
    
    VIEW -->|Query| LOAN_TABLE
    VIEW -->|Query| CUST_TABLE
    
    VIEW_ALL -->|Query| LOAN_TABLE
    VIEW_ALL -->|Calculate| CALC_EMI

    CALC_SCORE --> JSON
    CHECK_ELIG --> JSON
    CORRECT_RATE --> JSON
    CALC_EMI --> JSON
    REGISTER --> JSON
    CREATE --> JSON
    VIEW --> JSON
    VIEW_ALL --> JSON

    style CUSTOMER_XLS fill:#f8bbd0
    style LOAN_XLS fill:#f8bbd0
    style IMPORT fill:#bbdefb
    style CUST_TABLE fill:#fff9c4
    style LOAN_TABLE fill:#fff9c4
    style REGISTER fill:#c5e1a5
    style ELIGIBILITY fill:#c5e1a5
    style CREATE fill:#c5e1a5
    style JSON fill:#b2dfdb
```
