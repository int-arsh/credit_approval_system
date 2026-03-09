# Loan Approval Decision Flow

```mermaid
flowchart TD
    START([Loan Application]) --> FETCH[Fetch Customer Data]
    FETCH --> CALC_SCORE[Calculate Credit Score]
    
    CALC_SCORE --> CHECK1{Current Debt ><br/>Approved Limit?}
    CHECK1 -->|Yes| REJECT1[❌ Reject:<br/>Debt exceeds limit]
    CHECK1 -->|No| CHECK2
    
    CHECK2{Total EMIs ><br/>50% of Salary?}
    CHECK2 -->|Yes| REJECT2[❌ Reject:<br/>EMI burden too high]
    CHECK2 -->|No| CHECK_SCORE
    
    CHECK_SCORE{Credit Score?}
    
    CHECK_SCORE -->|Score > 50| APPROVE_HIGH[✅ Approve at<br/>Requested Rate]
    
    CHECK_SCORE -->|30 < Score ≤ 50| RATE_CHECK1{Interest Rate<br/>≥ 12%?}
    RATE_CHECK1 -->|Yes| APPROVE_MED[✅ Approve at<br/>Requested Rate]
    RATE_CHECK1 -->|No| CORRECT1[✅ Approve but<br/>Correct Rate to 12%]
    
    CHECK_SCORE -->|10 < Score ≤ 30| RATE_CHECK2{Interest Rate<br/>≥ 16%?}
    RATE_CHECK2 -->|Yes| APPROVE_LOW[✅ Approve at<br/>Requested Rate]
    RATE_CHECK2 -->|No| CORRECT2[✅ Approve but<br/>Correct Rate to 16%]
    
    CHECK_SCORE -->|Score ≤ 10| REJECT3[❌ Reject:<br/>Credit score too low]
    
    APPROVE_HIGH --> CREATE
    APPROVE_MED --> CREATE
    APPROVE_LOW --> CREATE
    CORRECT1 --> CREATE
    CORRECT2 --> CREATE
    
    CREATE[Create Loan Record] --> UPDATE[Update Customer Debt]
    UPDATE --> CALC_EMI[Calculate Monthly EMI]
    CALC_EMI --> SUCCESS([Return Success Response])
    
    REJECT1 --> FAILURE
    REJECT2 --> FAILURE
    REJECT3 --> FAILURE
    FAILURE([Return Rejection Response])

    style START fill:#e1f5ff
    style CHECK1 fill:#fff9c4
    style CHECK2 fill:#fff9c4
    style CHECK_SCORE fill:#fff9c4
    style APPROVE_HIGH fill:#c8e6c9
    style APPROVE_MED fill:#c8e6c9
    style APPROVE_LOW fill:#c8e6c9
    style CORRECT1 fill:#ffe082
    style CORRECT2 fill:#ffe082
    style REJECT1 fill:#ffcdd2
    style REJECT2 fill:#ffcdd2
    style REJECT3 fill:#ffcdd2
    style SUCCESS fill:#b2dfdb
    style FAILURE fill:#ffcdd2
```

## Interest Rate Correction Rules

| Credit Score Range | Minimum Interest Rate | Action |
|-------------------|----------------------|---------|
| > 50 | No minimum | Approve at requested rate |
| 30 - 50 | 12% | Correct if requested < 12% |
| 10 - 30 | 16% | Correct if requested < 16% |
| < 10 | N/A | Reject loan |
