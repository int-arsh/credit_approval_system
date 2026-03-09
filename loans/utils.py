from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta
from loans.models import Customer, Loan


def calculate_monthly_installment(loan_amount, interest_rate, tenure):
    """
    Calculate monthly installment using compound interest formula.
    
    Formula: EMI = P × r × (1 + r)^n / ((1 + r)^n - 1)
    Where:
        P = Principal loan amount
        r = Monthly interest rate (annual rate / 12 / 100)
        n = Number of monthly installments (tenure)
    
    Args:
        loan_amount: Principal amount (Decimal or float)
        interest_rate: Annual interest rate in percentage (Decimal or float)
        tenure: Loan tenure in months (int)
    
    Returns:
        Decimal: Monthly installment amount
    """
    P = float(loan_amount)
    r = float(interest_rate) / 12 / 100  # Monthly interest rate
    n = tenure
    
    if r == 0:  # No interest case
        return Decimal(str(P / n))
    
    # EMI calculation
    emi = P * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
    
    return Decimal(str(round(emi, 2)))


def calculate_credit_score(customer):
    """
    Calculate credit score for a customer based on loan history.
    
    Components:
    i.   Past Loans paid on time (40 points)
    ii.  Number of loans taken in past (20 points) 
    iii. Loan activity in current year (20 points)
    iv.  Loan approved volume (10 points)
    v.   If sum of current loans > approved limit, credit score = 0 (10 points)
    
    Args:
        customer: Customer object
    
    Returns:
        int: Credit score out of 100
    """
    loans = Loan.objects.filter(customer=customer)
    
    if not loans.exists():
        return 50  # Default score for new customers
    
    score = 0
    
    # Component i: Past Loans paid on time (40 points)
    total_emis = 0
    emis_paid_on_time = 0
    
    for loan in loans:
        total_emis += loan.tenure
        emis_paid_on_time += loan.emis_paid_on_time
    
    if total_emis > 0:
        on_time_ratio = emis_paid_on_time / total_emis
        score += int(on_time_ratio * 40)
    
    # Component ii: Number of loans taken in past (20 points)
    # Fewer loans = better score
    num_loans = loans.count()
    if num_loans == 0:
        score += 20
    elif num_loans <= 3:
        score += 15
    elif num_loans <= 6:
        score += 10
    elif num_loans <= 10:
        score += 5
    else:
        score += 0
    
    # Component iii: Loan activity in current year (20 points)
    current_year = date.today().year
    current_year_loans = loans.filter(start_date__year=current_year)
    
    if current_year_loans.count() == 0:
        score += 20  # No new loans this year is good
    elif current_year_loans.count() <= 2:
        score += 15
    elif current_year_loans.count() <= 4:
        score += 10
    else:
        score += 5
    
    # Component iv: Loan approved volume (10 points)
    # Lower total loan amount relative to approved limit is better
    total_loan_amount = sum(float(loan.loan_amount) for loan in loans)
    approved_limit = float(customer.approved_limit)
    
    if approved_limit > 0:
        volume_ratio = total_loan_amount / approved_limit
        if volume_ratio < 0.3:
            score += 10
        elif volume_ratio < 0.5:
            score += 7
        elif volume_ratio < 0.8:
            score += 4
        else:
            score += 2
    
    # Component v: If sum of current loans > approved limit, credit score = 0
    current_loans = loans.filter(end_date__gte=date.today())
    sum_current_loans = sum(float(loan.loan_amount) for loan in current_loans)
    
    if sum_current_loans > float(customer.approved_limit):
        return 0
    
    # Ensure score is between 0 and 100
    return min(100, max(0, score))


def get_corrected_interest_rate(credit_score, requested_rate):
    """
    Get corrected interest rate based on credit score.
    
    Rules:
    - If credit_score > 50: Approve with any rate
    - If 50 > credit_score > 30: Min rate = 12%
    - If 30 > credit_score > 10: Min rate = 16%
    - If credit_score < 10: Don't approve
    
    Args:
        credit_score: Credit score (0-100)
        requested_rate: Requested interest rate
    
    Returns:
        Decimal: Corrected interest rate
    """
    requested_rate = float(requested_rate)
    
    if credit_score > 50:
        return Decimal(str(requested_rate))
    elif credit_score > 30:
        return Decimal(str(max(12.0, requested_rate)))
    elif credit_score > 10:
        return Decimal(str(max(16.0, requested_rate)))
    else:
        return Decimal(str(requested_rate))  # Will be rejected anyway


def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    """
    Check if a loan can be approved for a customer.
    
    Returns:
        dict: {
            'approval': bool,
            'credit_score': int,
            'corrected_interest_rate': Decimal,
            'monthly_installment': Decimal,
            'message': str (if not approved)
        }
    """
    # Calculate credit score
    credit_score = calculate_credit_score(customer)
    
    # Get corrected interest rate
    corrected_interest_rate = get_corrected_interest_rate(credit_score, interest_rate)
    
    # Calculate monthly installment with corrected rate
    monthly_installment = calculate_monthly_installment(
        loan_amount, 
        corrected_interest_rate, 
        tenure
    )
    
    # Check eligibility conditions
    approval = True
    message = ""
    
    # Rule 1: Credit score < 10 -> reject
    if credit_score <= 10:
        approval = False
        message = "Credit score too low. Loan cannot be approved."
    
    # Rule 2: Sum of all current EMIs > 50% of monthly salary -> reject
    if approval:
        current_loans = Loan.objects.filter(
            customer=customer,
            end_date__gte=date.today()
        )
        total_current_emis = sum(float(loan.monthly_repayment) for loan in current_loans)
        total_current_emis += float(monthly_installment)  # Add new loan EMI
        
        max_allowed_emi = float(customer.monthly_salary) * 0.5
        
        if total_current_emis > max_allowed_emi:
            approval = False
            message = "Sum of all EMIs exceeds 50% of monthly salary. Loan cannot be approved."
    
    return {
        'approval': approval,
        'credit_score': credit_score,
        'corrected_interest_rate': corrected_interest_rate,
        'monthly_installment': monthly_installment,
        'message': message if not approval else "Loan can be approved."
    }