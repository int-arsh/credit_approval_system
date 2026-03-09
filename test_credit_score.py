import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_system.settings')
django.setup()

from loans.models import Customer
from loans.utils import (
    calculate_credit_score, 
    calculate_monthly_installment,
    check_loan_eligibility,
    get_corrected_interest_rate
)
from decimal import Decimal

print("=" * 60)
print("TESTING CREDIT SCORE UTILITIES")
print("=" * 60)

# Test 1: Monthly Installment Calculation
print("\n1. Testing Monthly Installment Calculation")
print("-" * 60)
emi = calculate_monthly_installment(
    loan_amount=Decimal('100000'),
    interest_rate=Decimal('10'),
    tenure=12
)
print(f"Loan: ₹100,000 at 10% for 12 months")
print(f"Monthly EMI: ₹{emi}")

# Test 2: Credit Score Calculation
print("\n2. Testing Credit Score Calculation")
print("-" * 60)
customer = Customer.objects.first()
if customer:
    credit_score = calculate_credit_score(customer)
    print(f"Customer: {customer.first_name} {customer.last_name} (ID: {customer.customer_id})")
    print(f"Credit Score: {credit_score}/100")
    print(f"Number of loans: {customer.loans.count()}")
else:
    print("No customers found!")

# Test 3: Corrected Interest Rate
print("\n3. Testing Corrected Interest Rate")
print("-" * 60)
test_cases = [
    (60, 8.0, "High credit score"),
    (40, 8.0, "Medium credit score"),
    (25, 8.0, "Low credit score"),
    (5, 8.0, "Very low credit score"),
]

for score, rate, description in test_cases:
    corrected = get_corrected_interest_rate(score, rate)
    print(f"{description} ({score}): {rate}% -> {corrected}%")

# Test 4: Full Eligibility Check
print("\n4. Testing Full Eligibility Check")
print("-" * 60)
if customer:
    result = check_loan_eligibility(
        customer=customer,
        loan_amount=Decimal('200000'),
        interest_rate=Decimal('10'),
        tenure=24
    )
    print(f"Customer: {customer.first_name} {customer.last_name}")
    print(f"Loan Amount: ₹200,000")
    print(f"Requested Rate: 10%")
    print(f"Tenure: 24 months")
    print(f"\nResult:")
    print(f"  Credit Score: {result['credit_score']}/100")
    print(f"  Approval: {'✓ YES' if result['approval'] else '✗ NO'}")
    print(f"  Corrected Rate: {result['corrected_interest_rate']}%")
    print(f"  Monthly EMI: ₹{result['monthly_installment']}")
    print(f"  Message: {result['message']}")

print("\n" + "=" * 60)
print("✓ All utility functions tested!")
print("=" * 60)