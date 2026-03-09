import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 70)
print("TESTING ALL API ENDPOINTS - IMPROVED")
print("=" * 70)

# Test 1: Register a new customer
print("\n1. Testing POST /register")
print("-" * 70)
register_data = {
    "first_name": "Test",
    "last_name": "User",
    "age": 30,
    "monthly_income": 100000,  # Higher income for easier loan approval
    "phone_number": 1234567890
}

response = requests.post(f"{BASE_URL}/register", json=register_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 201:
    new_customer_id = response.json()['customer_id']
    print(f"✓ New customer created with ID: {new_customer_id}")
else:
    print("✗ Registration failed")
    exit()

# Test 2: Check eligibility for the new customer
print("\n2. Testing POST /check-eligibility")
print("-" * 70)
eligibility_data = {
    "customer_id": new_customer_id,
    "loan_amount": 200000,
    "interest_rate": 10,
    "tenure": 24
}

response = requests.post(f"{BASE_URL}/check-eligibility", json=eligibility_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

approval = response.json().get('approval', False)
if approval:
    print("✓ Loan is eligible")
else:
    print("⚠ Loan not eligible (expected for new customer with no history)")

# Test 3: Create a loan for new customer
print("\n3. Testing POST /create-loan")
print("-" * 70)
loan_data = {
    "customer_id": new_customer_id,
    "loan_amount": 200000,
    "interest_rate": 10,
    "tenure": 24
}

response = requests.post(f"{BASE_URL}/create-loan", json=loan_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 201:
    new_loan_id = response.json()['loan_id']
    print(f"✓ New loan created with ID: {new_loan_id}")
elif response.json().get('loan_approved') == False:
    print(f"⚠ Loan rejected: {response.json().get('message')}")
    new_loan_id = None

# Test 4: View the newly created loan (if created)
if new_loan_id:
    print("\n4. Testing GET /view-loan/<loan_id>")
    print("-" * 70)
    response = requests.get(f"{BASE_URL}/view-loan/{new_loan_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✓ Loan details retrieved successfully")
else:
    print("\n4. Skipping view-loan test (no loan was created)")

# Test 5: View all loans for the new customer
print("\n5. Testing GET /view-loans/<customer_id>")
print("-" * 70)
response = requests.get(f"{BASE_URL}/view-loans/{new_customer_id}")
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    loan_count = len(response.json())
    print(f"✓ Retrieved {loan_count} loan(s) for customer {new_customer_id}")

# Test 6: Test with low credit score scenario
print("\n6. Testing eligibility with low interest rate (should be corrected)")
print("-" * 70)
eligibility_data = {
    "customer_id": 1,  # Existing customer with history
    "loan_amount": 50000,
    "interest_rate": 5,  # Low rate that should be corrected
    "tenure": 12
}

response = requests.post(f"{BASE_URL}/check-eligibility", json=eligibility_data)
print(f"Status Code: {response.status_code}")
result = response.json()
print(f"Requested Rate: {result['interest_rate']}%")
print(f"Corrected Rate: {result['corrected_interest_rate']}%")
print(f"Approval: {result['approval']}")

if result['interest_rate'] != result['corrected_interest_rate']:
    print("✓ Interest rate correction working")

# Test 7: Test error handling - non-existent customer
print("\n7. Testing error handling - non-existent customer")
print("-" * 70)
response = requests.post(f"{BASE_URL}/check-eligibility", json={
    "customer_id": 99999,
    "loan_amount": 100000,
    "interest_rate": 10,
    "tenure": 12
})
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 404:
    print("✓ Error handling working correctly")

print("\n" + "=" * 70)
print("✓ All comprehensive API tests completed!")
print("=" * 70)