from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta

from .models import Customer, Loan
from .serializers import (
    RegisterSerializer,
    RegisterResponseSerializer,
    CheckEligibilitySerializer,
    CheckEligibilityResponseSerializer,
    CreateLoanSerializer,
    CreateLoanResponseSerializer,
    ViewLoanSerializer,
    ViewLoansSerializer,
)
from .utils import (
    calculate_credit_score,
    check_loan_eligibility,
    calculate_monthly_installment,
)


@api_view(['POST'])
def register(request):
    """
    POST /register
    Register a new customer with approved limit based on salary.
    """
    serializer = RegisterSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Create customer
    customer = serializer.save()
    
    # Prepare response
    response_data = {
        'customer_id': customer.customer_id,
        'name': f"{customer.first_name} {customer.last_name}",
        'age': customer.age,
        'monthly_income': customer.monthly_salary,
        'approved_limit': customer.approved_limit,
        'phone_number': customer.phone_number,
    }
    
    response_serializer = RegisterResponseSerializer(response_data)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def check_eligibility(request):
    """
    POST /check-eligibility
    Check loan eligibility based on credit score and other factors.
    """
    serializer = CheckEligibilitySerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    customer_id = serializer.validated_data['customer_id']
    loan_amount = serializer.validated_data['loan_amount']
    interest_rate = serializer.validated_data['interest_rate']
    tenure = serializer.validated_data['tenure']
    
    # Check if customer exists
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check eligibility
    eligibility_result = check_loan_eligibility(
        customer, loan_amount, interest_rate, tenure
    )
    
    # Prepare response
    response_data = {
        'customer_id': customer_id,
        'approval': eligibility_result['approval'],
        'interest_rate': interest_rate,
        'corrected_interest_rate': eligibility_result['corrected_interest_rate'],
        'tenure': tenure,
        'monthly_installment': eligibility_result['monthly_installment'],
    }
    
    response_serializer = CheckEligibilityResponseSerializer(response_data)
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_loan(request):
    """
    POST /create-loan
    Create a new loan if eligible.
    """
    serializer = CreateLoanSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    customer_id = serializer.validated_data['customer_id']
    loan_amount = serializer.validated_data['loan_amount']
    interest_rate = serializer.validated_data['interest_rate']
    tenure = serializer.validated_data['tenure']
    
    # Check if customer exists
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check eligibility
    eligibility_result = check_loan_eligibility(
        customer, loan_amount, interest_rate, tenure
    )
    
    if not eligibility_result['approval']:
        # Loan not approved
        response_data = {
            'loan_id': None,
            'customer_id': customer_id,
            'loan_approved': False,
            'message': eligibility_result['message'],
            'monthly_installment': eligibility_result['monthly_installment'],
        }
        response_serializer = CreateLoanResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    # Create the loan with corrected interest rate
    corrected_rate = eligibility_result['corrected_interest_rate']
    monthly_installment = eligibility_result['monthly_installment']
    
    # Calculate start and end dates
    start_date = date.today()
    end_date = start_date + relativedelta(months=tenure)
    
    loan = Loan.objects.create(
        customer=customer,
        loan_amount=loan_amount,
        tenure=tenure,
        interest_rate=corrected_rate,
        monthly_repayment=monthly_installment,
        emis_paid_on_time=0,
        start_date=start_date,
        end_date=end_date,
    )
    
    # Update customer's current debt
    customer.current_debt += loan_amount
    customer.save()
    
    # Prepare response
    response_data = {
        'loan_id': loan.loan_id,
        'customer_id': customer_id,
        'loan_approved': True,
        'message': 'Loan approved successfully',
        'monthly_installment': monthly_installment,
    }
    
    response_serializer = CreateLoanResponseSerializer(response_data)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def view_loan(request, loan_id):
    """
    GET /view-loan/<loan_id>
    View details of a specific loan.
    """
    try:
        loan = Loan.objects.select_related('customer').get(loan_id=loan_id)
    except Loan.DoesNotExist:
        return Response(
            {'error': 'Loan not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = ViewLoanSerializer(loan)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_loans(request, customer_id):
    """
    GET /view-loans/<customer_id>
    View all current loans for a customer.
    """
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get all current loans (not yet ended)
    current_loans = Loan.objects.filter(
        customer=customer,
        end_date__gte=date.today()
    )
    
    serializer = ViewLoansSerializer(current_loans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)