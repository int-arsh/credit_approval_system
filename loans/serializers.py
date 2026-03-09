from rest_framework import serializers
from .models import Customer, Loan
from decimal import Decimal


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model - used in responses"""
    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'age', 
                  'phone_number', 'monthly_salary', 'approved_limit', 'current_debt']


class RegisterSerializer(serializers.Serializer):
    """Serializer for /register endpoint"""
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField(min_value=18)
    monthly_income = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    phone_number = serializers.IntegerField()

    def create(self, validated_data):
        # Calculate approved limit: 36 * monthly_salary, rounded to nearest lakh
        monthly_income = validated_data['monthly_income']
        approved_limit = round(36 * float(monthly_income) / 100000) * 100000
        
        customer = Customer.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            age=validated_data['age'],
            phone_number=validated_data['phone_number'],
            monthly_salary=monthly_income,
            approved_limit=Decimal(str(approved_limit)),
            current_debt=Decimal('0')
        )
        return customer


class RegisterResponseSerializer(serializers.Serializer):
    """Response serializer for /register endpoint"""
    customer_id = serializers.IntegerField()
    name = serializers.CharField()
    age = serializers.IntegerField()
    monthly_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    approved_limit = serializers.DecimalField(max_digits=12, decimal_places=2)
    phone_number = serializers.IntegerField()


class CheckEligibilitySerializer(serializers.Serializer):
    """Serializer for /check-eligibility endpoint request"""
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0)
    tenure = serializers.IntegerField(min_value=1)


class CheckEligibilityResponseSerializer(serializers.Serializer):
    """Response serializer for /check-eligibility endpoint"""
    customer_id = serializers.IntegerField()
    approval = serializers.BooleanField()
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    corrected_interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2)


class CreateLoanSerializer(serializers.Serializer):
    """Serializer for /create-loan endpoint request"""
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0)
    tenure = serializers.IntegerField(min_value=1)


class CreateLoanResponseSerializer(serializers.Serializer):
    """Response serializer for /create-loan endpoint"""
    loan_id = serializers.IntegerField(allow_null=True)
    customer_id = serializers.IntegerField()
    loan_approved = serializers.BooleanField()
    message = serializers.CharField(required=False)
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2)


class LoanDetailCustomerSerializer(serializers.Serializer):
    """Nested customer serializer for loan detail view"""
    id = serializers.IntegerField(source='customer_id')
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.IntegerField()
    age = serializers.IntegerField()


class ViewLoanSerializer(serializers.ModelSerializer):
    """Serializer for /view-loan/<loan_id> endpoint"""
    customer = LoanDetailCustomerSerializer(read_only=True)
    
    class Meta:
        model = Loan
        fields = ['loan_id', 'customer', 'loan_amount', 'interest_rate', 
                  'monthly_repayment', 'tenure']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Rename monthly_repayment to monthly_installment
        representation['monthly_installment'] = representation.pop('monthly_repayment')
        return representation


class ViewLoansSerializer(serializers.ModelSerializer):
    """Serializer for /view-loans/<customer_id> endpoint"""
    repayments_left = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Loan
        fields = ['loan_id', 'loan_amount', 'interest_rate', 
                  'monthly_repayment', 'repayments_left']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Rename monthly_repayment to monthly_installment
        representation['monthly_installment'] = representation.pop('monthly_repayment')
        return representation