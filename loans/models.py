from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(18)])
    phone_number = models.BigIntegerField()
    monthly_salary = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    approved_limit = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    current_debt = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    class Meta:
        db_table = 'customers'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.customer_id})"


class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE,
        related_name='loans'
    )
    loan_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    tenure = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Loan tenure in months"
    )
    interest_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    monthly_repayment = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    emis_paid_on_time = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    
    class Meta:
        db_table = 'loans'
    
    def __str__(self):
        return f"Loan {self.loan_id} - Customer {self.customer.customer_id}"
    
    @property
    def repayments_left(self):
        """Calculate number of EMIs left"""
        from datetime import date
        from dateutil.relativedelta import relativedelta
        
        if date.today() >= self.end_date:
            return 0
        
        months_passed = (date.today().year - self.start_date.year) * 12 + \
                       (date.today().month - self.start_date.month)
        
        emis_left = self.tenure - months_passed
        return max(0, emis_left)