import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_system.settings')
django.setup()

from loans.serializers import RegisterSerializer, CustomerSerializer
from loans.models import Customer

# Test RegisterSerializer
print("Testing RegisterSerializer...")
data = {
    'first_name': 'Test',
    'last_name': 'User',
    'age': 30,
    'monthly_income': 50000,
    'phone_number': 9876543210
}

serializer = RegisterSerializer(data=data)
if serializer.is_valid():
    print("✓ RegisterSerializer validation passed")
    print(f"  Validated data: {serializer.validated_data}")
else:
    print(f"✗ Errors: {serializer.errors}")

# Test CustomerSerializer
print("\nTesting CustomerSerializer...")
customer = Customer.objects.first()
if customer:
    serializer = CustomerSerializer(customer)
    print("✓ CustomerSerializer works")
    print(f"  Data: {serializer.data}")
else:
    print("✗ No customers found in database")

print("\n✓ All serializers ready!")