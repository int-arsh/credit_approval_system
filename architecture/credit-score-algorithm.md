# Credit Score Calculation Algorithm

```mermaid
flowchart TD
    START([Start: Calculate Credit Score]) --> INIT[Initialize score = 0]
    
    INIT --> CHECK_DEBT{Current Debt ><br/>Approved Limit?}
    CHECK_DEBT -->|Yes| ZERO[Score = 0<br/>Return immediately]
    CHECK_DEBT -->|No| COMP1
    
    COMP1[Component 1:<br/>Past Loans Paid on Time] --> CALC1[Score += emis_paid_on_time /<br/>total_emis × 40]
    
    CALC1 --> COMP2[Component 2:<br/>Number of Loans]
    COMP2 --> COUNT{Loan Count}
    COUNT -->|0 loans| ADD20_1[Score += 20]
    COUNT -->|1-3 loans| ADD15[Score += 15]
    COUNT -->|4-6 loans| ADD10[Score += 10]
    COUNT -->|7+ loans| ADD5[Score += 5]
    
    ADD20_1 --> COMP3
    ADD15 --> COMP3
    ADD10 --> COMP3
    ADD5 --> COMP3
    
    COMP3[Component 3:<br/>Current Year Activity] --> CURRENT{Current Year<br/>Loans}
    CURRENT -->|0 loans| ADD20_2[Score += 20]
    CURRENT -->|1-2 loans| ADD15_2[Score += 15]
    CURRENT -->|3-4 loans| ADD10_2[Score += 10]
    CURRENT -->|5+ loans| ADD5_2[Score += 5]
    
    ADD20_2 --> COMP4
    ADD15_2 --> COMP4
    ADD10_2 --> COMP4
    ADD5_2 --> COMP4
    
    COMP4[Component 4:<br/>Approved Volume] --> VOLUME{Debt vs<br/>Limit Ratio}
    VOLUME -->|debt < 25% limit| ADD10_3[Score += 10]
    VOLUME -->|25% ≤ debt < 50%| ADD7[Score += 7]
    VOLUME -->|50% ≤ debt < 75%| ADD5_3[Score += 5]
    VOLUME -->|debt ≥ 75%| ADD3[Score += 3]
    
    ADD10_3 --> COMP5
    ADD7 --> COMP5
    ADD5_3 --> COMP5
    ADD3 --> COMP5
    
    COMP5[Component 5:<br/>Debt Servicing] --> EMI{Total EMIs /<br/>Monthly Salary}
    EMI -->|< 30%| ADD10_4[Score += 10]
    EMI -->|30% - 40%| ADD7_2[Score += 7]
    EMI -->|40% - 50%| ADD5_4[Score += 5]
    EMI -->|> 50%| ADD0[Score += 0]
    
    ADD10_4 --> NORMALIZE
    ADD7_2 --> NORMALIZE
    ADD5_4 --> NORMALIZE
    ADD0 --> NORMALIZE
    ZERO --> END
    
    NORMALIZE[Ensure 0 ≤ score ≤ 100] --> END([Return Credit Score])

    style START fill:#e1f5ff
    style CHECK_DEBT fill:#fff9c4
    style ZERO fill:#ffcdd2
    style COMP1 fill:#c5e1a5
    style COMP2 fill:#c5e1a5
    style COMP3 fill:#c5e1a5
    style COMP4 fill:#c5e1a5
    style COMP5 fill:#c5e1a5
    style END fill:#b2dfdb
```

## Scoring Breakdown

| Component | Max Points | Criteria |
|-----------|------------|----------|
| Past Loans Paid on Time | 40 | EMIs paid on time / Total EMIs |
| Number of Loans | 20 | Fewer loans = Higher score |
| Current Year Activity | 20 | Fewer new loans = Higher score |
| Approved Volume | 10 | Lower debt ratio = Higher score |
| Debt Servicing Capability | 10 | Lower EMI/salary ratio = Higher score |
| **Total** | **100** | Sum of all components |

**Special Case**: If current debt > approved limit, score = 0 immediately.
