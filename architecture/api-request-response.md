# API Request-Response Flow

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant M as Middleware
    participant V as View Layer
    participant S as Serializer
    participant U as Utils/Business Logic
    participant DB as Database
    participant R as Response

    Note over C,R: Example: POST /api/check-eligibility

    C->>M: HTTP POST Request<br/>{customer_id, loan_amount,<br/>interest_rate, tenure}
    
    M->>M: CSRF Validation
    M->>M: Session Processing
    M->>M: Authentication (if required)
    
    M->>V: Forward to View Function<br/>check_eligibility()
    
    V->>S: Validate Request Data<br/>CheckEligibilitySerializer
    
    alt Invalid Data
        S-->>V: ValidationError
        V-->>R: 400 Bad Request
        R-->>C: Error Response
    else Valid Data
        S-->>V: Validated Data
        
        V->>DB: Fetch Customer
        DB-->>V: Customer Object
        
        alt Customer Not Found
            V-->>R: 404 Not Found
            R-->>C: Error Response
        else Customer Found
            V->>DB: Fetch Customer Loans
            DB-->>V: QuerySet of Loans
            
            V->>U: calculate_credit_score(customer)
            U->>U: Component 1: Past Loans
            U->>U: Component 2: Number of Loans
            U->>U: Component 3: Current Year
            U->>U: Component 4: Approved Volume
            U->>U: Component 5: Debt Servicing
            U-->>V: credit_score (0-100)
            
            V->>U: check_loan_eligibility()<br/>(customer, amount, rate, tenure)
            U->>U: Check debt > limit
            U->>U: Check EMI > 50% salary
            U->>U: Apply score-based rules
            U->>U: get_corrected_interest_rate()
            U->>U: calculate_monthly_installment()
            U-->>V: Eligibility Result
            
            V->>S: Serialize Response<br/>CheckEligibilityResponseSerializer
            S-->>V: JSON-ready data
            
            V-->>R: 200 OK Response
            R-->>C: Success Response<br/>{approval, interest_rate,<br/>corrected_interest_rate,<br/>monthly_installment}
        end
    end
```

## Response Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, eligibility check, loan view |
| 201 | Created | Successful customer registration, loan creation |
| 400 | Bad Request | Invalid input data, validation errors |
| 404 | Not Found | Customer or loan not found |
| 500 | Internal Server Error | Unexpected server errors |

## Error Response Format

```json
{
  "error": "Error message description",
  "details": {
    "field_name": ["Error detail for this field"]
  }
}
```
